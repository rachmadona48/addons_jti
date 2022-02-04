# -*- coding: utf-8 -*-

from num2words import num2words
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class bec_voucher_payment(models.Model):
    _name = 'voucher.payment'
    _inherit = ['mail.thread']
    
#     @api.depends('amount_total')
#     def amount_to_words(self):
#         if self.env.user.company_id.text_amount_language_currency:
#             self.text_amount = num2words(self.amount_total, to='currency',
#                                          lang=self.env.user.company_id.text_amount_language_currency)
    
    @api.one
    @api.depends('line_ids.amount_total')
    def _amount_all(self):
        total = 0.0
        for line in self.line_ids:
            total += line.amount_total
            
        self.update({
            'amount_total': total,
            })

    # @api.one
    # @api.depends('line_ids.amount_total')
    # def _amount_text(self):
    #     total = 0.0
    #     for line in self.line_ids:
    #         total += line.amount_total
            
    #     self.update({
    #         'amount_to_text': total,
    #         })
    
    @api.model
    def _default_currency(self):
        return self.env.user.company_id.currency_id
    
    def get_entries(self,id_d):
        # self.env.cr.execute("""
        #     select sum(aml.debit) as debit, sum(aml.credit) as credit, aa.code as code, aa.name as name from voucher_payment vp 
        #     left join voucher_payment_line vpl on vpl.payment_id = vp.id 
        #     left join account_invoice ai on ai.id = vpl.name
        #     left join account_move am on am.id = ai.move_id 
        #     left join account_move_line aml on am.id = aml.move_id 
        #     left join account_account aa on aa.id = aml.account_id 
        #     where vp.id = %s group by aa.code, aa.name order by aa.code asc
        # """, (int(id_d),))

        self.env.cr.execute("""
            select aml.credit as credit, aa.code as code, aa.name as name, am.name as move_name from voucher_payment vp 
            left join voucher_payment_line vpl on vpl.payment_id = vp.id 
            left join account_invoice ai on ai.id = vpl.name
            left join account_move am on am.id = ai.move_id 
            left join account_move_line aml on am.id = aml.move_id 
            left join account_account aa on aa.id = aml.account_id 
            where vp.id = %s and aml.credit > 0 and (aa.rounding is null or aa.rounding is false) 
            order by am.name asc
        """, (int(id_d),))
        
        query = self.env.cr.dictfetchall()
        return query
    
    name = fields.Char('No SPK', required=True, index=True, copy=False, default='New', track_visibility='onchange')
    partner_id = fields.Many2one('res.partner', string='Vendor',required=True, domain="[('is_company','=',True)]", track_visibility='onchange')
    state = fields.Selection([
            ('draft', 'Draft'),
            ('sent', 'Sent to Confirm'),
            ('confirm', 'Confirmed'),
            ('approved', 'Approved'),
            ('cancel', 'Cancelled'),
            ], string='State',default='draft',
            copy=False, index=True, store=True, track_visibility='onchange'
           )
    journal_type_id = fields.Many2one('account.journal', string='Bank Account', 
                                      copy=False, index=True, store=True, domain=[('type', 'in', ('bank', 'cash'))],required=True)
    date_payment = fields.Date('Date Payment',readonly=True, states={'draft': [('readonly', False)]},required=True)
    currency_id = fields.Many2one('res.currency', string='Currency',
        required=True, readonly=True, states={'draft': [('readonly', False)]},
        default=_default_currency, track_visibility='onchange')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all', track_visibility='always', track_sequence=6)
    amount_to_text = fields.Monetary(string='Total Credit',store=True, readonly=True, compute='_amount_text')
    text_amount = fields.Char(string="Be Calculated", required=False)
    comment = fields.Text(string='Information',readonly=True, states={'draft': [('readonly', False)]})
    line_ids = fields.One2many('voucher.payment.line', 'payment_id','Voucher Payment',readonly=False,copy=True)
    
    
    @api.model
    def create(self, vals):
        if vals.get('name','New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('voucher.payment') or '-'
        
        voucher_payment = super(bec_voucher_payment, self).create(vals)    
        for line in voucher_payment.line_ids:
            line.name.update({
                'payment_journal_id' : voucher_payment.journal_type_id.id or False,
                
#                 'approved_number' : voucher_payment.name,
                'voucher_id' : voucher_payment.id
                })
        return voucher_payment 
    
    @api.multi
    def button_cancel(self):
        return self.write({'state': 'cancel'})
    
    @api.multi
    def button_draft(self):
        return self.write({'state': 'draft'})
    
    @api.multi
    def button_sent(self):
        if len(self.line_ids) == 0:
            raise UserError(_("Please input your Bill(s) voucher."))
            
        if self.name == 'New':
            self.name = self.env['ir.sequence'].next_by_code('voucher.payment') or '-'
        return self.write({'state': 'sent'})
    
    @api.multi
    def button_confirm(self):
        return self.write({'state': 'confirm'})
    
    @api.multi
    def button_approved(self):
#         for line in self.line_ids:
#             line.name.update({
#                 'payment_journal_id' : self.journal_type_id.id or False,
#                 'approved_number' : self.name,
#                 })
        for line in self.line_ids:
            line.name.update({
                'payment_journal_id' : self.journal_type_id.id or False,
                'voucher_id' : self.id
                })
        return self.write({'state': 'approved'})
    
    
class bec_voucher_payment_line(models.Model):
    _name = 'voucher.payment.line'
    
    payment_id = fields.Many2one('voucher.payment', string='Bill',
        ondelete='cascade', index=True)
    partner_id_order = fields.Many2one('res.partner', string='Vendor', domain="[('is_company','=',True)]", required=True)
    name = fields.Many2one('account.invoice', string='Payment',
        ondelete='cascade', index=True, required=True,domain="[('type','=','in_invoice'),('state','=','open')]")
    partner_id = fields.Many2one('res.partner', string='Vendor',required=True, related="name.partner_id")
    amount_untaxed = fields.Monetary(string='Untaxed Amount',
        store=True, related='name.amount_untaxed', track_visibility='always')
    amount_tax = fields.Monetary(string='Tax',
        store=True, related='name.amount_tax', track_visibility='always')
    amount_total = fields.Monetary(string='Total',
        store=True, related="name.amount_total")
    residual = fields.Monetary(string='Amount Due',
        store=True, related="name.residual")
    currency_id = fields.Many2one('res.currency', string='Currency',
        required=True, readonly=True,related="name.currency_id")
    state = fields.Selection([
            ('draft','Draft'),
            ('open', 'Open'),
            ('in_payment', 'In Payment'),
            ('paid', 'Paid'),
            ('cancel', 'Cancelled'),
        ], string='Status', index=True, readonly=True, related="name.state")
    
    _sql_constraints = [('order_name_uniq', 'unique (payment_id,name)',     
                 'Duplicate Payment in order line not allowed !')]
    
    
#     @api.model_create_multi
#     def create(self,vals):
#         res = super(bec_voucher_payment_line, self).create(vals)
#         res._check_no_duplicate_line()
#         return res
#      
#     @api.multi
#     def write(self,vals):
#         res = super(bec_voucher_payment_line, self).write(vals)
#         self._check_no_duplicate_line()
#         return res
    
    @api.onchange('partner_id_order')
    def invoice_with_partner(self):
        if self.partner_id_order:
            domain_asset = [('partner_id', '=',self.partner_id_order.id)
                            ,('type','=','in_invoice')
                            ,('state','=','open')
                            ,('voucher_id','=',None)]
            return {'domain': {'name': domain_asset}}
    @api.multi
    def unlink(self):
        for record in self:
            invoice = self.env['account.invoice'].search([('id','=',record.name.id)])
            invoice.update({
                'voucher_id' : '',
                'payment_journal_id' : '',
                })
        
        return super(bec_voucher_payment_line, self).unlink()
#     def _check_no_duplicate_line(self):
#         for line in self:
#             existing = self.search([
#                 ('id', '!=', line.id),
#                 ('name', '=', line.name.id),
#                 ('payment_id', '=', line.payment_id),
#                 ])
#             if existing:
#                  raise UserError(_("You cannot have two or more same payments(%s)")%(line.name.display_name))

class inherit_register_payments(models.TransientModel):
    _inherit = "account.register.payments"
    
    
    transfer_number = fields.Char('No. Transfer')
#     @api.multi
#     def _get_journal(self):
#         print("aaaa")
#         
#         return 4
    
    @api.model
    def default_get(self, fields):
        rec = super(inherit_register_payments, self).default_get(fields)
        invoice = self.env['account.invoice'].search([('id','=',self._context['active_ids'][0])])
        if invoice:
            rec['journal_id'] = invoice.payment_journal_id.id
        # print("aaaaa")
        return rec
    
#     journal_id = fields.Many2one('account.journal', string='Payment Journal', required=True, domain=[('type', 'in', ('bank', 'cash'))],compute='_get_journal')
    
    @api.multi
    def create_payments(self):
         
        if self._context['active_domain'][0][2] == 'in_invoice':
            voucher_number = []
            same_number = True
            for record in self.invoice_ids:
                if record.voucher_id.state != 'approved':
                     raise ValidationError(_('Cannot pay. Payment has not been approved.'))
                voucher_number.append(record.voucher_id.id)
                record.update({
                    'cek_number' : self.transfer_number,
                    })
                 
            same_number = len(set(voucher_number)) == 1
#        print("aaaaaa",same_number)
            if same_number == False:
#            print("nnnnn")
                raise ValidationError(_('You cannot pay with different VP number'))      
        record = super(inherit_register_payments, self).create_payments()
         
         
        return record
    
class inherit_bec_invoice_AccountInvoice(models.Model):
    
    _inherit = "account.invoice"
    
    payment_journal_id = fields.Many2one('account.journal', string='Payment Journal', readonly=True, 
                                  states={'open': [('readonly', False)]}, domain=[('type', 'in', ('bank', 'cash'))])
    voucher_id = fields.Many2one('voucher.payment', string='No SPK', readonly=True)
    cek_number = fields.Char('Nomor Giro/Cek', readonly=True, states={'paid': [('readonly', False)]})
    
    
class account_voucher_register(models.TransientModel):
    _name = "account.voucher.register"
    _description = "Request Payments"
    
    invoice_ids = fields.Many2many('account.invoice', string='Invoices', copy=False)
    journal_type_id = fields.Many2one('account.journal', string='Bank Account',
                                      copy=False, domain=[('type', 'in', ('bank', 'cash'))])
    date_payment = fields.Date('Date Payment', default=fields.Date.today)
    
    @api.multi
    def create_request(self):
        bill = self.env['account.invoice'].search([('id','in',self._context['active_ids'])])
        type_inv = [] 
        state = []
        for bill in bill:
            if 'open' not in bill.state:
                # print('Only a open payment can be asked for approval.')
                raise ValidationError(_('Only a open payment can be asked for approval.'))

            if 'in_invoice' not in bill.type:
                # print('You cannot ask approval for out invoice')
                raise ValidationError(_('You cannot ask approval for out invoice'))  

            if len(bill.voucher_id) > 0:
#                 print('You cannot ask approval for out invoice')
                raise ValidationError(_(bill.number+' already has a payment voucher payment')) 


        partner = []
        same_partner = True
        
        for vendor_id in self._context['active_ids']:
            invoice = self.env['account.invoice'].search([('id','=',vendor_id)])
            partner.append(invoice.partner_id.id)            
        
        same_partner = len(set(partner)) == 1 
        if same_partner == True:
            voucher = self.env['voucher.payment']
        
            invoice_id = []
        
            for approval in self._context['active_ids']:
                invoice_id.append({
                    'name' : approval,
                    'partner_id_order' : partner[0]
                    })
            
            vouchers = voucher.create({
                'partner_id': partner[0],
                'journal_type_id': self.journal_type_id.id,
                'date_payment' :self.date_payment,
                'line_ids' : [(0,0,line) for line in invoice_id ]
                })
            
            action_vals = {
                'name': voucher.name,
                'domain': [('id', '=', vouchers.id)],
                'view_type': 'form',
                'res_id' : vouchers.id,
                'res_model': 'voucher.payment',
                'view_id': False,
                'view_mode': 'form',
                'type': 'ir.actions.act_window',
                }
            
            return action_vals
        
        else:
            # print('You cannot ask approval for different Vendor')
            raise ValidationError(_('You cannot ask approval for different Vendor'))
            
        
           
        
class bec_account_payment(models.Model):
    _inherit= "account.payment"

    transfer_number = fields.Char('No. Transfer')
    
    def action_validate_invoice_payment(self):
        voucher = self.env['account.invoice'].search([('id','=',self._context.get('active_id'))])
        
        if voucher.type == 'in_invoice':
            
            if voucher.voucher_id.state != 'approved':
                raise ValidationError(_('You cannot pay before your voucher is approved'))  
            
            else:
                voucher.write({
                'cek_number': self.transfer_number or '0',
            })
        
        rec = super(bec_account_payment, self).action_validate_invoice_payment()
        
        return rec

    @api.model
    def default_get(self, fields):
        rec = super(bec_account_payment, self).default_get(fields)
        if rec.get('invoice_ids'):
            invoice = self.env['account.invoice'].search([('id','=',self._context['active_ids'][0])])
            if invoice:
                rec['journal_id'] = invoice.payment_journal_id.id
        return rec
        
class bec_account_account(models.Model):
    _inherit = 'account.account'
        
    rounding = fields.Boolean(string='Rounding Bill', default=False, help="Akun pembulatan atau tidak") 
        
    
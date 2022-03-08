# -*- coding: utf-8 -*-

from num2words import num2words
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.http import request

class dn_peringatan1(models.Model):
    _name = 'peringatan.satu'
    _inherit = ['mail.thread']

    @api.model
    def _default_currency(self):
        return self.env.user.company_id.currency_id

    name = fields.Char('Nomor', required=True, index=True, copy=False, default='New', track_visibility='onchange')
    bank_id = fields.Many2one('res.partner.bank', string='Bank Account',required=True)
    date = fields.Date('Date', default=fields.Date.today,required=True)
    deadline_payment = fields.Date('Payment Deadline', default=fields.Date.today,required=True)
    partner_id = fields.Many2one('res.partner', string='Vendor',required=True,  track_visibility='onchange')
    state = fields.Selection([
            ('draft', 'Draft'),
            ('validate', 'Validate'),
            ('cancel', 'Cancelled'),
            ], string='State',default='draft',
            copy=False, index=True, store=True, track_visibility='onchange'
           )
    currency_id = fields.Many2one('res.currency', string='Currency',
        required=True, readonly=True, states={'draft': [('readonly', False)]},
        default=_default_currency, track_visibility='onchange')
    line_ids = fields.One2many('peringatan.satu.line', 'peringatan_satu_id','Peringatan Line',readonly=False,copy=True)
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all', track_visibility='always', track_sequence=6)
    amount_due_total = fields.Monetary(string='Total Due', store=True, readonly=True, compute='_amount_all', track_visibility='always', track_sequence=6)

    def _get_att(self):
        # print(self.id,' id nya =========================')
        inv = request.env['peringatan.satu.line'].sudo().search([('peringatan_satu_id', '=', int(self.id))],order='id asc', limit=1)
       
        return {
            'attn': inv.name.attn,
        }

    def Terbilang(self, bil):
        angka = ("", "Satu", "Dua", "Tiga", "Empat", "Lima", "Enam", "Tujuh",
                 "Delapan", "Sembilan", "Sepuluh", "Sebelas")
        Hasil = " "
        n = int(bil)
        if n >= 0 and n <= 11:
            Hasil = Hasil + angka[n]
        elif n < 20:
            Hasil = self.Terbilang(n % 10) + " belas"
        elif n < 100:
            Hasil = self.Terbilang(n / 10) + " Puluh" + self.Terbilang(n % 10)
        elif n < 200:
            Hasil = " Seratus" + self.Terbilang(n - 100)
        elif n < 1000:
            Hasil = self.Terbilang(n / 100) + " Ratus" + self.Terbilang(n % 100)
        elif n < 2000:
            Hasil = " Seribu" + self.Terbilang(n - 1000)
        elif n < 1000000:
            Hasil = self.Terbilang(n / 1000) + " Ribu" + self.Terbilang(n % 1000)
        elif n < 1000000000:
            Hasil = self.Terbilang(n / 1000000) + " Juta" + self.Terbilang(n % 1000000)
        else:
            Hasil = self.Terbilang(n / 1000000000) + " Milyar" + self.Terbilang(n % 1000000000)
        return Hasil

    @api.one
    @api.depends('amount_total')
    def _amount_to_text_cz(self):
        for r in self:
            if r.currency_id.name == "IDR":
                r.amount_terbilang = r.Terbilang(r.amount_total) + "Rupiah"
            else:
                r.amount_terbilang = r.currency_id.amount_to_text(r.amount_total)
    amount_terbilang = fields.Char(compute='_amount_to_text_cz', string="Jumlah Terbilang")

    @api.one
    @api.depends('line_ids.amount_total')
    def _amount_all(self):
        total = 0.0
        total_due = 0.0
        for line in self.line_ids:
            total += line.amount_total
            total_due += line.residual
            
        self.update({
            'amount_total': total,
            'amount_due_total': total_due,
            })

    @api.multi
    def button_validate(self):
        if self.name == 'New':
            self.name = self.env['ir.sequence'].next_by_code('peringatan.satu')
            self.state = 'validate'

    @api.multi
    def button_cancel(self):
        return self.write({'state': 'cancel'})

class dn_peringatan1_line(models.Model):
    _name = 'peringatan.satu.line'
    
    peringatan_satu_id = fields.Many2one('peringatan.satu', string='Peringatan Satu',
        ondelete='cascade', index=True)
    partner_id_order = fields.Many2one('res.partner', string='Customer', required=True)
    name = fields.Many2one('account.invoice', string='Invoice',
        ondelete='cascade', index=True, required=True,domain="[('type','=','out_invoice'),('state','=','open')]")
    partner_id = fields.Many2one('res.partner', string='Vendor',required=True, related="name.partner_id")
    invoice_date = fields.Date('Invoice Date', related="name.date_invoice", store=True)
    date_due = fields.Date('Due Date', related="name.date_due", store=True)
    description_invoice = fields.Char('Description', related="name.description_invoice")
    currency_id = fields.Many2one('res.currency', string='Currency',
        required=True, readonly=True,related="name.currency_id")
    amount_total = fields.Monetary(string='Total',
        store=True)
    residual = fields.Monetary(string='Amount Due',
        store=True)

    @api.model
    def create(self, vals):
        inv = self.env['account.invoice'].sudo().search([('id', '=', int(vals.get('name')))])
        vals.update({
            'amount_total': inv.amount_total,
            'residual': inv.residual
        })
        return super(dn_peringatan1_line, self).create(vals)

    @api.onchange('partner_id_order')
    def invoice_with_partner(self):
        if self.partner_id_order:
            domain_asset = [('partner_id', '=',self.partner_id_order.id)
                            ,('type','=','out_invoice')
                            ,('state','=','open')]
            return {'domain': {'name': domain_asset}}

    @api.onchange('name')
    def onchange_name(self):
        for dt in self:
            dt.amount_total = dt.name.amount_total
            dt.residual = dt.name.residual

class dn_peringatan1_wizard(models.TransientModel):
    _name = "peringatan.satu.wizard"
    _description = "Wizard Peringatan Satu"
    
    invoice_ids = fields.Many2many('account.invoice', string='Invoices', copy=False)
    bank_id = fields.Many2one('res.partner.bank', string='Bank Account',required=True)
    date = fields.Date('Date', default=fields.Date.today,required=True)
    deadline_payment = fields.Date('Payment Deadline', default=fields.Date.today,required=True)
    
    @api.multi
    def create_peringatan_satu(self):
        bill = self.env['account.invoice'].search([('id','in',self._context['active_ids'])])
        type_inv = [] 
        state = []
        for bill in bill:
            if 'open' not in bill.state:
                # print('Only a open payment can be asked for approval.')
                raise ValidationError(_('Only for open invoice.'))

            if 'out_invoice' not in bill.type:
                # print('You cannot ask approval for out invoice')
                raise ValidationError(_('Only for customer invoice'))  


        partner = []
        same_partner = True
        
        for vendor_id in self._context['active_ids']:
            invoice = self.env['account.invoice'].search([('id','=',vendor_id)])
            partner.append(invoice.partner_id.id)            
        
        same_partner = len(set(partner)) == 1 
        if same_partner == True:
            peringatan_satu = self.env['peringatan.satu']
        
            invoice_id = []
        
            for approval in self._context['active_ids']:
                invoice_id.append({
                    'name' : approval,
                    'partner_id_order' : partner[0]
                    })
            
            peringatan_s = peringatan_satu.create({
                'partner_id': partner[0],
                'bank_id': self.bank_id.id,
                'date' :self.date,
                'deadline_payment' : self.deadline_payment,
                'line_ids' : [(0,0,line) for line in invoice_id ]
                })
            
            action_vals = {
                'name': peringatan_satu.name,
                'domain': [('id', '=', peringatan_s.id)],
                'view_type': 'form',
                'res_id' : peringatan_s.id,
                'res_model': 'peringatan.satu',
                'view_id': False,
                'view_mode': 'form',
                'type': 'ir.actions.act_window',
                }
            
            return action_vals
        
        else:
            raise ValidationError(_('You cannot create for different Customer'))
            
        
     

        
    
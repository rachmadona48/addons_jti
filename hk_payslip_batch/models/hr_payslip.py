# -*- coding: utf-8 -*-

from odoo import models, fields, api
import collections

class Inherit_hk_payslip_batch(models.Model):
    _inherit = 'hr.payslip.run'

    invoice_id = fields.Many2one(comodel_name='account.invoice', string="Vendor Bill")
    spk_id = fields.Many2one(comodel_name='purchase.order', string="SPK")
    type = fields.Selection([('internal', 'Internal'),('outsourcing', 'Outsourcing')], default='internal')

    @api.multi
    def act_confirm(self):
        for x in self.slip_ids:
            x.compute_sheet()
            x.action_payslip_done()

    def get_data(self, type):

        list_data = []
        for x in self.slip_ids:
            line = x.line_ids.filtered(lambda r: r.code == 'THP')
            if line:
                thp = line.total
            else:
                thp = 0
            if x.penugasan_id:
                for penugasan in x.penugasan_id.new_rangkap_tugas_ids:
                    if penugasan.analytic_id and penugasan.account_id:
                        list_data.append({
                            penugasan.analytic_id.name + '-' + str(penugasan.analytic_id.id) + '-' + str(
                                penugasan.account_id.id): thp * penugasan.persen / 100
                        })

        invoice_line_ids = []

        if list_data:
            counter = collections.Counter()
            for d in list_data:
                counter.update(d)

            result = dict(counter)

            for r in result:
                spl = r.split('-')
                kode_proyek = spl[0]
                kode_proyek_id = spl[1]
                coa = spl[2]
                amount = result[r]

                if type == 'internal':
                    invoice_line_ids.append([0, 0, {
                        'name': "Kode Proyek: " + kode_proyek,
                        'account_id': coa,
                        'price_unit': amount,
                        'quantity': 1.0,
                    }])
                else:
                    product_id = self.env['product.product'].search([('default_code', '=', 'gaji')])

                    invoice_line_ids.append([0, 0, {
                        'product_id': product_id.id,
                        'name':  "Kode Proyek: " + kode_proyek,
                        'product_qty': 1,
                        'date_planned': fields.Date.today(),
                        'product_uom': product_id.uom_id.id,
                        'price_unit': amount,
                        'account_analytic_id': int(kode_proyek_id),
                        # 'custom_price_unit': line.custom_job_costing_line_id.cost_engineer,
                        # 'qty_available': line.qty_rap,
                    }])

        return invoice_line_ids

    @api.multi
    def act_create_invoice(self):

        invoice_line_ids = self.get_data('internal')
        if invoice_line_ids:
            no_vendor = self.env['res.partner'].search([('id', '=', 15501)])
            # if no_vendor:
            #     ar = no_vendor.property_account_receivable_id.id
            # else:
            #     ar = self.env['ir.property'].with_context(force_company=self.env.user.company_id.id).get('property_account_receivable_id', 'res.partner')
            #     ar = ar.id
            invoice = self.env['account.invoice'].sudo().create({
                'name': self.name,
                'origin': self.name,
                'type': 'in_invoice',
                'reference': self.name,
                # 'account_id': ar,
                'partner_id': no_vendor.id if no_vendor else 3,
                'invoice_line_ids': invoice_line_ids,
            })
            self.invoice_id = invoice.id

    @api.multi
    def act_create_spk(self):

        invoice_line_ids = self.get_data('outsourcing')
        if invoice_line_ids:
            no_vendor = self.env['res.partner'].search([('id', '=', 15501)])
            employee_id = None
            for emp in self.env.user.employee_ids:
                employee_id = emp

            purchase_obj = self.env['purchase.order']

            po_vals = {
                'partner_id': no_vendor.id if no_vendor else 3,
                'currency_id': self.env.user.company_id.currency_id.id,
                'date_order': fields.Date.today(),
                'company_id': self.env.user.company_id.id,
                'origin': self.name,
                'is_spk': True,
                'employee_id': employee_id.id or False,
                'custom_employee_id': employee_id.id or False,
                'assigned_to': employee_id.id or False,
                'dirat_emp': employee_id.department_id.id,
                'department_emp_id': employee_id.departments_id.id,
                'sub_dirat_emp': employee_id.branch_id.id,
                'order_line': invoice_line_ids
                # 'picking_type_id': picking.id,
            }
            purchase_order = purchase_obj.create(po_vals)
            self.spk_id = purchase_order.id


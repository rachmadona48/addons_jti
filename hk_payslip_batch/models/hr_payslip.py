# -*- coding: utf-8 -*-

from odoo import models, fields, api
import collections

class Inherit_hk_payslip_batch(models.Model):
    _inherit = 'hr.payslip.run'

    invoice_id = fields.Many2one(comodel_name='account.invoice', string="Invoice")

    @api.multi
    def act_confirm(self):
        for x in self.slip_ids:
            x.compute_sheet()
            x.action_payslip_done()

    @api.multi
    def act_create_invoice(self):
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
                            penugasan.analytic_id.name + '-' + str(penugasan.account_id.id): thp * penugasan.persen / 100
                        })
        if list_data:
            counter = collections.Counter()
            for d in list_data:
                counter.update(d)

            result = dict(counter)
            invoice_line_ids = []
            for r in result:

                spl = r.split('-')
                kode_proyek = spl[0]
                coa = spl[1]
                amount = result[r]

                invoice_line_ids.append([0, 0, {
                    'name': "Kode Proyek: " + kode_proyek,
                    'account_id': coa,
                    'price_unit': amount,
                    'quantity': 1.0,
                }])
            no_vendor = self.env['res.partner'].search([('id', '=', 15501)])
            # if no_vendor:
            #     ar = no_vendor.property_account_receivable_id.id
            # else:
            #     ar = self.env['ir.property'].with_context(force_company=self.env.user.company_id.id).get('property_account_receivable_id', 'res.partner')
            #     ar = ar.id
            invoice = self.env['account.invoice'].create({
                'name': self.name,
                'origin': self.name,
                'type': 'in_invoice',
                'reference': self.name,
                # 'account_id': ar,
                'partner_id': no_vendor.id if no_vendor else 3,
                'invoice_line_ids': invoice_line_ids,
            })
            self.invoice_id = invoice.id


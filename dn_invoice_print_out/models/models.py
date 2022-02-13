# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class dn_invoice_print_out(models.Model):
#     _name = 'dn_invoice_print_out.dn_invoice_print_out'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
# -*- coding: utf-8 -*-
from odoo import http

# class DnInvoicePrintOut(http.Controller):
#     @http.route('/dn_invoice_print_out/dn_invoice_print_out/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dn_invoice_print_out/dn_invoice_print_out/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dn_invoice_print_out.listing', {
#             'root': '/dn_invoice_print_out/dn_invoice_print_out',
#             'objects': http.request.env['dn_invoice_print_out.dn_invoice_print_out'].search([]),
#         })

#     @http.route('/dn_invoice_print_out/dn_invoice_print_out/objects/<model("dn_invoice_print_out.dn_invoice_print_out"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dn_invoice_print_out.object', {
#             'object': obj
#         })
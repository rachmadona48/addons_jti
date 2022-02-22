# -*- coding: utf-8 -*-
from odoo import http

# class DnHkPayslipBatch(http.Controller):
#     @http.route('/dn_hk_payslip_batch/dn_hk_payslip_batch/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dn_hk_payslip_batch/dn_hk_payslip_batch/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dn_hk_payslip_batch.listing', {
#             'root': '/dn_hk_payslip_batch/dn_hk_payslip_batch',
#             'objects': http.request.env['dn_hk_payslip_batch.dn_hk_payslip_batch'].search([]),
#         })

#     @http.route('/dn_hk_payslip_batch/dn_hk_payslip_batch/objects/<model("dn_hk_payslip_batch.dn_hk_payslip_batch"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dn_hk_payslip_batch.object', {
#             'object': obj
#         })
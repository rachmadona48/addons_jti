# -*- coding: utf-8 -*-
from odoo import http

# class HkPayslipBatch(http.Controller):
#     @http.route('/hk_payslip_batch/hk_payslip_batch/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hk_payslip_batch/hk_payslip_batch/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hk_payslip_batch.listing', {
#             'root': '/hk_payslip_batch/hk_payslip_batch',
#             'objects': http.request.env['hk_payslip_batch.hk_payslip_batch'].search([]),
#         })

#     @http.route('/hk_payslip_batch/hk_payslip_batch/objects/<model("hk_payslip_batch.hk_payslip_batch"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hk_payslip_batch.object', {
#             'object': obj
#         })
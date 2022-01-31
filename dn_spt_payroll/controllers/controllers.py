# -*- coding: utf-8 -*-
from odoo import http

# class DnSptPayroll(http.Controller):
#     @http.route('/dn_spt_payroll/dn_spt_payroll/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dn_spt_payroll/dn_spt_payroll/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dn_spt_payroll.listing', {
#             'root': '/dn_spt_payroll/dn_spt_payroll',
#             'objects': http.request.env['dn_spt_payroll.dn_spt_payroll'].search([]),
#         })

#     @http.route('/dn_spt_payroll/dn_spt_payroll/objects/<model("dn_spt_payroll.dn_spt_payroll"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dn_spt_payroll.object', {
#             'object': obj
#         })
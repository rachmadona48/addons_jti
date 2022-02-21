# -*- coding: utf-8 -*-
from odoo import http

# class DnEmployee(http.Controller):
#     @http.route('/dn_employee/dn_employee/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dn_employee/dn_employee/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dn_employee.listing', {
#             'root': '/dn_employee/dn_employee',
#             'objects': http.request.env['dn_employee.dn_employee'].search([]),
#         })

#     @http.route('/dn_employee/dn_employee/objects/<model("dn_employee.dn_employee"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dn_employee.object', {
#             'object': obj
#         })
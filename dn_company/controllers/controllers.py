# -*- coding: utf-8 -*-
from odoo import http

# class DnCompany(http.Controller):
#     @http.route('/dn_company/dn_company/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dn_company/dn_company/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dn_company.listing', {
#             'root': '/dn_company/dn_company',
#             'objects': http.request.env['dn_company.dn_company'].search([]),
#         })

#     @http.route('/dn_company/dn_company/objects/<model("dn_company.dn_company"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dn_company.object', {
#             'object': obj
#         })
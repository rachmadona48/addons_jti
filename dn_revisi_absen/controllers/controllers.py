# -*- coding: utf-8 -*-
from odoo import http

# class DnModuleName(http.Controller):
#     @http.route('/dn_module_name/dn_module_name/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dn_module_name/dn_module_name/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dn_module_name.listing', {
#             'root': '/dn_module_name/dn_module_name',
#             'objects': http.request.env['dn_module_name.dn_module_name'].search([]),
#         })

#     @http.route('/dn_module_name/dn_module_name/objects/<model("dn_module_name.dn_module_name"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dn_module_name.object', {
#             'object': obj
#         })
# -*- coding: utf-8 -*-
from odoo import http

# class DnResign(http.Controller):
#     @http.route('/dn_resign/dn_resign/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dn_resign/dn_resign/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dn_resign.listing', {
#             'root': '/dn_resign/dn_resign',
#             'objects': http.request.env['dn_resign.dn_resign'].search([]),
#         })

#     @http.route('/dn_resign/dn_resign/objects/<model("dn_resign.dn_resign"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dn_resign.object', {
#             'object': obj
#         })
# -*- coding: utf-8 -*-
from odoo import http

# class UcTask(http.Controller):
#     @http.route('/uc_task/uc_task/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/uc_task/uc_task/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('uc_task.listing', {
#             'root': '/uc_task/uc_task',
#             'objects': http.request.env['uc_task.uc_task'].search([]),
#         })

#     @http.route('/uc_task/uc_task/objects/<model("uc_task.uc_task"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('uc_task.object', {
#             'object': obj
#         })
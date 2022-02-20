# -*- coding: utf-8 -*-
from odoo import http

# class RdTaskNew(http.Controller):
#     @http.route('/rd_task_new/rd_task_new/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rd_task_new/rd_task_new/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rd_task_new.listing', {
#             'root': '/rd_task_new/rd_task_new',
#             'objects': http.request.env['rd_task_new.rd_task_new'].search([]),
#         })

#     @http.route('/rd_task_new/rd_task_new/objects/<model("rd_task_new.rd_task_new"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rd_task_new.object', {
#             'object': obj
#         })
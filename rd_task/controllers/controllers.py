# -*- coding: utf-8 -*-
from odoo import http

# class RdTask(http.Controller):
#     @http.route('/rd_task/rd_task/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rd_task/rd_task/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rd_task.listing', {
#             'root': '/rd_task/rd_task',
#             'objects': http.request.env['rd_task.rd_task'].search([]),
#         })

#     @http.route('/rd_task/rd_task/objects/<model("rd_task.rd_task"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rd_task.object', {
#             'object': obj
#         })
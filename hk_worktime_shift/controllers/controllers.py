# -*- coding: utf-8 -*-
from odoo import http

# class HkWorktimeShift(http.Controller):
#     @http.route('/hk_worktime_shift/hk_worktime_shift/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hk_worktime_shift/hk_worktime_shift/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hk_worktime_shift.listing', {
#             'root': '/hk_worktime_shift/hk_worktime_shift',
#             'objects': http.request.env['hk_worktime_shift.hk_worktime_shift'].search([]),
#         })

#     @http.route('/hk_worktime_shift/hk_worktime_shift/objects/<model("hk_worktime_shift.hk_worktime_shift"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hk_worktime_shift.object', {
#             'object': obj
#         })
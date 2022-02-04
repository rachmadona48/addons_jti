# -*- coding: utf-8 -*-
from odoo import http

# class RdVoucerPayment(http.Controller):
#     @http.route('/rd_voucer_payment/rd_voucer_payment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rd_voucer_payment/rd_voucer_payment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rd_voucer_payment.listing', {
#             'root': '/rd_voucer_payment/rd_voucer_payment',
#             'objects': http.request.env['rd_voucer_payment.rd_voucer_payment'].search([]),
#         })

#     @http.route('/rd_voucer_payment/rd_voucer_payment/objects/<model("rd_voucer_payment.rd_voucer_payment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rd_voucer_payment.object', {
#             'object': obj
#         })
# -*- coding: utf-8 -*-

import json
import re
import uuid
from functools import partial

from lxml import etree
from dateutil.relativedelta import relativedelta
from werkzeug.urls import url_encode

from odoo import api, exceptions, fields, models, _
from odoo.tools import float_is_zero, float_compare, pycompat
from odoo.tools.misc import formatLang

from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from odoo.http import request



class dn_AccountInvoice(models.Model):
    _inherit = "account.invoice"

    bank_id = fields.Many2one('res.partner.bank', string='Company Bank Account',
        readonly=True, states={'draft': [('readonly', False)]})
    no_per_pembayaran = fields.Char(string='No Permohonan Pembayaran',readonly=True)

    @api.multi
    def action_invoice_open(self):
        res = super(dn_AccountInvoice, self).action_invoice_open()
        for dt in self:
            if dt.type == 'out_invoice':
                dt.no_per_pembayaran = self.env['ir.sequence'].next_by_code('permohonan.pembayaran')
        return res

    def _get_label(self):
        # print(self.id,' id nya =========================')
        ail = request.env['account.invoice.line'].sudo().search([('invoice_id', '=', int(self.id))],order='id asc', limit=1)
       
        return {
            'label': ail.name,
        }
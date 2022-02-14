# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class ExitRequest(models.Model):
    _inherit = 'exit.request'

    @api.onchange('req_date')
    def onchange_req_date(self):
        if self.req_date:
            req_date = fields.Date.from_string(self.req_date)
            self.last_date = req_date + relativedelta(months=1)
        else:
            self.last_date = None


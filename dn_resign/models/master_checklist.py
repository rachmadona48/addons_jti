# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class MasterChecklist(models.Model):
    _inherit = 'checklist.information'

    type_transaksi = fields.Selection([('resign', "Resign"),
                              ('pensiun', "Pensiun"),
                              ('pensiun_dplk', "Pensiun DPLK Manulife")], default='resign')
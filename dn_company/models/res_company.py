# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
import calendar
import time
from dateutil.relativedelta import relativedelta

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT
from odoo.tools.float_utils import float_round, float_is_zero


class DN_ResCompany(models.Model):
    _inherit = "res.company"

    def _get_text_overdue_msg(self):
        code = self.env['ir.sequence'].next_by_code('overdue.message')
        self.overdue_msg='''Dear Sir/Madam,

Number : '''+code+'''
Our records indicate that some payments on your account are still due. Please find details below.
If the amount has already been paid, please disregard this notice. Otherwise, please forward us the total amount stated below.
If you have any queries regarding your account, Please contact us.

Thank you in advance for your cooperation.
Best Regards,
        '''

    overdue_msg = fields.Text(string='Overdue Payments Message', translate=True,compute='_get_text_overdue_msg')
#     overdue_msg2 = fields.Text(string='Overdue Payments Message', translate=True,
#         default=lambda s: _('''Dear Sir/Madam 3,

# Our records indicate that some payments on your account are still due. Please find details below.
# If the amount has already been paid, please disregard this notice. Otherwise, please forward us the total amount stated below.
# If you have any queries regarding your account, Please contact us.

# Thank you in advance for your cooperation.
# Best Regards,'''))
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class RdHolidaysType(models.Model):
    _inherit = "hr.holidays.status"
    
    gender = fields.Selection(selection=[('male', 'Male'),('female', 'Female')],string='Jenis Kelamin',
                                   required=False)
    status_karyawan = fields.Selection(selection=[('KONTRAK OFFICE', 'KONTRAK OFFICE'),
                                                  ('TETAP', 'TETAP'),
                                                  ('MAGANG', 'MAGANG'),
                                                  ('OUTSOURCING', 'OUTSOURCING'),
                                                  ('PROYEK LANGSUNG', 'PROYEK LANGSUNG'),],string='Status Karyawan',
                                                     required=False)
    marital = fields.Selection(selection=[('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced')],
                                    string='Status', required=False)
    joining_date = fields.Date(string='Joining Date')
    line_hr_leave = fields.One2many(comodel_name='line.hr.employee.leave', inverse_name='hr_hr_holidays_status_id',
                                ondelete='set null')
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InheritResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    analytic_id = fields.Many2one(comodel_name='account.analytic.account', string="Project Code")


class InheritResourceCalendarAttendance(models.Model):
    _inherit = 'resource.calendar.attendance'

    code = fields.Char("Code")

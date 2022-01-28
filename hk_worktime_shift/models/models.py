# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Shifting(models.Model):
    _name = 'resource.calendar.shifting'

    name = fields.Char("Name")
    analytic_id = fields.Many2one(comodel_name='account.analytic.account', string="Project Code")
    resource_calendar_id = fields.Many2one(comodel_name='resource.calendar', string="Working Schedule")
    date_from = fields.Date("Date From")
    date_to = fields.Date("Date To")
    is_shift = fields.Boolean("Shift?")
    is_request = fields.Boolean("Request?")
    employee_line = fields.One2many(comodel_name='resource.calendar.shifting.employee', inverse_name='shifting_id',
                                    string="Employees")


class ShiftingEmployee(models.Model):
    _name = 'resource.calendar.shifting.employee'
    _rec_name = 'employee_id'

    shifting_id = fields.Many2one(comodel_name='resource.calendar.shifting', string='Shifting')
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee')
    schedule_line = fields.One2many(comodel_name='resource.calendar.shifting.employee.schedule',
                                    inverse_name='shifting_employee_id', string="Schedule")

    @api.multi
    def open_schedule(self):
        form_id = self.env.ref('hk_worktime_shift.hr_schedule_shifting_employee_view_form')

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'resource.calendar.shifting.employee',
            'view_id': form_id.id,
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }


class ShiftingEmployeeSchedule(models.Model):
    _name = 'resource.calendar.shifting.employee.schedule'
    _rec_name = 'shifting_employee_id'

    shifting_employee_id = fields.Many2one(comodel_name='resource.calendar.shifting.employee')
    date = fields.Date("Date")
    attendance_id = fields.Many2one(comodel_name='resource.calendar.attendance', string="Attendance")

    @api.onchange('shifting_employee_id')
    def onchange_shifting_employee_id(self):
        domain = []
        if self.shifting_employee_id:
            if self.shifting_employee_id.shifting_id.resource_calendar_id:
                return {'domain':
                            {'attendance_id':
                                 [('id', 'in', [x.id for x in
                                                self.shifting_employee_id.shifting_id.resource_calendar_id.attendance_ids])]}}

        return domain

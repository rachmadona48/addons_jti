# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Shifting(models.Model):
    _name = 'resource.calendar.shifting'

    name = fields.Char("Name")
    analytic_id = fields.Many2one(comodel_name='account.analytic.account', string="Project Code")
    resource_calendar_id = fields.Many2one(comodel_name='resource.calendar', string="Working Schedule")
    resource_calendar_to_id = fields.Many2one(comodel_name='resource.calendar', string="Working Schedule To Be Set")
    resource_calendar_after_id = fields.Many2one(comodel_name='resource.calendar', string="Working Schedule After")
    date_from = fields.Date("Date From")
    date_to = fields.Date("Date To")
    is_shift = fields.Boolean("Shift?")
    is_request = fields.Boolean("Request?")
    is_executed = fields.Boolean("Executed?")
    employee_line = fields.One2many(comodel_name='resource.calendar.shifting.employee', inverse_name='shifting_id',
                                    string="Employees")

    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed')], default='draft', copy=False)

    @api.onchange('analytic_id')
    def onchange_analytic_id(self):
        self.resource_calendar_id = False
        if self.employee_line:
            self.employee_line.schedule_line = None

    @api.multi
    def act_confirm(self):
        self.state = 'confirm'

    @api.multi
    def act_set_to_draft(self):
        self.state = 'draft'

    @api.multi
    def act_execute(self):
        if not self.is_executed:
            res_id = self.resource_calendar_to_id.id
            self.is_executed = True
        else:
            res_id = self.resource_calendar_after_id.id
        # query = ("""update hr_employee set resource_calendar_id = %s where som_nonsom = 'NON SOM'""" % ())
        # self.cr.execute(query)
        emps = self.env['hr.employee'].search([('som_nonsom', '=', 'NON SOM')])
        for emp in emps:
            emp.resource_calendar_id = res_id

class ShiftingEmployee(models.Model):
    _name = 'resource.calendar.shifting.employee'
    _rec_name = 'employee_id'

    shifting_id = fields.Many2one(comodel_name='resource.calendar.shifting', ondelete='cascade', string='Shifting')
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

    shifting_employee_id = fields.Many2one(comodel_name='resource.calendar.shifting.employee', ondelete='cascade')
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

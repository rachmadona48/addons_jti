# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models,_
from odoo.exceptions import UserError
from odoo.tools import datetime
    
class RdHrEmployee(models.Model):
    _inherit = "hr.employee"  
    
    rd_line_hr = fields.One2many(comodel_name='line.hr.employee.leave', inverse_name='employee_id_leave')

    @api.model
    def create(self, values):
        leave = self.env["hr.holidays.status"].sudo().search(['|','|','|',("gender","=",values['gender']),("status_karyawan","=",values['status_karyawan']),("marital","=",values['marital']),("agama","=",values['agama'])])
        
        listt = []
        for eq in leave:
            line = {'name':eq.id}
            listt.append([0,0,line])
        values.update({'rd_line_hr':listt})
        
        return super(RdHrEmployee, self).create(values)  

    @api.multi
    def create_leave_allocation(self):
        for dt in self:
            for leave_line in dt.rd_line_hr:
                exist_allocation = self.env["hr.holidays"].sudo().search([("employee_id","=",int(dt.id)),("holiday_status_id","=",int(leave_line.name.id))])
                if len(exist_allocation) <= 0:
                    if leave_line.number_of_days_temp <= 0:
                        raise UserError(_('Duration is zero!!'))
                    else:
                        new_allocation = self.env['hr.holidays'].sudo().create({
                            'type': 'add',
                            'employee_id': dt.id,
                            'holiday_status_id': leave_line.name.id,
                            'holiday_type': 'employee',
                            'nrp': dt.nrp,
                            'date_from':False,
                            'date_to':False,
                            'number_of_days_temp': leave_line.number_of_days_temp,
                            'department_id': dt.department_id.id,
                            'departments_id': dt.departments_id.id,
                            'branch_id': dt.branch_id.id,
                            'state': 'validate',
                        })
        
            tree_view = {
                'name': _('Leaves Allocation'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'view_id': False,
                'res_model': 'hr.holidays',
                'type': 'ir.actions.act_window',
                'domain': [('employee_id', '=', dt.id)],
                'target': 'main',
            }
            return tree_view

    
class rd_LineRdHrEmployee(models.Model):
    _name = "line.hr.employee.leave"
    
    hr_hr_holidays_status_id = fields.Many2one('hr.holidays.status')
    employee_id_leave = fields.Many2one('hr.employee')
    name = fields.Many2one('hr.holidays.status','Leave Type')
    number_of_days_temp = fields.Float(String='Duration')
    
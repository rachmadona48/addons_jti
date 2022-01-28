# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.tools import datetime
    
class RdHrEmployee(models.Model):
    _inherit = "hr.employee"  
    
    rd_line_hr = fields.One2many(comodel_name='line.hr.employee.leave', inverse_name='employee_id',
                                ondelete='set null')
    
class LineRdHrEmployee(models.Model):
    _name = "line.hr.employee.leave"
    
    hr_hr_holidays_status_id = fields.Many2one('hr.holidays.status')
    employee_id = fields.Many2one('hr.employee')
    name = fields.Many2one('hr.holidays.status','Leave Type')
    
#     @api.onchange('many2one_field')
#     def _onchange_many2one_field(self):
#             self.one2many_record_field = self.env['One2manyFieldModelName'].search([('One2manyFieldName', '=', self.many2one_field)])

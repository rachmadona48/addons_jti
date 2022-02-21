from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, Warning

class dn_HREmployee(models.Model):
    _inherit = 'hr.employee'
    
    @api.onchange('usia_pensiun','age')
    def update_i_bpjs_kes(self):
        contract = self.env['hr.contract'].sudo().search([('employee_id', '=', int(self._origin.id))])
        if len(contract)>=1:
            for cnt in contract:
                if int(self.usia_pensiun) <= int(self.age):
                    cnt.write({'iuran_bpjs_pen':True})
                else:
                    cnt.write({'iuran_bpjs_pen':False})

class Contract(models.Model):
    _inherit = 'hr.contract'

    iuran_bpjs_pen = fields.Boolean('Iuran BPJS Pensiun.')
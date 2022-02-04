# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning, ValidationError

class HrPenugasan(models.Model):
    _inherit = 'hr.penugasan'

    @api.multi
    def validate_dept(self):
        vals = super(HrPenugasan, self).validate_dept()
        contract = self.env['hr.contract'].search([('employee_id','=', self.employee_id.id),('state','=','open')], limit=1)
        if contract:
            contract.penugasan_id = self.id
        else:
            raise UserError(_('Contract %s not found.' % self.employee_id.name))
        return vals

class NewRangkapPenugasan(models.Model):
    _inherit = 'new.rangkap.tugas'

    account_id = fields.Many2one('account.account', string='Account')
    account_id2 = fields.Many2one('account.account', string='Account')

    @api.onchange('account_id')
    def onchange_account_id(self):
        for r in self:
            if r.account_id:
                r.account_id2 = r.account_id.id
            if not r.account_id:
                r.account_id2 = False

class HrContract(models.Model):
    _inherit = 'hr.contract'

    penugasan_id = fields.Many2one('hr.penugasan')

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    penugasan_id = fields.Many2one('hr.penugasan')

    @api.multi
    def action_payslip_done(self):
        vals = super(HrPayslip, self).action_payslip_done()
        if self.contract_id.penugasan_id:
            if not self.penugasan_id:
                self.penugasan_id = self.contract_id.penugasan_id.id
        return vals

    @api.multi
    def compute_sheet(self):
        vals = super(HrPayslip, self).compute_sheet()
        for x in self:
            if x.contract_id.penugasan_id:
                if not x.penugasan_id:
                    x.penugasan_id = x.contract_id.penugasan_id.id
        return vals

# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError, AccessError
from dateutil.relativedelta import relativedelta


class MasterChecklist(models.Model):
    # _inherit = 'checklist.information'
    _inherit = 'exit.checklist'

    type_transaksi = fields.Selection([('resign', "Resign"),
                              ('pensiun', "Pensiun"),
                              ('pensiun_dplk', "Pensiun DPLK Manulife")],'Type', default='resign')

class dn_exit_request(models.Model):
    _inherit = "exit.request"

    type_transaksi = fields.Selection([('resign', "Resign"),
                              ('pensiun', "Pensiun"),
                              ('pensiun_dplk', "Pensiun DPLK Manulife")],'Type', default='resign')
    checklist_ids = fields.Many2many('checklist.information','rel_exit_request_id',string="Checklist")

    def action_confirm(self):
        for dt in self:
            for cek in dt.checklist_ids:
                if cek.state != 'approved':
                    raise UserError(_('Checklist state must be Approve'))
                if cek.type_transaksi != dt.type_transaksi:
                    raise UserError(_('Checklist type is not match'))

        return super(dn_exit_request, self).action_confirm()

    def action_approve_dept(self):
        for dt in self:
            for cek in dt.checklist_ids:
                if cek.state != 'approved':
                    raise UserError(_('Checklist state must be Approve'))
                if cek.type_transaksi != dt.type_transaksi:
                    raise UserError(_('Checklist type is not match'))

        return super(dn_exit_request, self).action_approve_dept()

    def action_approve_hr(self):
        for dt in self:
            for cek in dt.checklist_ids:
                if cek.state != 'approved':
                    raise UserError(_('Checklist state must be Approve'))
                if cek.type_transaksi != dt.type_transaksi:
                    raise UserError(_('Checklist type is not match'))
            dt.employee_id.active = False
        # exit()
        return super(dn_exit_request, self).action_approve_hr()

    def action_approve_gen(self):
        for dt in self:
            for cek in dt.checklist_ids:
                if cek.state != 'approved':
                    raise UserError(_('Checklist state must be Approve'))
                if cek.type_transaksi != dt.type_transaksi:
                    raise UserError(_('Checklist type is not match'))

        return super(dn_exit_request, self).action_approve_gen()

class dn_exit_checklist(models.Model):
    _inherit = "checklist.information"

    type_transaksi = fields.Selection([('resign', "Resign"),
                              ('pensiun', "Pensiun"),
                              ('pensiun_dplk', "Pensiun DPLK Manulife")],'Type', required=True,store=True)

    @api.onchange('type_transaksi')
    def _type_transaksi_onchange(self):
        res = {}
        res['domain']={'checklist_id':[('type_transaksi', '=', self.type_transaksi)]}
        return res


    checklist_id = fields.Many2one('exit.checklist',string="Checklist")

# class dn_checklist_lines(models.Model):
#     _inherit = "exit.checklist.line"

#     checklist_id = fields.Many2one('exit.checklist',domain=[('type_transaksi','=',self.checklist_info_id.checklist_id.type_transaksi)])
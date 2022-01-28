# -*- coding: utf-8 -*-

from odoo import models, fields, api

class dn_module_name(models.Model):
    _name = 'dn.revisi.absen'

    name = fields.Char('Name')
    sequence = fields.Char('Sequence')
    state = fields.Selection([('draft', "Draft"),
                              ('submitted', "Submitted"),
                              ('approved', "Approved"),
                              ('close', 'Closed'),
                              ('cancel', 'Cancel')
                              ], track_visibility='onchange', default='draft')
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    employee_ids = fields.Many2many('hr.employee', string='Employee')
    revisi_line_ids = fields.One2many('dn.revisi.absen.revision.line','revisi_absen_id', string='Line')

    @api.multi
    def create_button_cek(self, aline):
        revisi_line_ids = {
            'revisi_absen_id': self.id,
            'datetime': aline.name,
            'date': aline.date,
            'attendance_status': aline.attendance_status,
            'employee_id': aline.employee_id.id,
            'attendance_id': aline.id,
            'backup_datetime': aline.name,
            'backup_date': aline.date,
            'backup_attendance_status': aline.attendance_status,
        }
        return revisi_line_ids

    @api.multi
    def button_cek(self):
        for r in self:
            if r.revisi_line_ids:
                r.revisi_line_ids.unlink()
            draft_attendance = self.env['hr.draft.attendance']
            domain = [('employee_id', 'in', r.employee_ids.ids),('date','<=', r.date_to),('date','>=', r.date_from)]
            stock_move = draft_attendance.search(domain)
            new_lines = self.env['dn.revisi.absen.revision.line']
            for line in stock_move:
                data = r.create_button_cek(line)
                new_line = new_lines.new(data)
                new_lines += new_line
            r.revisi_line_ids += new_lines


    @api.multi
    def action_cancel(self):
        for r in self:
            if r.state == 'close':
                for line in r.revisi_line_ids:
                    if line.editable:
                        line.write({'name': line.backup_datetime,
                                    'date': line.backup_date,
                                    'attendance_status': line.backup_attendance_status,
                                    'editable': False, })
                r.state = 'cancel'
            else:
                r.state = 'cancel'

    @api.multi
    def action_set_to_draft(self):
        for r in self:
            r.state = 'draft'

    @api.multi
    def action_submit(self):
        for r in self:
            r.state = 'approved'

    @api.multi
    def action_validate(self):
        for r in self:
            for line in r.revisi_line_ids:
                if line.editable:
                    line.write({'name': line.datetime,
                                'date': line.date,
                                'attendance_status': line.attendance_status,
                                'editable': True, })
            r.state = 'close'

class dn_module_name_revision(models.Model):
    _name = 'dn.revisi.absen.revision.line'

    name = fields.Char('Name')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    datetime = fields.Datetime('Date and Time')
    date = fields.Date('Date')
    editable = fields.Boolean('Edited')
    attendance_status = fields.Selection([('sign_in', "Sign In"), ('sign_out', "Sign Out"), ('sign_none', "None"), ])
    revisi_absen_id = fields.Many2one('dn.revisi.absen', string='Revisi Id')
    attendance_id = fields.Many2one('hr.draft.attendance', string='Attendance ID')

    backup_datetime = fields.Datetime('Date and Time')
    backup_date = fields.Date('Date')
    backup_attendance_status = fields.Selection([('sign_in', "Sign In"), ('sign_out', "Sign Out"), ('sign_none', "None"), ])

    @api.onchange('datetime')
    def onchange_datetime(self):
        for r in self:
            if r.datetime:
                r.date = r.datetime
            if not r.editable:
                r.editable = True

    @api.onchange('date')
    def onchange_date(self):
        for r in self:
            if not r.editable:
                r.editable = True

    @api.onchange('attendance_status')
    def onchange_attendance_status(self):
        for r in self:
            if not r.editable:
                r.editable = True

class Attendance(models.Model):
    _inherit = 'hr.draft.attendance'

    editable = fields.Boolean('Editable')
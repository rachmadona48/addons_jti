# -*- coding: utf-8 -*-

from odoo import models, fields, api

class dn_module_name(models.Model):
    _name = 'dn.revisi.absen'

    @api.model
    def create(self, vals):
        name = self.env['ir.sequence'].next_by_code('rev.abs.seq')
        vals.update({
            'name': name
            })
        return super(dn_module_name, self).create(vals)

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
    keterangan = fields.Char('Keterangan')

    @api.multi
    def create_button_cek(self, aline):
        revisi_line_ids = {
            'revisi_absen_id': self.id,
            'nrp': aline.nrp,
            'day': aline.day,
            'check_in': aline.check_in,
            'check_out': aline.check_out,
            'employee_id': aline.employee_id.id,
            'attendance_id': aline.id,
            'backup_datetime_in': aline.check_in,
            'backup_datetime_out': aline.check_out,
            'backup_date': aline.day,
        }
        return revisi_line_ids

    @api.multi
    def button_cek(self):
        for r in self:
            if r.revisi_line_ids:
                r.revisi_line_ids.unlink()
            draft_attendance = self.env['hr.attendance']
            domain = [('employee_id', 'in', r.employee_ids.ids),('day','<=', r.date_to),('day','>=', r.date_from)]
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
                        line.attendance_id.write({
                                    'day': line.backup_date,
                                    'check_in': line.backup_datetime_in,
                                    'check_out': line.backup_datetime_out,
                                    'editable': False,
                                    'keterangan': r.keterangan, })
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
                    line.attendance_id.write({
                                'day': line.day,
                                'check_in': line.check_in,
                                'check_out': line.check_out,
                                'editable': True,})
            r.state = 'close'

class dn_module_name_revision(models.Model):
    _name = 'dn.revisi.absen.revision.line'

    name = fields.Char('Name')
    nrp = fields.Char('NRP')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    datetime = fields.Datetime('Date and Time')
    check_in = fields.Datetime('Check In')
    check_out = fields.Datetime('Check Out')
    day = fields.Date('Date')
    editable = fields.Boolean('Edited')
    attendance_status = fields.Selection([('sign_in', "Sign In"), ('sign_out', "Sign Out"), ('sign_none', "None"), ])
    revisi_absen_id = fields.Many2one('dn.revisi.absen', string='Revisi Id')
    attendance_id = fields.Many2one('hr.attendance', string=' ')
    attendance_id2 = fields.Many2one('hr.attendance.base', string='Attendance ID')

    backup_datetime_in = fields.Datetime('Backup Check In')
    backup_datetime_out = fields.Datetime('Backup Check Out')
    backup_date = fields.Date('Back up Date')
    backup_attendance_status = fields.Selection([('sign_in', "Sign In"), ('sign_out', "Sign Out"), ('sign_none', "None"), ])


    @api.onchange('day','check_in','check_out')
    def onchange_date(self):
        for r in self:
            if not r.editable:
                r.editable = True

# class AttendanceBase(models.Model):
#     _inherit = 'hr.attendance.base'
#
#     editable = fields.Boolean('Editable')
#     keterangan = fields.Char('Keterangan')

class Attendance(models.Model):
    _inherit = 'hr.attendance'

    editable = fields.Boolean('Editable')
    keterangan = fields.Char('Keterangan')

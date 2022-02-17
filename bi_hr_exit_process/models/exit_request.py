# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
import datetime
from odoo.exceptions import UserError


class exit_request(models.Model):
    _name = "exit.request"
    

    name = fields.Char(string ="Name",related="employee_id.name",readonly=True)
    employee_id =  fields.Many2one('hr.employee',string="Employee" ,required=True)
    req_date = fields.Date(string="Request Date",required=True)
    last_date = fields.Date(string="Last Day Of Work",required=True)
    partner_id= fields.Many2one('res.partner',string="Contact",required=True)
    department_manager_id = fields.Many2one('res.users',string="Department Manager")
    department_id = fields.Many2one('hr.department',string="Department")
    job_title_id = fields.Many2one('hr.job',string="Job Title",required=True)
    user_id = fields.Many2one('res.users',string="User",required=True)
    state = fields.Selection([('draft','Draft'),('confirm','Confirmed'),('approved_dept','Approved By Dept Manager'),('approved_hr','Approved By HR Manager'),('approved_gen','Approved By General Manager'),('done','Done')],string='State',default='draft')
    #interview_id = fields.Many2one('')
    confirmed_by_id = fields.Many2one('res.users',string="Confirmed By",readonly=True)
    approved_by_dept_manager_id = fields.Many2one('res.users',string="Approved By Department Manager",readonly=True)
    approved_by_hr_manager_id = fields.Many2one('res.users',string="Approved By HR Manager",readonly=True)
    approved_by_hr_genral_id = fields.Many2one('res.users',string="Approved By General Manager",readonly=True)

    confirm_date = fields.Date(string="Confirm Date(Employee)",readonly=True)
    approve_date_dept_manager = fields.Date(string="Approved Date(Department Manager)",readonly=True)
    approve_date_hr_manager = fields.Date(string="Approved Date(HR Manager)",readonly=True)
    approve_date_gen_manager = fields.Date(string="Approved Date(General Manager)",readonly=True)
    # checklist_ids = fields.Many2many('checklist.information','rel_exit_request_id',string="Checklist",domain=[('state','=','approved')])
    checklist_ids = fields.Many2many('checklist.information','rel_exit_request_id',string="Checklist")
    reasone = fields.Text(string="Reason For Exit")
    notes = fields.Text(string="Notes")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")



    survey_id = fields.Many2one('survey.survey', related='job_title_id.survey_id', string="Interview")
    response_id = fields.Many2one('survey.user_input', "Response", ondelete="set null", oldname="response")



    @api.constrains('req_date','last_date')
    def check_end_date(self):
        if self.last_date < self.req_date :
            raise Warning(_('Last Day Of Work must br after the Request Date!!'))




    @api.onchange('employee_id')
    def onchange_employee(self):

        self.department_id = self.employee_id.department_id.id
        self.job_title_id = self.employee_id.job_id.id
        

    @api.multi
    def action_makeMeeting(self):
        """ This opens Meeting's calendar view to schedule meeting on current applicant
            @return: Dictionary value for created Meeting view
        """
        self.ensure_one()
        partners = self.partner_id | self.user_id.partner_id | self.department_id.manager_id.user_id.partner_id

        category = self.env.ref('hr_recruitment.categ_meet_interview')
        res = self.env['ir.actions.act_window'].for_xml_id('calendar', 'action_calendar_event')
        res['context'] = {
            'search_default_partner_ids': self.partner_id.name,
            'default_partner_ids': partners.ids,
            'default_user_id': self.env.uid,
            'default_name': self.name,
            'default_categ_ids': category and [category.id] or False,
        }
        return res


    @api.multi
    def action_start_survey(self):
        self.ensure_one()
        # create a response and link it to this applicant
        if not self.response_id:
            response = self.env['survey.user_input'].create({'survey_id': self.survey_id.id, 'partner_id': self.partner_id.id})
            self.response_id = response.id
        else:
            response = self.response_id
        # grab the token of the response and start surveying
        return self.survey_id.with_context(survey_token=response.token).action_start_survey()

    @api.multi
    def action_print_survey(self):
        """ If response is available then print this response otherwise print survey form (print template of the survey) """
        self.ensure_one()
        if not self.response_id:
            return self.survey_id.action_print_survey()
        else:
            response = self.response_id
            return self.survey_id.with_context(survey_token=response.token).action_print_survey()




    def action_confirm(self):
        self.write({'state': 'confirm'})
        self.confirm_date = datetime.datetime.now().date()
        self.confirmed_by_id = self.env.user.id
        return

    def action_approve_dept(self):
        self.write({'state': 'approved_dept'})
        self.approve_date_dept_manager = datetime.datetime.now().date()
        self.approved_by_dept_manager_id = self.env.user.id
        return

    def action_approve_hr(self):
        self.write({'state': 'approved_hr'})
        self.approve_date_hr_manager = datetime.datetime.now().date()
        self.approved_by_hr_manager_id = self.env.user.id
        return

    def action_approve_gen(self):
        self.write({'state': 'approved_gen'})
        self.approve_date_gen_manager = datetime.datetime.now().date()
        self.approved_by_hr_genral_id = self.env.user.id
        return

    def action_done(self):
        self.write({'state': 'done'})
        return

class exit_checklist(models.Model):
    _name = "checklist.information"
    _rec_name = "checklist_id"

    checklist_id = fields.Many2one('exit.checklist',string="Checklist")
    responsible_user_id = fields.Many2one('res.users',string="Responsible User")
    remarks = fields.Char('Remarks')
    exit_request_id = fields.Many2one('exit.request')
    
    state = fields.Selection([('new','New'),('confirm','Confirmed'),('approved','Approved')],string='State',default='new')
    checklist_line_ids = fields.One2many('exit.checklist.line','checklist_info_id',string="Checklist Line")

    @api.onchange('checklist_id')
    def onchange_checklist_id(self):
        
        self.responsible_user_id = self.checklist_id.responsible_user_id.id
        self.remarks = self.checklist_id.notes
        self.checklist_line_ids = self.checklist_id.checklist_line_ids.ids
        return

    def action_confirm(self) :
        self.write({'state': 'confirm'})
        return

    def action_approve(self) :
        self.write({'state': 'approved'})
        return

class employee_exit_checklist(models.Model):
    _name = "exit.checklist"

    name = fields.Char(string = "Checklist")
    responsible_user_id = fields.Many2one('res.users',string="Responsible User")
    notes = fields.Char('Notes')
    
    checklist_line_ids = fields.One2many('exit.checklist.line','checklist_id',string="Checklist")

class checklist_lines(models.Model):
    _name = "exit.checklist.line"

    name = fields.Char(string="Name")
    checklist_id = fields.Many2one('exit.checklist')
    checklist_info_id = fields.Many2one('checklist.information')





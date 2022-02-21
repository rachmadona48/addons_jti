from collections import defaultdict
from odoo import models, fields, api, _
from datetime import date, datetime, time, timedelta
from dateutil.relativedelta import relativedelta
from odoo import api, models, _
from odoo.exceptions import UserError
import pytz
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


import math
import xlsxwriter
import base64

class UcWizardKaryawanSOMReport(models.TransientModel):
    _name = 'uc.karyawan.som.wizard'
    _description = "Rekapitulasi Karyawan SOM Wizard"

    from_date = fields.Date('From Date', default=lambda self: fields.Date.to_string(date.today().replace(day=1)),
                            required=True)
    to_date = fields.Date("To Date", default=lambda self: fields.Date.to_string(
        (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()), required=True)
    employee_ids = fields.Many2many('hr.employee', string="Employees")
    filter_status_by = fields.Selection(string='Filter status by',
                                        selection=[('all', 'All')],
                                        default='all')

    xls_file = fields.Binary(string='Download')
    xls_filename = fields.Char(string='File name', size=64)
    xls_state = fields.Selection([('select', 'select'), ('download', 'download')], default="select", string="Status")

    def date_range(self, date_from, date_to):
        lst_date_range = []
        delta = date_to - date_from
        for i in range(delta.days + 1):
            day = date_from + timedelta(days=i)
            lst_date_range.append(day)
        return lst_date_range

    @api.multi
    def print_kary_som_pdf(self):
        return self.env.ref('uc_task.action_report_karyawan_som_id').report_action(self)

    def get_data(self):
        timezone = "Asia/Jakarta"
        if not timezone:
            timezone = "UTC"
        active_tz = pytz.timezone(timezone)

        s_date = datetime.strptime(self.from_date, DEFAULT_SERVER_DATE_FORMAT).date()
        e_date = datetime.strptime(self.to_date, DEFAULT_SERVER_DATE_FORMAT).date()
        delta = e_date - s_date
        day_state_list = []
        list_data = []

        for employee in self.employee_ids:
            daterange = self.date_range(s_date, e_date)
            sch_project = self.env['resource.calendar.shifting.employee'].search ([('employee_id','=',employee.id)])

            for day in daterange:
                sch = self.env['resource.calendar.shifting.employee.schedule'].search ([('date','=',day),
                                                                                        ('shifting_employee_id','in',[s.id for s in sch_project])])
                if sch:
                    list_data.append({
                        'day': day,
                        'masuk': sch.attendance_id.hour_from,
                        'pulang': sch.attendance_id.hour_to

                    })

        return list_data





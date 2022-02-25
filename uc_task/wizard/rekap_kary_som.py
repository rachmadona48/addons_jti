from collections import defaultdict
from odoo import models, fields, api, _
# from datetime import date, datetime, time, timedelta
from datetime import *
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

    def convert_to_float(self, time_att):
        h_m_s = time_att.split(":")
        hours = int(h_m_s[0])
        minutes_1 = float(h_m_s[1])/60.0
        minutes = ("%.2f" % minutes_1)
        return hours+float(minutes)

    def get_data2(self):
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
            list_att = []
            for day in daterange:
                
                sch = self.env['resource.calendar.shifting.employee.schedule'].search ([('date','=',day),
                                                                                        ('shifting_employee_id','in',[s.id for s in sch_project])])
                if sch:

                    self.env.cr.execute("""
                        SELECT id,employee_id,day,
                        to_char((check_in+ interval '25200 second')::time,'HH24:MI') as check_in,
                        to_char((check_out+ interval '25200 second')::time,'HH24:MI') as check_out,
                        to_char((check_in+ interval '25200 second'),'YYYY-MM-DD HH24:MI') as check_in1,
                        to_char((check_out+ interval '25200 second'),'YYYY-MM-DD HH24:MI') as check_out1,
                        check_in as check_in2,
                        check_out as check_out2
                        FROM hr_attendance_base 
                        WHERE employee_id = %s
                        AND day = %s
                    """, (int(employee.id),str(day),))
                    
                    atte = self.env.cr.dictfetchone()

                    if atte == None:
                        at_check_in = ''
                        at_check_out = ''
                        at_dtg_cepat = ''
                        at_dtg_telat = ''
                        at_plg_cepat = ''
                        at_plg_telat = ''
                        at_tt_jamker = ''
                        at_poin = -50
                        at_ket = 'Alpha'

                    else:
                        check_in2 = datetime.strptime(atte['check_in2'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.utc).astimezone(active_tz)
                        check_out2 = datetime.strptime(atte['check_out2'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.utc).astimezone(active_tz)

                        hour_from_time = '{0:02.0f}:{1:02.0f}'.format(*divmod(sch.attendance_id.hour_from * 60, 60))
                        jadwal_masuk = str(day)+' '+str(hour_from_time)
                        jadwal_masuk = datetime.strptime(jadwal_masuk, '%Y-%m-%d %H:%M')
                        check_in1 = datetime.strptime(atte['check_in1'], "%Y-%m-%d %H:%M")

                        hour_to_time = '{0:02.0f}:{1:02.0f}'.format(*divmod(sch.attendance_id.hour_to * 60, 60))
                        jadwal_plg = str(day)+' '+str(hour_to_time)
                        jadwal_plg = datetime.strptime(jadwal_plg, '%Y-%m-%d %H:%M')
                        check_out1 = datetime.strptime(atte['check_out1'], "%Y-%m-%d %H:%M")
                        
                        cek_dt_cepat = jadwal_masuk - check_in1
                        if str(cek_dt_cepat)[0:1] == '0':
                            dtg_cepat = str(cek_dt_cepat)
                        else:
                            dtg_cepat = '0'

                        cek_dt_telat = check_in1 - jadwal_masuk 
                        if str(cek_dt_telat)[0:1] == '0':
                            dtg_telat = str(cek_dt_telat)
                        else:
                            dtg_telat = '0'

                        cek_plg_cepat = jadwal_plg - check_out1
                        if str(cek_plg_cepat)[0:1] == '0':
                            plg_cepat = str(cek_plg_cepat)
                        else:
                            plg_cepat = '0'

                        
                        cek_plg_telat = check_out1 - jadwal_plg
                        if str(cek_plg_telat)[0:1] != '-':
                            plg_telat = str(cek_plg_telat)
                        else:
                            plg_telat = '0'

                        at_tt_jamker = str(check_out1-check_in1)

                        at_check_in = atte['check_in']
                        at_check_out = atte['check_out']
                        at_dtg_cepat = dtg_cepat
                        at_dtg_telat = dtg_telat
                        at_plg_cepat = plg_cepat
                        at_plg_telat = plg_telat
                        at_poin = 0
                        at_ket = 'Hadir'

                    list_att.append({
                        'day': day,
                        'masuk': sch.attendance_id.hour_from,
                        'pulang': sch.attendance_id.hour_to,
                        'check_in': at_check_in,
                        'check_out': at_check_out,
                        'dtg_cepat': at_dtg_cepat,
                        'dtg_telat': at_dtg_telat,
                        'plg_cepat': at_plg_cepat,
                        'plg_telat': at_plg_telat,
                        'tt_jamker': at_tt_jamker,
                        'poin': at_poin,
                        'keterangan': at_ket
                    })

            list_data.append({
                'start_date': self.from_date,
                'end_date': self.to_date,
                'emp_nrp': employee.nrp,
                'employee_name': employee.name,
                'emp_department': employee.department_id.name,
                'list_att': list_att,

            })
            
        return list_data


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
            list_att = []
            for day in daterange:
                sch = self.env['resource.calendar.shifting.employee.schedule'].search ([('date','=',day),
                                                                                        ('shifting_employee_id','in',[s.id for s in sch_project])])
                
                self.env.cr.execute("""
                    SELECT id,employee_id,day,
                    to_char((check_in+ interval '25200 second')::time,'HH24:MI') as check_in,
                    to_char((check_out+ interval '25200 second')::time,'HH24:MI') as check_out
                    FROM hr_attendance_base 
                    WHERE employee_id = %s
                    AND day = %s
                """, (int(employee.id),str(day),))
                
                atte = self.env.cr.dictfetchone()
                # print(atte['id'],' id query 2==================')
                # print(day,' day1=======================')
                # print(atte['day'],' day=======================')
                # print(atte['check_in'],' check_in=======================')
                # print(atte['check_out'],' check_out=======================')
                # check_in_h_m = check_in.strftime("%H:%M")
                if sch:
                    # print(atte['check_in'],' att.check_inatt.check_inatt.check_inatt.check_in')
                    
                    # check_in = datetime.datetime.strptime(att.check_in, '%H:%M')
                    # check_out = datetime.datetime.strptime(att.check_out, '%H:%M')
                    list_data.append({
                        'day': day,
                        'masuk': sch.attendance_id.hour_from,
                        'pulang': sch.attendance_id.hour_to,
                        'check_in': atte['check_in'],
                        'check_out': atte['check_out']

                    })

            # list_data.append({
            #     'emp_nrp': employee.nrp,
            #     'employee_name': employee.name,
            #     'list_att': list_att,

            # })
        print(list_data,' list data')
        # exit()
        return list_data





from odoo import api, fields, models


class rd_holiday_status(models.Model):
    _inherit = "hr.holidays.status"
    
    gender = fields.Selection(selection=[('male', 'Male'),('female', 'Female')],string='Jenis Kelamin',
                                   required=False)
    status_karyawan = fields.Selection(selection=[('KONTRAK OFFICE', 'KONTRAK OFFICE'),
                                                  ('TETAP', 'TETAP'),
                                                  ('MAGANG', 'MAGANG'),
                                                  ('OUTSOURCING', 'OUTSOURCING'),
                                                  ('PROYEK LANGSUNG', 'PROYEK LANGSUNG'),],string='Status Karyawan',
                                                     required=False)
    marital = fields.Selection(selection=[('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced')],
                                    string='Status', required=False)
    month_service = fields.Float(string="Month Of Service",digits=(3,0))
    agama = fields.Selection(selection=[('islam', 'Islam'), ('hindu', 'Hindu'), ('kristen', 'Kristen'),('katolik', 'Katolik'), 
    ('kristen protestan', 'Kristen Protestan'), ('kong hu cu', 'KONG HU CU')],string='Agama')
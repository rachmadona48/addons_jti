# -*- coding: utf-8 -*-
{
    'name': "uc_task",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','mcs_hr_attendance_report'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'wizard/rekap_kary_som.xml',
        'views/views.xml',
        'views/templates.xml',
        'report/rekap_kary_som_pdf.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
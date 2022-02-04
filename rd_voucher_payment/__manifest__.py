# -*- coding: utf-8 -*-
{
    'name': "rd_voucher_payment",

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
    'depends': ['base','account'],

    # always loaded
    'data': [
        'data/report_paperformat.xml',
        'data/data.xml',
        # 'data/res_groups.xml',
        
        'security/ir.model.access.csv',
        #'security/security.xml',
        
        'views/voucher_payment_views.xml',
        'views/invoice_views.xml',
        'views/views.xml',
        'views/templates.xml',
        
        'report/voucher.xml',
        'report/voucher_report_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
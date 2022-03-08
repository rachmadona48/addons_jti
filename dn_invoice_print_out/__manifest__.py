# -*- coding: utf-8 -*-
{
    'name': "dn_invoice_print_out",

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
    'depends': ['base','account','jti_vendor_bill','sale','jti_progress_billing'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/seq_peringatan_satu.xml',
        'views/kwintansi_pembayaran.xml',
        'views/templates.xml',
        'views/vendor_bill.xml',
        'views/account_invoice.xml',
        'views/permohonan_pembayaran.xml',
        'views/peringatan_satu.xml',
        'views/print_peringatan_satu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
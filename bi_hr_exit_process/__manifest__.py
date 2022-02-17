# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.
{
    'name': 'employee Exit Process Management in odoo',
    'version': '11.0.0.1',
    'category': 'Human Resources',
    'summary': 'Employee Exit Process Management',
    'description': """This app allows an organization to handle employee exit process or when employee leaving organization.
   This module allow organization to handle employee exit process or when employee leaving organization.
Available Features:
  * Configure Checklists For Exit Process
  * Employee Exit Request
  * Employee Exit Checklists
  * Print Employee Exit PDF Report.
Notes: Two new groups has been added: 1. Department Manager 2. Genaral Manager. So we have added record rules and ACL which will take care of exit process requests and its workflow!
This apps add below menus: 
  * Employees/Configuration/Configure Checklists
  * Employees/Employee Exit
Employee offboarding
employee dismissal process
Employee termination
Employees resigning
    * Employees/Employee Exit/Employee Exit Checklists
    * Employees/Employee Exit/Exit Requests
hr exit process management 
employee leaving process 
  This app is helpfull for all those organisation who are willing to keep account on employee exit """,    'author': 'BrowseInfo',
    'website': 'http://www.browseinfo.in',
    "price": 10,
    "currency": 'EUR',
    'depends': ['base','hr','hr_recruitment','contacts','survey','hr_recruitment_survey'],
    'data': ['security/ir.model.access.csv',
             'security/groups.xml',
              'views/views_request_exit.xml',
             'views/check_list_views.xml',
             'report/report_views.xml',
             'report/report_exit_request.xml',
              ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'live_test_url':'https://youtu.be/EJkAbmAVwhY',
    "images":["static/description/banner.png"],
}

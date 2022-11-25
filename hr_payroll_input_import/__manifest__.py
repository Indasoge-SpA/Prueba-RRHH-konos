# -*- coding: utf-8 -*-
{
    'name': 'Payroll Input Import from Excel',
    'version': '2.2',
    'description': """
Payroll Input Excel Import.
============================


    -Import From Excel Payroll Inputs

    """,
    'license': 'AGPL-3',
    'category': 'hr',
    'author': 'Konos',
    'website': 'http://konos.cl',
    'depends': [
        'hr_payroll'
    ],
    'data': [
        'views/hr_payroll_input_import.xml',
        'views/hr_payroll_input_menu.xml',
        'security/ir.model.access.csv',
        'wizards/hr_payroll_input_wizard.xml',
    ],

    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

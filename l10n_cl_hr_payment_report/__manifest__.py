# -*- coding: utf-8 -*-
{
    'name': 'Payroll Payment Report',
    'version': '14.0.1.0.0',
    'summary': "Payroll Payment Report",
    'description': "Payroll Payment Report",
    'category': 'Payroll Localization',
    'author': 'Konos',
    'website': 'http://konos.cl',
    'depends': [
                'base',
                'l10n_cl',
                'l10n_cl_hr',
                ],
    'data': [
            'views/wizard_view.xml',
            'security/ir.model.access.csv',
            ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'auto_install': False,
}

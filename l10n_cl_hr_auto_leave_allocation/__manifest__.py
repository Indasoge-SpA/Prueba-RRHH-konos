# -*- coding: utf-8 -*-
{
    'name': "Auto Leave Allocation",

    'summary': """Automatically increment a leave type to the employees""",

    'author': "Konos Soluciones & Servicios",
    'website': "https://www.konos.cl",

    'category': 'Human Resources',
    'version': '13.0.0.0.0',

    'depends': [
        'hr_holidays', 'l10n_cl_hr', 'hr',
    ],

    'data': [
        'views/res_config_settings_views.xml',
    ],

    'demo': [
    ],

    'installable': False,
    'auto_install': False,
    'application': True,
}

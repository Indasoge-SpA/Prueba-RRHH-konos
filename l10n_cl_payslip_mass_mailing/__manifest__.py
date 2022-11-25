# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Chilean Payslip Mass Mailing',
    'version': '13.0.0.0.0',
    'category': 'Human Resources',
    'website': 'http://www.konos.cl',
    'license': 'AGPL-3',
    'author': 'Konos',
    'summary': 'Select send payslips to employee by email',
    'depends': [
        'hr',
        'l10n_cl_hr',
        'mail',
    ],
    'data': [
        "data/payslip_mail_template.xml",
        "wizard/payslip_mass_mailing.xml",
    ],
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
        'static/description/index.html',
    ],
    'installable': False,
    'auto_install': False,
    'application': True,
}

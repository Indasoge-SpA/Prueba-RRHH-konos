# -*- coding: utf-8 -*-
from odoo.tools.misc import str2bool, xlwt
from xlsxwriter.workbook import Workbook
import base64
import re,sys
import io
from odoo import api, fields, models
from xlwt import easyxf
import csv
import time
from datetime import datetime, date

import logging
_logger = logging.getLogger(__name__)

class PayrollPayment(models.TransientModel):
    _name = "hr.payment.report"
    _description = "Payroll Payment"

    journal_id = fields.Many2one('account.journal', string='Journal', required=True, domain=[('type', '=', 'bank')])
    date_to = fields.Date('Date To', required=True, default=lambda self: str(datetime.now()))
    date_from = fields.Date('Fecha Inicial', required=True, default=lambda self: time.strftime('%Y-%m-01'))

    def get_payslip_lines_value(self, obj, rule):
        try:
            lineas = self.env['hr.payslip.line']
            detail = lineas.search([('slip_id','=',obj.id),('code','=',rule)])
            return detail.amount
        except:
            return '0'


    def export_xls(self):
        i = 1
        sheetName = 1
        workbook = xlwt.Workbook()

        n = 1
        c = 0
        style1 = xlwt.easyxf('pattern: pattern solid, fore_colour blue;''font: colour white, bold True;')
        filename = 'PagoNomina'+str(self.date_to)+'.xls'
        style = xlwt.XFStyle()
        tall_style = xlwt.easyxf('font:height 720;')
        font = xlwt.Font()
        font.name = 'Times New Roman'
        font.bold = True
        font.height = 250
        currency = xlwt.easyxf('font: height 180; align: wrap yes, horiz right',
        num_format_str='#,##0.00')
        formato_fecha=xlwt.easyxf(num_format_str='DD-MM-YY')
        worksheet = workbook.add_sheet("PagoNomina"+str(self.date_to))

        payslip_recs = self.env['hr.payslip'].search([('date_from','>=',self.date_from),
        ('date_to', '<=', self.date_to),
        ('state','not in',['draft','cancel']),
        ('company_id' ,'=',self.env.user.company_id.id)])


        worksheet.col(0).width = 5000
        worksheet.col(1).width = 5000
        worksheet.col(2).width = 5000
        worksheet.col(3).width = 5000
        worksheet.col(4).width = 5000
        worksheet.col(5).width = 5000
        worksheet.col(6).width = 5000
        worksheet.col(7).width = 5000
        worksheet.col(8).width = 5000
        worksheet.col(9).width = 5000
        worksheet.col(10).width = 5000
        worksheet.col(11).width = 5000
        worksheet.col(12).width = 5000
        worksheet.write(n-1, 0, 'Cuenta origen', style1)
        worksheet.write(n-1, 1, 'Moneda origen', style1)
        worksheet.write(n-1, 2, 'Cuenta destino', style1)
        worksheet.write(n-1, 3, 'Moneda destino', style1)
        worksheet.write(n-1, 4, 'Código banco destino', style1)
        worksheet.write(n-1, 5, 'RUT beneficiario', style1)
        worksheet.write(n-1, 6, 'Nombre beneficiario', style1)
        worksheet.write(n-1, 7, 'Monto transferencia', style1)
        worksheet.write(n-1, 8, 'Glosa personalizada transferencia', style1)
        worksheet.write(n-1, 9, 'Correo beneficiario', style1)
        worksheet.write(n-1, 10, 'Mensaje correo beneficiario', style1)
        worksheet.write(n-1, 11, 'Glosa cartola originador', style1)
        worksheet.write(n-1, 12, 'Glosa cartola beneficiario', style1)

        for rec in payslip_recs:
            #Only Employees with correct Chilean Bank Accounts
            if rec.employee_id.bank_account_id and rec.employee_id.bank_account_id.bank_id and rec.employee_id.bank_account_id.bank_id.l10n_cl_sbif_code:
                santander = False
                if rec.employee_id.bank_account_id.bank_id.l10n_cl_sbif_code == '037':
                    santander = True

                worksheet.write(n, 0, self.journal_id.bank_account_id.acc_number or False, style)
                worksheet.write(n, 1, 'CLP', style)
                worksheet.write(n, 2, rec.employee_id.bank_account_id.acc_number or False, style)
                worksheet.write(n, 3, 'CLP', style)
                worksheet.write(n, 4, '' if santander else int(rec.employee_id.bank_account_id.bank_id.l10n_cl_sbif_code), style)
                worksheet.write(n, 5, '' if santander else rec.employee_id.identification_id.replace('.','').replace('-',''), style)
                worksheet.write(n, 6, '' if santander else rec.employee_id.name, style)
                worksheet.write(n, 7, self.get_payslip_lines_value(rec,'LIQ'), style)
                worksheet.write(n, 8, rec.name or False, style)
                worksheet.write(n, 9, rec.employee_id.work_email or False, style)
                worksheet.write(n, 10, rec.name or False, style)
                worksheet.write(n, 11, rec.name or False, style)
                worksheet.write(n, 12, rec.name or False, style)
                n = n+1
        fp = io.BytesIO()
        workbook.save(fp)
        export_id = self.env['export.excel'].create({'excel_file':
        base64.encodestring(fp.getvalue()), 'file_name': filename})
        fp.close()

        return {
            'view_mode': 'form',
            'res_id': export_id.id,
            'res_model': 'export.excel',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'context': self._context,
            'target': 'new',

        }
        return True

class export_excel(models.TransientModel):
    _name= "export.excel"
    _description = "Export Excel"
    excel_file = fields.Binary('Excel Report')
    file_name = fields.Char('Excel File', size=64)

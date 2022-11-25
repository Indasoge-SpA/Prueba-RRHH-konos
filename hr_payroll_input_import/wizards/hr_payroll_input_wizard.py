import tempfile
import binascii
import logging
import time
from datetime import datetime, timedelta, date
from odoo.exceptions import Warning, UserError, ValidationError
from odoo import models, fields, api, exceptions, _
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import xlrd
from xlrd import xlsx

_logger = logging.getLogger(__name__)
try:
    import xlwt
except ImportError:
    _logger.debug('Cannot `import xlwt`.')
try:
    import cStringIO
except ImportError:
    _logger.debug('Cannot `import cStringIO`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')


class ContractImportWizards(models.TransientModel):
    _name = "hr.payroll.input.wizard"
    _description = 'Contract Import Wizard'

    file = fields.Binary('File')
    file_opt = fields.Selection([('excel', 'Excel'), ('csv', 'CSV')], default='excel')
    date_end = fields.Date('Date Start', required=True, default=lambda self: str(datetime.now()))

    def import_file(self):
        """File importing workflow"""
        fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
        fp.write(binascii.a2b_base64(self.file))
        fp.seek(0)
        workbook = xlrd.open_workbook(fp.name)
        sheet = workbook.sheet_by_index(0)
        # RUT CODE AMOUNT
        # 18.195.968-1   HEX50   150000
        for row_no in range(sheet.nrows):
            if row_no > 0:
                line = list(map(lambda row: isinstance(
                    row.value, str) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
                vat = line[0]
                code = line[1]
                amount = int(str(line[2]).replace('.0', ''))
                partner_id = self.env['hr.employee'].search(
                    [('identification_id', '=', vat), ('active', '=', True)], limit=1)
                inputs_id = self.env['hr.payslip.input.type'].search([('code', '=', code)], limit=1)
                if not partner_id:
                    _logger.warning("NO Employee")
                    _logger.warning(vat)
                else:
                    _logger.warning(partner_id.identification_id)
                if not inputs_id:
                    _logger.warning("NO CODE")
                    _logger.warning(code)
                if partner_id and inputs_id:
                    vals = {
                        'date': self.date_end,
                        'amount': amount,
                        'inputs_id': inputs_id.id,
                        'employee_id': partner_id.id,
                        'name': code,
                        }
                    inputs = self.env['hr.payroll.input.import'].create(vals)
        action = self.env.ref('hr_payroll_input_import.hr_input_import_action')
        result = action.read()[0]
        return result

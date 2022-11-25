# -*- coding: utf-8 -*-
import time
import babel
from odoo import models, fields, api, tools, _
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)


class HrPayslipInput(models.Model):
    _inherit = 'hr.payslip.input'

    import_input_line_id = fields.Many2one('hr.payroll.input.import', string="Input Import")


class HrPayslipIn(models.Model):
    _inherit = 'hr.payslip'

    @api.onchange('employee_id', 'date_from', 'date_to')
    def onchange_employee(self):
        if (not self.employee_id) or (not self.date_from) or (not self.date_to):
            return

        employee = self.employee_id
        date_from = self.date_from
        date_to = self.date_to

        ttyme = datetime.fromtimestamp(time.mktime(time.strptime(str(date_from), "%Y-%m-%d")))
        locale = self.env.context.get('lang') or 'en_US'
        self.name = _('Salary Slip of %s for %s') % (
            employee.name, tools.ustr(babel.dates.format_date(date=ttyme, format='MMMM-y', locale=locale)))
        self.company_id = employee.company_id

        contract_ids = []
        if not self.env.context.get('contract') or not self.contract_id:
            contract_ids = employee._get_contracts(date_from, date_to, states=['open', 'close'])
            if not contract_ids:
                return
            self.contract_id = contract_ids[0]

        if not self.contract_id.structure_type_id.struct_ids:
            return
        self.struct_id = self.contract_id.structure_type_id.struct_ids[0]

        self.worked_days_line_ids = self._get_new_worked_days_lines()
        worked_days_lines = self.worked_days_line_ids.browse([])
        self.worked_days_line_ids = worked_days_lines
        if contract_ids:
            self.input_line_ids = False
            input_line_ids = self._get_inputs_other(contract_ids, date_from, date_to)
            if input_line_ids:
                self.input_line_ids = input_line_ids
        return

    def _get_inputs_other(self, contract_ids, date_from, date_to):
        contract_obj = self.env['hr.contract']
        emp_id = contract_obj.browse(contract_ids[0].id).employee_id
        input_obj_lines = self.env['hr.payroll.input.import'].search([
            ('employee_id', '=', emp_id.id),
            ('date', '>=', date_from),
            ('date', '<=', date_to)])
        result = []
        for input_obj in input_obj_lines:
            result += [(0, 0, {
                'input_type_id': input_obj.inputs_id.id,
                'amount': input_obj.amount,
            })]
        return result

    def compute_sheet(self):
        res = super(HrPayslipIn, self).compute_sheet()
        payslips = self.filtered(lambda slip: slip.state in ['draft', 'verify'])
        # delete old payslip lines
        payslips.input_line_ids.unlink()
        for payslip in payslips:
            input_line_ids = payslip._get_inputs_other(payslip.contract_id, payslip.date_from, payslip.date_to)
            if input_line_ids:
                payslip.input_line_ids = input_line_ids

        return res

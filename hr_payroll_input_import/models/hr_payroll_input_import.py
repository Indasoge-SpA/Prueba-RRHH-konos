# coding: utf-8
from odoo import api, fields, models


class HrPayrollInputImport(models.Model):
    _name = 'hr.payroll.input.import'
    _description = 'HR Payroll Input Import'

    name = fields.Char('Name', required=True)
    date = fields.Date(string="Payment Date", required=True)
    amount = fields.Float(string="Amount", required=True)
    inputs_id = fields.Many2one("hr.payslip.input.type", string="Input", required=True)
    employee_id = fields.Many2one('hr.employee', string="Employee")
    paid = fields.Boolean(string="Paid")
    payslip_id = fields.Many2one('hr.payslip', string="Payslip Ref.")

    @api.model
    def create(self, vals):
        if vals.get('name', "New") == "New":
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.payroll.input.import') or "New"
        return super(HrPayrollInputImport, self).create(vals)

from odoo import api, fields, models


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.multi
    def action_payslip_done(self):
        res = super(HrPayslip, self).action_payslip_done()
        for rec in self:

            conf_val = self.env['res.config.settings'].search(
                [], order='id desc', limit=1)

            if conf_val and conf_val.auto_leave_allocation:
                allocation_new = {
                    'name': conf_val.holiday_status_id.name,
                    'holiday_status_id': conf_val.holiday_status_id.id,
                    'number_of_days': conf_val.auto_leave_number,
                    'holiday_type': 'employee',
                    'employee_id': rec.employee_id.id,
                }

                new_allocation = self.env[
                    'hr.leave.allocation'].create(allocation_new)
                new_allocation.sudo().action_approve()
        return res

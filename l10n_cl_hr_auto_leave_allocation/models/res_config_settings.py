# -*- coding: utf-8 -*-

from odoo import fields, api, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    auto_leave_allocation = fields.Boolean(
        string="Enable automatic leave allocate",
        help="Automatically increment a leave type to the employees"
    )
    holiday_status_id = fields.Many2one(
        "hr.leave.type", string="Leave Type",
        help="Type to be incremented"
    )
    auto_leave_number = fields.Float(
        string="Days",
        help="Number of days to increment"
    )

    @api.model
    def default_get(self, fields):
        """Function call for get default value."""
        res = super(ResConfigSettings, self).default_get(fields)
        for data in self.search([]):
            res.update({
                'auto_leave_allocation': data.auto_leave_allocation,
                'holiday_status_id': data.holiday_status_id.id,
                'auto_leave_number': data.auto_leave_number,
            })
        return res

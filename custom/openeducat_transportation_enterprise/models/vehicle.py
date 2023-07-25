
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpVehicle(models.Model):
    _name = "op.vehicle"
    _inherits = {"fleet.vehicle": "vehicle_id"}
    _description = "Transportation Vehicle"

    capacity = fields.Integer('Capacity', required=True)
    vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicle',
                                 required=True, ondelete="cascade")
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)
    active = fields.Boolean(default=True)

    @api.constrains('capacity')
    def check_capacity(self):
        if self.capacity <= 0:
            raise ValidationError(_('Enter proper Capacity.'))

    def action_onboarding_vehicle_layout(self):
        self.env.user.company_id.onboarding_vehicle_layout_state = 'done'


# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpStop(models.Model):
    _name = "op.stop"
    _order = "sequence asc"
    _description = "Transportation Stop"

    sequence = fields.Integer('Sequence')
    name = fields.Char('Name', size=64, required=True)
    partner_ids = fields.Many2many('res.partner', string='Person(s)')
    estimated_arrival_conf = fields.Float('Estimated Arrival Time')
    route_id = fields.Many2one('op.route', 'Route', required=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)
    active = fields.Boolean(default=True)
    # state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'),('done','Done')])

    @api.constrains('partner_ids')
    def check_capacity(self):
        total = 0
        for cap in self.route_id.stop_ids:
            total += len(cap.partner_ids)
        if total > self.route_id.vehicle_id.capacity:
            raise ValidationError(_('Vehicle capacity is over.'))

    def action_onboarding_stop_layout(self):
        print('action_onboarding_stop_layout')
        self.env.user.company_id.onboarding_stop_layout_state = 'done'

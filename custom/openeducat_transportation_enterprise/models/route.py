
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields


class OpRoute(models.Model):
    _name = "op.route"
    _description = "Transportation Route"

    name = fields.Char('Name', size=64, required=True)
    stop_ids = fields.One2many('op.stop', 'route_id', string='Stops')
    cost = fields.Float('Cost')
    vehicle_id = fields.Many2one('op.vehicle', 'Vehicle', required=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)
    active = fields.Boolean(default=True)
    product_id = fields.Many2one('product.product', 'Product')
    # fields added
    transport_fee = fields.Float('Transport Fee')

    def action_onboarding_route_layout(self):
        self.env.user.company_id.onboarding_route_layout_state = 'done'

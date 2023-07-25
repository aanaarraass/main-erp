
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


class OpRouteRegister(models.Model):
    _name = "op.route.register"
    _rec_name = "name"
    _description = "Route Register"

    name = fields.Char("Name", required=True)
    route_id = fields.Many2one('op.route', 'Route', required=True)
    start_date = fields.Date(
        'Start Date', required=True, readonly=True, default=fields.Date.today())
    end_date = fields.Date('End Date', required=True)
    product_id = fields.Many2one('product.product', 'Product')

    cost = fields.Float('Cost')
    transport_fee = fields.Float('Transport Fee')
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirm'),
            ('gathering', 'Register Gathering'), ('cancel', 'Cancel')],
        'Status', default='draft')
    transport_lines = fields.One2many('op.transportation.agreement',
                                      'route_register_id',
                                      'Transportation Agreement')
    # transport_lines = fields.One2many('op.transportation.agreement',
    #                                   'stop_id',
    #                                   'Transportation Agreement')
    plan_id = fields.Many2one('cost.plan', string="Plan")

    def set_to_draft(self):
        self.state = 'draft'

    def close_register(self):
        self.state = 'confirm'

    def register_gathering(self):
        self.state = 'gathering'

    def cancel_register(self):
        self.state = 'cancel'

    @api.onchange('route_id')
    def onchange_route_id(self):
        self.product_id = self.route_id.product_id
        self.cost = self.route_id.cost

    @api.constrains('start_date', 'end_date')
    def _check_date(self):
        if self.start_date > self.end_date:
            raise ValidationError(_('End date must be greater than start date'))


# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields, api


class OpRouteStopLine(models.Model):
    _name = "op.route.stop.line"
    _description = "Transportation Route Stop Line"

    sequence = fields.Integer(related="stop_id.sequence", string='Sequence')
    stop_id = fields.Many2one('op.stop', 'Stop')
    estimated_time = fields.Float(compute='_compute_estimated_time',
                                  string='Estimated Arrival')
    route_line_id = fields.Many2one('op.route.line', 'Route Line',
                                    ondelete='cascade')
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)

    @api.depends('stop_id.estimated_arrival_conf', 'route_line_id.start_time')
    def _compute_estimated_time(self):
        for stop in self:
            stop.estimated_time = \
                stop.route_line_id.start_time + \
                stop.stop_id.estimated_arrival_conf


# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields


class OpRoutePssenger(models.Model):
    _name = "op.route.passenger"
    _description = "Transportation Route Passenger"

    stop_id = fields.Many2one('op.stop', 'Stop', required=True)
    route_line_id = fields.Many2one(
        'op.route.line', 'Route Line', required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', 'Passenger', required=True)
    present = fields.Boolean('Present/Absent')
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)

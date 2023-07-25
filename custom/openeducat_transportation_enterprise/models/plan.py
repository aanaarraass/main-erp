
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import fields, models


class Plan(models.Model):
    _name = 'cost.plan'
    _description = 'Plan for Cost'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Plan Code", required=True)
    company_id = fields.Many2one(
        'res.company', default=lambda self: self.env.user.company_id)
    plan_description = fields.Text('Plan Desription')
    bill = fields.Integer(string="Bill Every", tracking=True)
    bill_selection = fields.Selection([('days', 'Day(s)'),
                                       ('weeks', 'Week(s)'),
                                       ('months', 'Month(s)'), ('years', 'Year(s)')],
                                      string="Bill Type", tracking=True,
                                      help='Repeat every (Days/Week/Month/Year)')
    expires_after = fields.Integer(help="Expires after number of billing cycles")

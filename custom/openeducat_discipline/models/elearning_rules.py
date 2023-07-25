# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields


class ElearningRules(models.Model):
    _name = "elearning.rules"
    _description = "Elearning Rules Details"
    _rec_name = "id"

    id = fields.Integer('Id', required=True)
    name = fields.Text('Rules', required=True)
    rules_action = fields.Text('Action To Be Taken', required=True)
    company_id = fields.Many2one('res.company', 'Company', required=True,
                                 default=lambda self: self.env.user.company_id)
    active = fields.Boolean(default=True)

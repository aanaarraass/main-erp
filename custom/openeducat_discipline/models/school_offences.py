# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields


class SchoolOffences(models.Model):
    _name = "school.offences"
    _description = "School Offences Details"
    _rec_name = "offences_type"

    id = fields.Integer('Id', required=True)
    name = fields.Text('Name', required=True)
    offences_type = fields.Selection([
        ('minor', 'Minor'), ('major', 'Major')],
        'Offences Type', required=True)
    company_id = fields.Many2one(
        'res.company', 'Company', required=True,
        default=lambda self: self.env.user.company_id)
    active = fields.Boolean(default=True)

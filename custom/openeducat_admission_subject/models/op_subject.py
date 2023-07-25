
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields


class OpSubject(models.Model):
    _inherit = "op.subject"

    required_subject = fields.One2many(
        "required.subject", "required_subject_id", string="Pre Requisite Subject"
    )


class RequireSubject(models.Model):
    _name = "required.subject"
    _description = 'Require Subject'

    required_subject_id = fields.Many2one("op.subject")

    subject_id = fields.Many2one("op.subject")
    code = fields.Char(related="subject_id.code")

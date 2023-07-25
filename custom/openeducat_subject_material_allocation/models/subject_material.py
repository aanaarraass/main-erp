
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields


class Subjectmaterial(models.Model):
    _inherit = "op.subject"
    _description = "Subject Material Allocation"

    attachment_ids = fields.One2many('ir.attachment', 'res_id',
                                     domain=[('res_model', '=',
                                              'op.subject')],
                                     string='Attachments',
                                     readonly=True)

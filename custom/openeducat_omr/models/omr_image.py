# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields


class OpOmrImage(models.Model):

    _name = 'op.omr.image'
    _description = "Omr Images"
    _inherit = ['mail.thread']
    _rec_name = 'image'

    image = fields.Binary(attachment=True, string="Omr Image")
    omr_exam_id = fields.Many2one("op.omr.exam")

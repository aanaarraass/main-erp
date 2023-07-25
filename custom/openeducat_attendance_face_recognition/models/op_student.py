
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields, api


class OpStudent(models.Model):
    _inherit = "op.student"
    _description = "Student"

    image_detect = fields.Image()
    descriptor = fields.Char("Descriptor")

    @api.onchange('image_detect')
    def onchange_image(self):
        if not self.image_detect:
            self.descriptor = False

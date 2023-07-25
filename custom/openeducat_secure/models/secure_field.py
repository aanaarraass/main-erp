# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields


class Base(models.AbstractModel):
    _inherit = 'base'

    def _valid_field_parameter(self, field, name):
        return name == 'secure' or super()._valid_field_parameter(field, name)


class IrModelSecureField(models.Model):
    _inherit = 'ir.model.fields'

    secure = fields.Boolean(
        string="Secure",
        help="If set,creates QR Code of all secure fields with privacy.",
    )

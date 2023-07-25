# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################


from odoo import models, fields


class AccountAssets(models.Model):
    _inherit = "account.asset.asset"

    assign_state = fields.Boolean(string="Assigned ?", readonly=True)

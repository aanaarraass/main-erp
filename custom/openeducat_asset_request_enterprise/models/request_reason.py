# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################


from odoo import models, fields


class RequestReason(models.Model):
    _name = "asset.request.reason"
    _description = "Request Reason"

    name = fields.Char("Reason")

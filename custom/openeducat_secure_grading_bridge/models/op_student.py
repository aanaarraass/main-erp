# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################


from odoo import models, fields


class OpStudent(models.Model):
    _name = 'op.student'
    _inherit = "op.student"

    first_name = fields.Char(secure=True)
    middle_name = fields.Char(secure=True)
    last_name = fields.Char(secure=True)

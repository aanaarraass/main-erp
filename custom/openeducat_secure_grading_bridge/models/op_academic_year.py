# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields


class OpAcademicYear(models.Model):
    _name = 'op.academic.year'
    _inherit = 'op.academic.year'

    name = fields.Char('Name', required=True, secure=True)

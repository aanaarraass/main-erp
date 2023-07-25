# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields


class GradingAssigment(models.Model):
    _name = 'grading.assignment'

    _inherit = 'grading.assignment'

    name = fields.Char('Name', required=True, secure=True)

# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields


class StudentLeaveType(models.Model):
    _name = "student.leave.type"
    _description = "Student Leave Type"

    name = fields.Char(string="Type", required=True)
    code = fields.Char(string="code", required=True)

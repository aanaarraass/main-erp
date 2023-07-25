
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright(C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################
from odoo import models, fields


class Meeting(models.Model):
    _inherit = 'calendar.event'

    salt = fields.Char("Salt")
    apw = fields.Char("Attendee Password")
    meeting_name = fields.Char("Meeting ID")

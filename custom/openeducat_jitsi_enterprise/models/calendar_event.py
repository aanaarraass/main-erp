
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    use_jitsi = fields.Boolean(
        string='Remote Meeting',
    )

    jitsi_open = fields.Boolean(
        string='Jitsi Open',
        help='The Remote Meeting allows to join',
    )

    jitsi_room = fields.Char(
        string='Jitsi Room',
    )
    online_meeting = fields.Boolean("Online Meeting", copy=False)

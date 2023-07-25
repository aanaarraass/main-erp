# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################


from odoo import models, api, fields, _
from odoo.exceptions import ValidationError


class SkypeMeet(models.TransientModel):
    _name = "skype.meet"
    _description = "Skype Meet"

    user_id = fields.Many2one('res.users', 'User',
                              default=lambda self: self._uid)
    meeting_url = fields.Char("URL For Skype Meet")
    session_id = fields.Many2one("op.session", 'Session')
    invite_via_email = fields.Boolean('Invite Via Email')
    meeting_id = fields.Many2one('calendar.event', 'Meeting')

    @api.model
    def default_get(self, fields):
        res = super(SkypeMeet, self).default_get(fields)
        context = dict(self.env.context)
        active_id = context.get('active_id', False)
        res.update({
            'meeting_id': active_id,
            'invite_via_email': True,
        })
        return res

    def create_meeting(self):
        for record in self:
            record.meeting_id.write({
                'online_meeting': True,
                'meeting_url': self.meeting_url
            })
            for attendee in self.meeting_id.attendee_ids:
                attendee.write({
                    'attendee_meeting_url': self.meeting_url
                })
            if record.invite_via_email is True:
                record.meeting_id.action_sendmail()
            return True
        else:
            raise ValidationError(_("Unable to reach server"))

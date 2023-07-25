# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields, api
import json
import requests


class GoogleMeet(models.TransientModel):

    _name = 'google.meet'
    _description = 'Google Meet Meetings'

    subject = fields.Char(required=True)
    invite_via_email = fields.Boolean()
    start_date = fields.Datetime(required=True, string="Start time")
    end_date = fields.Datetime(required=True, string="End time")
    meeting_id = fields.Many2one('calendar.event')

    @api.model
    def default_get(self, fields):
        res = super(GoogleMeet, self).default_get(fields)
        context = dict(self.env.context)
        active_id = context.get('active_id', False)
        calender = self.env['calendar.event'].browse(active_id)
        res.update({
            'meeting_id': active_id,
            'subject': calender.name,
            'start_date': calender.start,
            'end_date': calender.stop,
            'invite_via_email': True,
        })
        return res

    def create_meeting(self):

        user = self.env['res.users'].sudo().search(
            [('id', '=', self.env.user.id)])

        if user.access_token and user.refresh_token:
            user.refreshTokenUser()

        access_token_config = \
            self.env['ir.config_parameter'].sudo().search(
                [('key', '=', 'google.meet.access.token')])

        user_creds = user.access_token if user.access_token \
            else access_token_config.value

        context = dict(self.env.context)
        active_id = context.get('active_id', False)
        calendar = self.env['calendar.event'].browse(active_id)
        calendar.start_date = self.start_date

        start_time = 'T'.join(str(self.start_date).split(' ')) + 'Z'

        end_time = 'T'.join(str(self.end_date).split(' ')) + 'Z'

        title = calendar.name
        alias_id = calendar.op_session_id.course_id.code
        description = calendar.description
        attendees = []

        for cal in calendar.partner_ids:
            attendees.append({'email': cal.email})

        meeting_body = {
            'summary': title,
            'description': description,

            "end": {
                "dateTime": end_time
            },

            "start": {
                "dateTime": start_time
            },

            "conferenceData": {
                "createRequest": {
                    "conferenceSolutionKey": {
                        "type": "hangoutsMeet"
                    },
                    "requestId": alias_id
                }
            },

            "attendees": attendees,
        }
        try:
            response = requests.post(
                "https://www.googleapis.com/calendar/v3/calendars/primary/events",
                headers={'content-type': 'application/x-www-form-urlencoded',
                         'Authorization': 'Bearer {}'.format(user_creds)},
                data=json.dumps(meeting_body),
                params={'conferenceDataVersion': '1', 'sendNotifications': True})

            meet_url = response.json()['hangoutLink']

            calendar.meet_url = meet_url
            calendar.online_meeting = True

            for record in self:
                for attendee in self.meeting_id.attendee_ids:
                    if record.meeting_id.user_id.partner_id == attendee.partner_id:
                        attendee.write({
                            'attendee_meeting_url': meet_url,
                        })
                    else:
                        attendee.write({
                            'attendee_meeting_url': meet_url,
                        })
                if record.invite_via_email is True:
                    record.meeting_id.action_sendmail()
                return True
        except Exception:
            pass


class CalendarEvent(models.Model):

    _inherit = 'calendar.event'

    meet_url = fields.Char(string="Meet URL", readonly=True)
    online_meeting = fields.Boolean()

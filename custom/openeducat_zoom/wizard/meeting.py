
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, api, fields, _
from odoo.exceptions import AccessError, ValidationError
import requests
import jwt
import time
import json
from random import choice


class ZoomMeeting(models.TransientModel):
    _name = "zoom.meeting"
    _description = "Zoom Meeting"

    name = fields.Char("Name / Subject")
    user_id = fields.Many2one('res.users', 'User',
                              default=lambda self: self._uid)
    apw = fields.Char("Attendee password",
                      default=lambda self: self.create_password())
    session_id = fields.Many2one("op.session", 'Session')
    invite_via_email = fields.Boolean('Invite Via Email')
    meeting_id = fields.Many2one('calendar.event', 'Meeting')

    @api.model
    def default_get(self, fields):
        res = super(ZoomMeeting, self).default_get(fields)
        context = dict(self.env.context)
        active_id = context.get('active_id', False)
        calender = self.env['calendar.event'].browse(active_id)
        res.update({
            'meeting_id': active_id,
            'name': calender.name,
            'invite_via_email': True,
        })
        return res

    def create_password(self):
        size = 6
        values = '0123456789'
        p = ''
        p = p.join([choice(values) for i in range(size)])
        return p

    def create_meeting(self):
        res_param = self.env['ir.config_parameter'].sudo()
        for record in self:
            res_user = self.env['res.users'].search(
                [('id', '=', self.user_id.id)]).sudo()
            if res_user.zoom_api_key and res_user.zoom_secret_key \
                    and res_user.zoom_email:
                api_key = res_user.zoom_api_key
                api_secret_key = res_user.zoom_secret_key
                email = res_user.zoom_email
                settings = {'host_video': res_user.host_video,
                            'participant_video': res_user.participant_video,
                            'cn_meeting': res_user.cn_meeting,
                            'in_meeting': res_user.in_meeting,
                            'join_before_host': res_user.join_before_host,
                            'mute_upon_entry': res_user.mute_upon_entry,
                            'watermark': res_user.watermark,
                            'use_pmi': res_user.use_pmi,
                            'approval_type': res_user.approval_type,
                            'registration_type': res_user.registration_type,
                            'audio': res_user.audio,
                            'auto_recording': res_user.auto_recording,
                            'enforce_login': res_user.enforce_login,
                            'enforce_login_domains':
                                res_user.enforce_login_domains or '',
                            'alternative_hosts':
                                res_user.alternative_hosts or '',
                            'close_registration': res_user.close_registration,
                            'waiting_room': res_user.waiting_room, }

                if not api_key or not api_secret_key:
                    raise AccessError(
                        _('Please Configure Zoom Credentials'))
            else:
                api_key = res_param.search([
                    ('key', '=', 'zoom.apikey')])
                api_secret_key = res_param.search([
                    ('key', '=', 'zoom.secretkey')])
                email = res_param.search([
                    ('key', '=', 'zoom.email')])
                host_video = res_param.search([
                    ('key', '=', 'zoom.host_video')])
                participant_video = res_param.search([
                    ('key', '=', 'zoom.participant_video')])
                cn_meeting = res_param.search([
                    ('key', '=', 'zoom.cn_meeting')])
                in_meeting = res_param.search([
                    ('key', '=', 'zoom.in_meeting')])
                join_before_host = res_param.search([
                    ('key', '=', 'zoom.join_before_host')])
                mute_upon_entry = res_param.search([
                    ('key', '=', 'zoom.mute_upon_entry')])
                watermark = res_param.search([
                    ('key', '=', 'zoom.watermark')])
                use_pmi = res_param.search([
                    ('key', '=', 'zoom.use_pmi')])
                approval_type = res_param.search([
                    ('key', '=', 'zoom.approval_type')])
                registration_type = res_param.search([
                    ('key', '=', 'zoom.registration_type')])
                audio = res_param.search([
                    ('key', '=', 'zoom.audio')])
                auto_recording = res_param.search([
                    ('key', '=', 'zoom.auto_recording')])
                enforce_login = res_param.search([
                    ('key', '=', 'zoom.enforce_login')])
                enforce_login_domains = res_param.search([
                    ('key', '=', 'zoom.enforce_login_domains')])
                alternative_hosts = res_param.search([
                    ('key', '=', 'zoom.alternative_hosts')])
                close_registration = res_param.search([
                    ('key', '=', 'zoom.close_registration')])
                waiting_room = res_param.search([
                    ('key', '=', 'zoom.waiting_room')])
                api_key = api_key.value
                api_secret_key = api_secret_key.value
                email = email.value
                settings = {'host_video': host_video.value,
                            'participant_video': participant_video.value,
                            'cn_meeting': cn_meeting.value,
                            'in_meeting': in_meeting.value,
                            'join_before_host': join_before_host.value,
                            'mute_upon_entry': mute_upon_entry.value,
                            'watermark': watermark.value,
                            'use_pmi': use_pmi.value,
                            'approval_type': int(approval_type.value),
                            'registration_type': int(registration_type.value),
                            'audio': audio.value,
                            'auto_recording': auto_recording.value,
                            'enforce_login': enforce_login.value,
                            'enforce_login_domains':
                                enforce_login_domains.value or '',
                            'alternative_hosts': alternative_hosts.value or '',
                            'close_registration': close_registration.value,
                            'waiting_room': waiting_room.value, }

                if not api_key or not api_secret_key:
                    raise AccessError(
                        _('Please Configure Zoom Credentials'))
            api_key = api_key
            api_secret_key = api_secret_key
            zoom_email = email
            base_url = res_param.search([
                ('key', '=', 'web.base.url')])
            if not base_url:
                raise AccessError(
                    _('Please Configure URL in System Parameters'))
            usr_data = {'email': zoom_email, 'login_type': 2}
            header = {"alg": "HS256", "typ": "JWT"}
            payload = {"iss": api_key, "exp": int(time.time() + 3600)}
            token = jwt.encode(payload, api_secret_key, algorithm="HS256",
                               headers=header)
            header_token = token.decode("utf-8")
            header = {'Authorization': 'Bearer %s' % header_token}
            usr_url = "https://api.zoom.us/v2/users?email=%s&login_type=%d" % (
                usr_data['email'], usr_data['login_type'])
            res_user = requests.get(usr_url, params=usr_data, headers=header)
            data = json.loads(res_user.content)
            for d in data['users']:
                if d['email'] == usr_data['email']:
                    user_id = d['id']
            meeting_date = record.meeting_id.start.strftime(
                "%Y-%m-%dT%H:%M:%SZ")
            url = "https://api.zoom.us/v2/users/%s/meetings" % user_id
            meeting_data = {'topic': record.name,
                            'type': 2,
                            'start_time': meeting_date,
                            'duration': record.meeting_id.duration,
                            'timezone': 'Asia/Kolkata',
                            'password': record.apw,
                            'agenda': record.name,
                            'user_id': '%s' % user_id,
                            'settings': settings,
                            }
            meeting_info = requests.post(url, json=meeting_data, headers=header)
            meeting_json = json.loads(meeting_info.content)
            join_url = meeting_json['join_url']
            record.meeting_id.write({
                'online_meeting': True,
                'meeting_url': meeting_json['start_url'],
                'mpw': meeting_json['password'],
            })
            for attendee in self.meeting_id.attendee_ids:
                if record.meeting_id.user_id.partner_id == attendee.partner_id:
                    attendee.write({
                        'attendee_meeting_url': meeting_json['start_url'],
                        'apw': meeting_json['password']
                    })
                else:
                    attendee.write({
                        'attendee_meeting_url': join_url,
                        'apw': meeting_json['password']
                    })
            if record.invite_via_email is True:
                record.meeting_id.action_sendmail()
            return True
        else:
            raise ValidationError(_("Unable to reach server"))

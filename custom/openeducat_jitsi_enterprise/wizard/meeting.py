
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, api, fields, _
import re
from random import choice

from odoo.exceptions import AccessError


class JitsiMeeting(models.TransientModel):
    _name = "jitsi.meeting"
    _description = "Jitsi Meeting"

    name = fields.Char("Name / Subject")
    user_id = fields.Many2one('res.users', 'User',
                              default=lambda self: self._uid)
    invite_via_email = fields.Boolean('Invite Via Email')
    meeting_id = fields.Many2one('calendar.event', 'Meeting')
    jitsi_password = fields.Char(
        string='Attendee Password',
        default=lambda self: self.create_jitsi_password()
    )
    jitsi_url = fields.Char(
        string='Jitsi Url',
        compute='_compute_jitsi_url',
    )
    jitsi_room = fields.Char(
        string='Jitsi Room',
        compute='_compute_jitsi_url',
    )

    def create_jitsi_password(self):
        size = 6
        values = '0123456789'
        p = ''
        p = p.join([choice(values) for i in range(size)])
        return p

    def _compute_jitsi_url(self):
        for record in self:
            real_id = record.meeting_id.id
            record.jitsi_url = '/jitsi/{0}'.format(real_id)
            room_name = '{0} vc {1}'.format(record.user_id.company_id.name,
                                            real_id).lower()
            room_name = re.sub('[^\w ]+', '', room_name)  # noqa
            room_name = re.sub(' +', '-', room_name)
            record.jitsi_room = room_name

    @api.model
    def default_get(self, fields):
        res = super(JitsiMeeting, self).default_get(fields)
        context = dict(self.env.context)
        active_id = context.get('active_id', False)
        calender = self.env['calendar.event'].browse(active_id)
        res.update({
            'meeting_id': active_id,
            'name': calender.name,
            'invite_via_email': True,
        })
        return res

    def create_meeting(self):
        res_param = self.env['ir.config_parameter'].sudo()
        for record in self:
            url = res_param.search([
                ('key', '=', 'jitsi.server')])
            if not url:
                raise AccessError(
                    _('Please Configure Jitsi Credentials'))
            base_url = res_param.search([
                ('key', '=', 'web.base.url')])
            if not base_url:
                raise AccessError(
                    _('Please Configure URL in System Parameters'))
            record.meeting_id.write({
                'use_jitsi': True,
                'mpw': record.jitsi_password,
                'jitsi_open': True,
                'meeting_url': record.jitsi_url,
                'jitsi_room': record.jitsi_url,
                'online_meeting': True,
            })
            for attendee in self.meeting_id.attendee_ids:
                record.jitsi_url = '/jitsi/join/{0}'.format(attendee.id)
                attendee.write({
                    'attendee_meeting_url': record.jitsi_url,
                    'apw': record.jitsi_password,
                })
            if record.invite_via_email is True:
                record.meeting_id.action_sendmail()

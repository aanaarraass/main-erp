
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################


from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    openeducat_zoom_api_key = fields.Char(
        string="OpenEducat Zoom Api Key", readonly=False,
        help="Configure your Zoom Api Key")
    openeducat_zoom_secret_key = fields.Char(
        "OpenEducat Zoom Secret Key", readonly=False,
        help="Configure your Zoom Secret Key")
    openeducat_zoom_email = fields.Char(
        "OpenEducat Zoom email", readonly=False,
        help="Configure yours Zoom Email")
    dial_number_zoom = fields.Char('Dial Number',
                                   config_parameter='zooom.dial_number')
    host_video = fields.Boolean('Host Video',
                                help="Start meetings with "
                                     "the host's video on.")
    participant_video = fields.Boolean('Participant Video',
                                       help="Start meetings with the "
                                            "participants video on.")
    cn_meeting = fields.Boolean('CN Meeting', help='Meeting in China')
    in_meeting = fields.Boolean('In Meeting', help="Meeting in India ")
    join_before_host = fields.Boolean('Join Before Host',
                                      help='Allow participants to join'
                                           ' the meeting before the host'
                                           ' joins. If disabled, participants'
                                           ' can only join after the host'
                                           ' starts the meeting.'
                                      )
    mute_upon_entry = fields.Boolean('Mute Open Entry',
                                     help=' If join before host is not enabled'
                                          ', this will mute participants as'
                                          ' they join the meeting.'
                                          ' Participants can unmute themselves'
                                          ' after joining the meeting.')
    watermark = fields.Boolean('Watermark',
                               help='The Watermark feature superimposes'
                                    ' an image, consisting of a portion of a'
                                    ' meeting participant own email address, '
                                    'onto the shared content they are viewing'
                                    ' and the video of the person who is'
                                    ' sharing their screen.')
    use_pmi = fields.Boolean('Use PMI',
                             help="Check this if you want to use your Personal"
                                  " Meeting ID. If not selected, a random"
                                  " unique meeting ID will be generated.")
    approval_type = fields.Char('Approval Time',
                                help=" 0 Automatically Approve,"
                                     " 1 Manually Approve,"
                                     " 2 No Registration Required")
    registration_type = fields.Char('Registration Type',
                                    help="Used for recurring meeting "
                                         "with fixed time only.")
    audio = fields.Char('Audio',
                        help='Choose whether to allow users to call in via'
                             ' Telephone only, Computer Audio only, Both, '
                             'or 3rd Party Audio ')
    auto_recording = fields.Char('Auto Recording',
                                 help='Check this if you want the meeting to'
                                      ' be automatically recorded.')
    enforce_login = fields.Boolean('Enforce Login',
                                   help="Only signed-in users "
                                        "can join this meeting")
    enforce_login_domains = fields.Char('Enforce Login Domains',
                                        help="Only signed-in users "
                                             "with a specified domains")
    alternative_hosts = fields.Char('Alternative Hosts',
                                    help='Enter the email address of another'
                                         ' Zoom user who is Licensed, '
                                         'on your account to allow them to '
                                         'start the meeting in your absence. ')
    close_registration = fields.Boolean('Close Registration',
                                        help="Close registration "
                                             "after event date")
    waiting_room = fields.Boolean('Waiting Room',
                                  help=' Waiting Room feature allows the host'
                                       ' to control when a participant joins'
                                       ' the meeting. As the meeting host,'
                                       ' you can admit attendees one by one'
                                       ' or hold all attendees in the waiting'
                                       ' room and admit them all at once.')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            openeducat_zoom_api_key=self.env['ir.config_parameter'].sudo().get_param(
                'zoom.apikey'),
            openeducat_zoom_secret_key=self.env['ir.config_parameter'].sudo().get_param(
                'zoom.secretkey'),
            openeducat_zoom_email=self.env['ir.config_parameter'].sudo().get_param(
                'zoom.email'),
            host_video=self.env['ir.config_parameter'].sudo().get_param(
                'zoom.host_video'),
            participant_video=self.env['ir.config_parameter'].sudo().get_param(
                'zoom.participant_video'),
            cn_meeting=self.env['ir.config_parameter'].sudo().get_param(
                'zoom.cn_meeting'),
            in_meeting=self.env['ir.config_parameter'].sudo().get_param(
                'zoom.in_meeting'),
            join_before_host=self.env['ir.config_parameter'].sudo().get_param(
                'zoom.join_before_host'),
            mute_upon_entry=self.env['ir.config_parameter'].sudo().get_param(
                'zoom.mute_upon_entry'),
            watermark=self.env['ir.config_parameter'].sudo().get_param(
                'zoom.watermark'),
            use_pmi=self.env['ir.config_parameter'].sudo().get_param(
                'zoom.use_pmi'),
            approval_type=(self.env['ir.config_parameter'].sudo().get_param(
                'zoom.approval_type')),
            registration_type=self.env['ir.config_parameter'].sudo().get_param(
                'zoom.registration_type'),
            audio=self.env['ir.config_parameter'].sudo().get_param(
                'zoom.audio'),
            auto_recording=self.env['ir.config_parameter'].sudo().get_param(
                'zoom.auto_recording'),
            enforce_login=self.env['ir.config_parameter'].sudo().get_param(
                'zoom.enforce_login'),
            enforce_login_domains=self.env['ir.config_parameter'].sudo().get_param(
                'zoom.enforce_login_domains'),
            alternative_hosts=self.env['ir.config_parameter'].sudo().get_param(
                'zoom.alternative_hosts'),
            close_registration=self.env['ir.config_parameter'].sudo().get_param(
                'zoom.close_registration'),
            waiting_room=self.env['ir.config_parameter'].sudo().get_param(
                'zoom.waiting_room'),

        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        param.set_param('zoom.apikey', self.openeducat_zoom_api_key)
        param.set_param('zoom.secretkey', self.openeducat_zoom_secret_key)
        param.set_param('zoom.email', self.openeducat_zoom_email)
        param.set_param('zoom.host_video', self.host_video)
        param.set_param('zoom.participant_video', self.participant_video)
        param.set_param('zoom.cn_meeting', self.cn_meeting)
        param.set_param('zoom.in_meeting', self.in_meeting)
        param.set_param('zoom.join_before_host', self.join_before_host)
        param.set_param('zoom.mute_upon_entry', self.mute_upon_entry)
        param.set_param('zoom.watermark', self.watermark)
        param.set_param('zoom.use_pmi', self.use_pmi)
        param.set_param('zoom.approval_type', self.approval_type)
        param.set_param('zoom.registration_type', self.registration_type)
        param.set_param('zoom.audio', self.audio)
        param.set_param('zoom.auto_recording', self.auto_recording)
        param.set_param('zoom.enforce_login', self.enforce_login)
        param.set_param('zoom.enforce_login_domains', self.enforce_login_domains)
        param.set_param('zoom.alternative_hosts', self.alternative_hosts)
        param.set_param('zoom.close_registration', self.close_registration)
        param.set_param('zoom.waiting_room', self.waiting_room)

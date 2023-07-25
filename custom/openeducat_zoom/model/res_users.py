
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################


from odoo import fields, models, SUPERUSER_ID


class ResUsers(models.Model):
    _inherit = 'res.users'
    zoom_api_key = fields.Char(
        string="Zoom Api Key", readonly=False,
        help="Configure your Zoom Api Key")
    zoom_secret_key = fields.Char(
        "Zoom Secret Key", readonly=False,
        help="Configure your Zoom Secret Key")
    zoom_email = fields.Char(
        "Zoom Email", readonly=False,
        help="Configure yours Zoom Email")
    host_video = fields.Boolean('Host Video',
                                help="Start meetings with the "
                                     "host's video on.")
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
    approval_type = fields.Integer(
        'Approval Time', help="0 Automatically Approve,"
                              "1 Manually Approve,"
                              "2 No Registration Required")
    registration_type = fields.Integer(
        'Registration Type', help="Used for recurring meeting "
                                  "with fixed time only.")
    audio = fields.Char('Audio',
                        help='Choose whether to allow users to call in via'
                             ' Telephone only, Computer Audio only, Both, '
                             'or 3rd Party Audio ')
    auto_recording = fields.Char('Auto Recording',
                                 help='Check this if you want the meeting to '
                                      'be automatically recorded.')
    enforce_login = fields.Boolean(
        'Enforce Login')
    enforce_login_domains = fields.Char(
        'Enforce Login Domains')
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

    def write(self, vals):
        self = self.with_user(SUPERUSER_ID)
        result = super(ResUsers, self).write(vals)
        return result

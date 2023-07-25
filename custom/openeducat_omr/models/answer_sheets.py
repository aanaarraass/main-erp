# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields
import uuid


class OpAnswerSheets(models.Model):

    _name = 'op.answer.sheets'
    _description = "Answer Sheets"
    _inherit = ['mail.thread']
    _rec_name = 'roll_number'

    roll_number = fields.Char(string="Roll Number")
    key_type = fields.Char(string="Paper Set")
    right_answer = fields.Integer(string="Right Answers")
    wrong_answer = fields.Integer(string="Wrong Answer")
    not_attampted = fields.Integer(string="Not Attampted")
    score = fields.Integer(string="Total Score")
    omr_exam_id = fields.Many2one("op.omr.exam")
    date_time = fields.Datetime(string="Date & Time", readonly=True)
    student_id = fields.Many2one('op.student')
    image_id = fields.Many2one('op.omr.image')

    access_url = fields.Char(
        'Portal Access URL', compute='_compute_access_url',
        help='Customer Portal URL')
    access_token = fields.Char('Security Token', copy=False)

    def _compute_access_url(self):
        for record in self:
            record.access_url = '/openeducat-omr/exam/result/%s' % (record.id)

    def _portal_ensure_token(self):
        """ Get the current record access token """
        if not self.access_token:
            # we use a `write` to force the cache clearing otherwise
            # `return self.access_token` will return False
            self.sudo().write({'access_token': str(uuid.uuid4())})
        return self.access_token

    def get_portal_url(self, suffix=None, report_type=None,
                       download=None, query_string=None, anchor=None):
        """
            Get a portal url for this model, including access_token.
            The associated route must handle the flags for them to have any effect.
            - suffix: string to append to the url, before the query string
            - report_type: report_type query string, often one of: html, pdf, text
            - download: set the download query string to true
            - query_string: additional query string
            - anchor: string to append after the anchor #
        """
        self.ensure_one()
        url = self.access_url + '%s?access_token=%s%s%s%s' % (
            suffix if suffix else '',
            self._portal_ensure_token(),
            '&download=true' if download else '',
            query_string if query_string else '',
            '#%s' % anchor if anchor else ''
        )
        return url

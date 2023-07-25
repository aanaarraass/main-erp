# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields


class OpAnswerSheetConfiguration(models.Model):

    _name = 'op.answersheet.configuration'
    _description = "Answer Sheet Configuration"
    _inherit = ['mail.thread']
    _rec_name = 'name'

    name = fields.Char("Answer Sheet Name")
    subject_id = fields.Many2one('op.subject')
    answer_set_line = fields.One2many("op.answer.set", "answersheet_configuration_id")

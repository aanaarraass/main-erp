# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields


class OpAnswerSet(models.Model):

    _name = 'op.answer.set'
    _description = "Answer Sets"
    _inherit = ['mail.thread']
    _rec_name = 'paper_set'

    paper_set = fields.Char("Paper Set")
    question_answer_line = fields.One2many("op.question.answer", "answer_set_id")
    omr_exam_id = fields.Many2one("op.omr.exam")
    answersheet_configuration_id = fields.Many2one("op.answersheet.configuration")


class OpQuestionAnswer(models.Model):

    _name = 'op.question.answer'
    _description = "Answer Sheet Question-Answer"
    _inherit = ['mail.thread']

    question = fields.Integer(string="Question Number")
    answer = fields.Char(string="Answer")
    answer_set_id = fields.Many2one("op.answer.set")

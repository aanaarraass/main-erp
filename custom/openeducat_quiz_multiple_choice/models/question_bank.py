from odoo import models, fields


class OpQuestionBank(models.Model):
    _inherit = "op.question.bank.line"

    que_type = fields.Selection(
        selection_add=[('multiple_choice', 'Multiple Choice')],
        default='optional')
    multiple_choice_que_type = fields.Selection([
        ('text', 'Text'), ('image', 'Image')], 'Multiple Choice Question Type',
        default='text')
    multiple_choice_line_ids = fields.One2many(
        'op.question.bank.answer.multiple.choice',
        'multiple_choice_line_id', 'Multiple Choice Answers')


class OpQuestionMultipleChoiceBankAnswer(models.Model):
    _name = "op.question.bank.answer.multiple.choice"
    _description = "Quiz Question Bank Answers multiple choice"

    que_type = fields.Selection([
        ('text', 'Text'), ('image', 'Image')], 'Question Type')
    que_image = fields.Binary("Image")
    que_text = fields.Char('Text Question')
    given_answer = fields.Boolean('Given Answer')
    default_answer = fields.Boolean('default Answer')
    multiple_choice_line_id = fields.Many2one(
        'op.question.bank.line', 'Question line')
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)

from odoo import models, fields


class OpQuestionBank(models.Model):
    _inherit = "op.question.bank.line"

    que_type = fields.Selection(
        selection_add=[('match_following', 'Match Following')],
        ondelete={'match_following': 'set default'})
    following_line_ids = fields.One2many('op.question.bank.answer.following',
                                         'following_line_id', 'Follwing Answers')


class OpQuestionBankAnswer(models.Model):
    _name = "op.question.bank.answer.following"
    _description = "Quiz Answers match the following"

    image = fields.Binary("Image")
    question = fields.Char('Question')
    answer = fields.Char('Answer')
    following_line_id = fields.Many2one('op.question.bank.line', 'question')
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self : self.env.user.company_id)

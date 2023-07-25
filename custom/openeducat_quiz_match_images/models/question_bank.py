from odoo import models, fields


class OpQuestionBank(models.Model):
    _inherit = "op.question.bank.line"

    que_type = fields.Selection(
        selection_add=[('match_following_images',
                        'Match the Images')], default='optional')
    following_images_line_ids = fields.One2many(
        'op.question.bank.answer.following.images',
        'following_images_line_id', 'Follwing Answers')


class OpQuestionBankAnswer(models.Model):
    _name = "op.question.bank.answer.following.images"
    _description = "Quiz Answers match the following images"

    image = fields.Binary("Question", required=True)
    given_answer = fields.Binary('Given Answer')
    default_answer = fields.Binary('default Answer', required=True)
    following_images_line_id = fields.Many2one(
        'op.question.bank.line', 'question')
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)

from odoo import fields, models


class Quizmatchfollowing(models.Model):
    _inherit = "op.quiz.line"

    que_type = fields.Selection(
        selection_add=[('match_following', 'Match Following')],
        ondelete={'match_following': 'set default'})
    following_line_ids = fields.One2many('op.quiz.answer.following',
                                         'following_line_id', 'Follwing Answers')


class Quizmatchanswer(models.Model):
    _name = "op.quiz.answer.following"
    _description = "Quiz Answers match the following"

    image = fields.Binary("Image")
    question = fields.Char('Question')
    answer = fields.Char('Answer')
    default_answer = fields.Char('default Answer')
    grade_id = fields.Many2one('op.answer.grade', 'Grade')
    following_line_id = fields.Many2one('op.quiz.line', 'question')
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self : self.env.user.company_id)


class Quiz(models.Model):
    _inherit = "op.quiz"

    def get_result_id(self):
        res = super(Quiz, self).get_result_id()
        for data in res.line_ids:
            if data.bank_line.que_type == 'match_following':
                if data.que_type != 'match_following':
                    for temp in data.bank_line.following_line_ids:
                        self.env['op.quiz.result.line.answers'].sudo().create({
                            'line_id' : data.id,
                            'image' : temp.image,
                            'question' : temp.question,
                            'name' : '',
                            'default_answer' : temp.answer,
                        })
                data.que_type = data.bank_line.que_type
                data.grade_true_id = data.bank_line.grade_true_id
                data.grade_false_id = data.bank_line.grade_false_id
        return res

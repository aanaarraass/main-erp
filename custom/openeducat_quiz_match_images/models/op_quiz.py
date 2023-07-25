from odoo import fields, models


class Quizmatchfollowing(models.Model):
    _inherit = "op.quiz.line"

    que_type = fields.Selection(
        selection_add=[('match_following_images', 'Match the Images')],
        default='optional')
    following_images_line_ids = fields.One2many(
        'op.quiz.answer.following.images',
        'following_images_line_id', 'Follwing Images Answers')


class QuizMatchImagesAnswer(models.Model):
    _name = "op.quiz.answer.following.images"
    _description = "Quiz Answers match the following images"

    image = fields.Binary("Question", required=True)
    given_answer = fields.Binary('Given Answer')
    default_answer = fields.Binary('default Answer', required=True)
    grade_id = fields.Many2one('op.answer.grade', 'Grade')
    following_images_line_id = fields.Many2one('op.quiz.line', 'question')
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)


class Quiz(models.Model):
    _inherit = "op.quiz"

    def get_result_id(self):
        res = super(Quiz, self).get_result_id()
        for data in res.line_ids:
            if data.bank_line.que_type == 'match_following_images':
                if data.que_type != 'match_following_images':
                    for temp in data.bank_line.following_images_line_ids:
                        self.env['op.quiz.result.line.following.images'].\
                            sudo().create(
                            {'following_images_line_id': data.id,
                             'image': temp.image,
                             'default_answer': temp.default_answer,
                             'given_answer': ''})
                data.que_type = data.bank_line.que_type
                data.grade_true_id = data.bank_line.grade_true_id
                data.grade_false_id = data.bank_line.grade_false_id
        return res

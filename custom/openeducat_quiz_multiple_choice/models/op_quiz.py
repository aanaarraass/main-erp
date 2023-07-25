from odoo import fields, models


class QuizMultipleChoice(models.Model):
    _inherit = "op.quiz.line"

    que_type = fields.Selection(
        selection_add=[('multiple_choice', 'Multiple Choice')],
        default='optional')
    multiple_choice_que_type = fields.Selection([
        ('text', 'Text'), ('image', 'Image')], 'Multiple Choice Question Type',
        default='text')
    multiple_choice_line_ids = fields.One2many(
        'op.quiz.answer.multiple.choice',
        'multiple_choice_line_id', 'Multiple Choice Answers')


class QuizMultipleChoiceAnswer(models.Model):
    _name = "op.quiz.answer.multiple.choice"
    _description = "Quiz Answers multiple choice"

    que_image = fields.Binary('image Question')
    que_given_answer = fields.Binary('default Answer')
    que_text = fields.Char('Text Question')
    que_text_answer = fields.Char('Text Answer')
    default_answer = fields.Boolean('Grade')
    multiple_choice_line_id = fields.Many2one('op.quiz.line', 'question')
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)


class Quiz(models.Model):
    _inherit = "op.quiz"

    def get_result_id(self):
        res = super(Quiz, self).get_result_id()
        for data in res.line_ids:
            if data.bank_line.que_type == 'multiple_choice':
                if data.que_type != 'multiple_choice':
                    for temp in data.bank_line.multiple_choice_line_ids:
                        self.env['op.quiz.result.line.multiple.choice'].\
                            sudo().create(
                            {'multiple_choice_line_id': data.id,
                             'que_image': temp.que_image,
                             'que_text': temp.que_text,
                             'default_answer': temp.default_answer, })
                data.que_type = data.bank_line.que_type
                data.multiple_choice_que_type = data.\
                    bank_line.multiple_choice_que_type
                data.grade_true_id = data.bank_line.grade_true_id
                data.grade_false_id = data.bank_line.grade_false_id
        return res

from odoo import fields, models


class QuizNumeric(models.Model):
    _inherit = "op.quiz.line"

    que_type = fields.Selection(
        selection_add=[('numeric', 'Numeric')], ondelete={'numeric': 'set default'})
    numeric_answer = fields.Float('numeric')


class Quiz(models.Model):
    _inherit = "op.quiz"

    def get_result_id(self):
        res = super(Quiz, self).get_result_id()
        for data in res.line_ids:
            if data.bank_line.que_type == 'numeric':
                data.que_type = data.bank_line.que_type
                data.answer = data.bank_line.numeric_answer
                data.grade_true_id = data.bank_line.grade_true_id
                data.grade_false_id = data.bank_line.grade_false_id
        return res

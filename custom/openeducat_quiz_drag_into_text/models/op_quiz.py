from odoo import fields, models


class QuizDragIntoText(models.Model):
    _inherit = "op.quiz.line"

    que_type = fields.Selection(
        selection_add=[('drag_into_text', 'Drag Into Text')],
        ondelete={'drag_into_text': 'set default'})


class QuizResultDragIntoText(models.Model):
    _inherit = "op.quiz"

    def get_result_id(self):
        res = super(QuizResultDragIntoText, self).get_result_id()
        for data in res.line_ids:
            if data.bank_line.que_type == 'drag_into_text':
                s = data.name
                x = s.replace("<<", "")
                y = x.replace(">>", "")
                data.answer = y
                data.que_type = data.bank_line.que_type
                data.grade_true_id = data.bank_line.grade_true_id
                data.grade_false_id = data.bank_line.grade_false_id
        return res

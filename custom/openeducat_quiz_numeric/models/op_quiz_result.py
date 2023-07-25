from odoo import fields, models, api


class QuizResultLineNumeric(models.Model):
    _inherit = "op.quiz.result.line"

    que_type = fields.Selection(
        selection_add=[('numeric', 'Numeric')], ondelete={'numeric': 'set default'})


class QuizResultNumeric(models.Model):
    _inherit = "op.quiz.result"

    @api.depends('line_ids', 'line_ids.mark', 'line_ids.answer',
                 'line_ids.given_answer')
    def _compute_get_result(self):
        res = super(QuizResultNumeric, self)._compute_get_result()
        for obj in self:
            obj.total_question = len(obj.line_ids.ids)
            total_correct = obj.total_correct
            total_incorrect = obj.total_incorrect
            total_not_attempt = obj.total_not_attempt
            total_marks = 0
            received_marks = obj.received_marks
            for line in obj.line_ids:
                total_marks += line.question_mark or 0.0
                if not line.given_answer:
                    total_not_attempt += 1
                    continue
                if line.que_type == 'numeric':
                    if float(line.answer) == float(line.given_answer):
                        received_mark = (line.question_mark *
                                         (line.grade_true_id.value or 0.0)) / 100
                        line.mark = received_mark
                        received_marks += line.question_mark
                        total_correct += 1
                    else:
                        received_mark = (line.question_mark * (line.grade_false_id.value
                                                               or 0.0)) / 100
                        received_marks += received_mark
                        line.mark = received_mark
                        total_incorrect += 1
            obj.total_marks = total_marks or 0.0
            obj.total_not_attempt = total_not_attempt or 0.0
            obj.total_incorrect = total_incorrect or 0.0
            obj.total_correct = total_correct or 0.0
            obj.received_marks = received_marks or 0.0
            obj.score = (received_marks * 100) / total_marks
        return res

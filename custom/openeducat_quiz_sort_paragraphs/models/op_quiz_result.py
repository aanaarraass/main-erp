from odoo import fields, models, api


class QuizResultLine(models.Model):
    _inherit = "op.quiz.result.line"

    que_type = fields.Selection(
        selection_add=[('sort_paragraphs', 'Sort the Paragraphs')],
        ondelete={'sort_paragraphs': 'set default'})
    sort_paragraphs_line_ids = fields.One2many(
        'op.quiz.result.line.sort.paragraphs',
        'line_id', 'Sort Paragraphs Answer')


class QuizResultLineSortParagraphs(models.Model):
    _name = "op.quiz.result.line.sort.paragraphs"
    _description = "Quiz result sort paragraphs"

    given_answer = fields.Char('Given Answer')
    default_answer = fields.Char('Default Answer')
    line_id = fields.Many2one('op.quiz.result.line', 'Question')


class QuizResultSortParagraphs(models.Model):
    _inherit = "op.quiz.result"

    @api.depends('line_ids.sort_paragraphs_line_ids',
                 'line_ids.sort_paragraphs_line_ids.given_answer')
    def _compute_get_result(self):
        res = super(QuizResultSortParagraphs, self)._compute_get_result()
        for obj in self:
            obj.total_question = len(obj.line_ids.ids)
        total_correct = obj.total_correct
        total_incorrect = obj.total_incorrect
        total_not_attempt = obj.total_not_attempt
        total_marks = 0
        received_marks = obj.received_marks
        for line in obj.line_ids:
            total_marks += line.question_mark or 0.0
            if not line.name:
                total_not_attempt += 1
                continue
            if line.que_type == 'sort_paragraphs':
                line.mark = 0
                total_question_line = len(line.sort_paragraphs_line_ids)
                total_correct_ans = 0
                for data in line.sort_paragraphs_line_ids:
                    if data.given_answer == data.default_answer:
                        total_correct_ans += 1
                if total_correct_ans == total_question_line:
                    total_correct += 1
                    received_marks += (line.question_mark*line.grade_true_id.value)/100
                    line.mark = (line.question_mark*line.grade_true_id.value)/100
                else:
                    total_incorrect += 1
                    received_marks += (line.question_mark*line.grade_false_id.value)/100
                    line.mark = (line.question_mark*line.grade_false_id.value)/100
        obj.total_marks = total_marks or 0.0
        obj.total_not_attempt = total_not_attempt or 0.0
        obj.total_incorrect = total_incorrect or 0.0
        obj.total_correct = total_correct or 0.0
        obj.received_marks = received_marks or 0.0
        obj.score = (received_marks * 100) / total_marks
        return res

    def get_answer_data(self):
        res = super(QuizResultSortParagraphs, self).get_answer_data()
        datafilter = list(filter(
            lambda i: i['que_type'] != 'sort_paragraphs', res['not_attempt_answer']))
        res['not_attempt_answer'] = datafilter
        for line in self.line_ids:
            if line.que_type == 'sort_paragraphs':
                temp_total_correct = 0
                total_question_line = len(line.sort_paragraphs_line_ids)
                for data in line.sort_paragraphs_line_ids:
                    if data.given_answer == data.default_answer:
                        temp_total_correct += 1
                if(temp_total_correct == total_question_line):
                    questiondata = []
                    for temp in line.sort_paragraphs_line_ids:
                        questiondata.append({
                            'given_answer' : temp.given_answer,
                            'default_answer' : temp.default_answer,
                            'id' : temp.id})
                    res['right_answers'].append(
                        {'que_type': line.que_type, 'question': line.name,
                         'answer': line.answer or '', 'line_data' : questiondata})
                else:
                    questiondata = []
                    for temp in line.sort_paragraphs_line_ids:
                        questiondata.append({
                            'given_answer' : temp.given_answer,
                            'default_answer' : temp.default_answer,
                            'id' : temp.id})
                    res['wrong_answer'].append(
                        {'que_type': line.que_type, 'question': line.name,
                         'given_answer': line.given_answer,
                         'answer': line.answer, 'line_data' : questiondata})
        quiz = self.quiz_id
        if quiz.wrong_ans and res['wrong_answer']:
            res['display_wrong_ans'] = 1
        if quiz.right_ans and res['right_answers']:
            res['display_true_ans'] = 1
        if quiz.not_attempt_ans and res['not_attempt_answer']:
            res['not_attempt_ans'] = 1
        return res

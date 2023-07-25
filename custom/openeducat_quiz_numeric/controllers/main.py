from odoo import http
from odoo.addons.openeducat_quiz.controllers.main import OpeneducatQuizRender
from odoo.http import request


class OpeneducatQuizNumeric(OpeneducatQuizRender):

    @http.route()
    def quiz_result_attempt(self, **kwargs):
        res = super(OpeneducatQuizNumeric, self).quiz_result_attempt(**kwargs)
        if kwargs.get('question', False):
            result_line = request.env['op.quiz.result.line']
            line = result_line.sudo().browse(
                int(kwargs['question']))
        if 'answer' in kwargs and kwargs['answer']:
            if line.que_type == 'numeric':
                line.given_answer = kwargs['answer']
        return res

    def get_quiz_result_data(self, values):
        res = super(OpeneducatQuizNumeric, self).get_quiz_result_data(values)
        result = request.env['op.quiz.result']. \
            sudo().browse(int(values['ExamID']))

        datafilter = list(filter(
            lambda i: i['que_type'] != 'numeric', res['not_attempt_answer']))
        res['not_attempt_answer'] = datafilter

        for line in result.line_ids:
            if ('numeric' + str(line.id)) in values:
                if values['numeric' + str(line.id)] != '':
                    given_answer_id = float(values['numeric' + str(line.id)])
                    line.given_answer = given_answer_id
                    if float(line.given_answer) == float(line.answer):
                        res['right_answers'].append({
                            'question': line.name, 'answer': line.answer,
                        })
                        received_mark = (line.question_mark *
                                         (line.grade_true_id.value or 0.0)) / 100
                        line.mark = received_mark
                    else:
                        res['wrong_answer'].append({
                            'question': line.name,
                            'given_answer': line.given_answer,
                            'answer': line.answer,
                        })
                        received_mark = (line.question_mark *
                                         (line.grade_false_id.value or 0.0)) / 100
                        line.mark = received_mark
                else:
                    res['not_attempt_answer'].append({
                        'question': line.name, 'answer': line.answer or ''})
        quiz = result.quiz_id
        if quiz.wrong_ans and res['wrong_answer']:
            res['display_wrong_ans'] = 1
        if quiz.right_ans and res['right_answers']:
            res['display_true_ans'] = 1
        if quiz.not_attempt_ans and res['not_attempt_answer']:
            res['not_attempt_ans'] = 1
        res['total_incorrect'] = result.total_incorrect
        res['total_question'] = result.total_question
        res['total_correct'] = result.total_correct
        res['total_incorrect'] = result.total_incorrect
        res['total_marks'] = result.total_marks
        res['received_marks'] = result.received_marks
        return res

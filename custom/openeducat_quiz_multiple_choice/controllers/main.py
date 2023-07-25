from odoo import http
from odoo.http import request
from odoo.addons.openeducat_quiz.controllers.main import \
    OpeneducatQuizRender


class QuizMatchFollowingImages(http.Controller):

    @http.route('/multiple/choice/data', type='json',
                website=True, auth='user', csrf=False)
    def quiz_data(self, answerdata=None):
        following_data = []
        if answerdata:
            for index in range(len(answerdata)):
                result = answerdata[index]['id']
                quiz_data1 = request.env['op.quiz.result.line']. \
                    sudo().browse(int(result))
                for data in quiz_data1:
                    questiondata = []
                    for temp in data.multiple_choice_line_ids:
                        questiondata.append({
                            'given_answer': temp.given_answer,
                            'id': temp.id,
                            'que_type': data.multiple_choice_que_type
                        })
                    following_data.append({
                        'id': data.id,
                        'que_type': data.que_type,
                        'que_required': data.result_id.quiz_id.que_required,
                        'name': data.name,
                        'question_data': questiondata

                    })
        return following_data

    @http.route(['/quiz/multiple_choice/answer/data'], type='json',
                website=True, auth='user', csrf=False)
    def quiz_following_images_answer(self, answerdata=None):
        if answerdata:
            for index in range(len(answerdata)):
                result = answerdata[index]['id']
                temp = request.env['op.quiz.result.line.multiple.choice']. \
                    sudo().browse(int(result))
                temp.given_answer = answerdata[index]['answer']

    @http.route('/following/check/check/required', type='json',
                website=True, auth='user', csrf=False)
    def check_que_required(self, question_id=None):
        quiz_data = request.env['op.quiz.result.line'].sudo().browse(
            int(question_id))
        total_attempt_question = 0
        if quiz_data.bank_line.quiz_id.que_required:
            for data in quiz_data:
                total_question = len(data.line_ids)
                for temp in data.line_ids:
                    if temp.name != '':
                        total_attempt_question += 1
            if total_attempt_question == total_question:
                return True
            else:
                return False


class OpeneducatQuizMultipleChoice(OpeneducatQuizRender):
    def get_quiz_result_data(self, values):
        res = super(OpeneducatQuizMultipleChoice,
                    self).get_quiz_result_data(values)
        result = request.env['op.quiz.result']. \
            sudo().browse(int(values['ExamID']))
        datafilter = list(filter(
            lambda i: i['que_type'] != 'multiple_choice',
            res['not_attempt_answer']))
        res['not_attempt_answer'] = datafilter
        for line in result.line_ids:
            if line.que_type == 'multiple_choice':
                temp_total_correct = 0
                total_attemp = 0
                total_question_line = len(line.multiple_choice_line_ids)
                for data in line.multiple_choice_line_ids:
                    if data.default_answer == data.given_answer:
                        temp_total_correct += 1
                if len(line.multiple_choice_line_ids) == total_attemp:
                    questiondata = []
                    for temp in line.multiple_choice_line_ids:
                        questiondata.append({
                            'given_answer': temp.given_answer,
                            'que_image': temp.que_image,
                            'que_text': temp.que_text,
                            'que_type': line.multiple_choice_que_type,
                            'default_answer': temp.default_answer,
                            'id': temp.id
                        })
                    res['not_attempt_answer'].append(
                        {'que_type': line.que_type,
                         'question': line.name,
                         'answer': line.answer or '',
                         'line_data': questiondata})

                elif(temp_total_correct == total_question_line):
                    questiondata = []
                    for temp in line.multiple_choice_line_ids:
                        questiondata.append({
                            'given_answer': temp.given_answer,
                            'que_image': temp.que_image,
                            'que_text': temp.que_text,
                            'que_type': line.multiple_choice_que_type,
                            'default_answer': temp.default_answer,
                            'id': temp.id
                        })
                    res['right_answers'].append(
                        {'que_type': line.que_type, 'question': line.name,
                         'answer': line.answer, 'line_data': questiondata})
                else:
                    questiondata = []
                    for temp in line.multiple_choice_line_ids:
                        questiondata.append({
                            'given_answer': temp.given_answer,
                            'que_image': temp.que_image,
                            'que_text': temp.que_text,
                            'que_type': line.multiple_choice_que_type,
                            'default_answer': temp.default_answer,
                            'id': temp.id
                        })
                    res['wrong_answer'].append(
                        {'que_type': line.que_type,
                         'question': line.name,
                         'given_answer': line.given_answer,
                         'answer': line.answer,
                         'line_data': questiondata})
        quiz = result.quiz_id
        if quiz.wrong_ans and res['wrong_answer']:
            res['display_wrong_ans'] = 1
        if quiz.right_ans and res['right_answers']:
            res['display_true_ans'] = 1
        if quiz.not_attempt_ans and res['not_attempt_answer']:
            res['not_attempt_ans'] = 1
        return res

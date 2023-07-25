from odoo import http
from odoo.http import request
import re
import random


class QuizMatchDragIntoText(http.Controller):

    @http.route('/DragIntoText', type='json', website=True, auth='user', csrf=False)
    def quiz_data(self, question_id=None):
        following_data = []

        quiz_data1 = request.env['op.quiz.result.line'].sudo().browse(int(question_id))
        option = []
        for data in quiz_data1:
            s = data.name
            for i in range(0, len(s)):
                if s[i] == '<' and s[i+1] == '<':
                    str1 = ""
                    for j in range(i+2, len(s)):
                        if s[j] == '>' and s[j+1] == '>':
                            i = j
                            option.append({
                                'option' : str1
                            })
                            break
                        str1 = str1 + s[j]
            random.shuffle(option)
            span = '<span class="drop_droptarget%s" id="option1"></span>' % str(data.id)
            question = re.sub('<<[^>]+>>', span, data.name)
            following_data.append({
                'question' : question,
                'option' : option,
                'id' : data.id,
                'que_required' : quiz_data1.bank_line.quiz_id.que_required
            })
        return following_data

    @http.route('/quiz/dragintotext/data', type='json',
                website=True, auth='user', csrf=False)
    def quiz_result(self , answerdata=None, question_id=None, examid=None):
        temp = request.env['op.quiz.result'].sudo().browse(int(examid))
        for data in temp.line_ids:
            if data.id == int(question_id):
                data.given_answer = answerdata

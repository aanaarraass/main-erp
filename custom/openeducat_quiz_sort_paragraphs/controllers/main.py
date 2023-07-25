from odoo import http
from odoo.http import request
import random


class Quiz(http.Controller):

    @http.route('/sort/paragraphs', type='json', website=True, auth='user',
                csrf=False)
    def quiz_data(self, question_id=None):
        question_data = []
        quiz_data1 = request.env['op.quiz.result.line'].sudo().browse(int(question_id))
        for data in quiz_data1:
            questiondata = []
            for temp in data.sort_paragraphs_line_ids:
                questiondata.append({
                    'given_answer' : temp.given_answer,
                    'default_answer' : temp.default_answer,
                    'line_id' : temp.id,
                })
            random.shuffle(questiondata)
            question_data.append({
                'id' : data.id,
                'que_type' : data.que_type,
                'name' : data.name,
                'question_data' : questiondata
            })
        return question_data

    @http.route(['/quiz/sortparagraphs/alldata'], type='json',
                website=True, auth='user', csrf=False)
    def quiz_following_answer(self, all_data=None):
        for data in all_data:
            if data['que_type'] == 'sort_paragraphs':
                answer_list = data['answer'].split('$$$')
                temp = request.env['op.quiz.result.line.sort.paragraphs'].sudo(). \
                    search([('line_id', '=', int(data['id']))])
                i = 0
                for ans in temp.line_id.sort_paragraphs_line_ids:
                    ans.given_answer = answer_list[i]
                    i = i+1

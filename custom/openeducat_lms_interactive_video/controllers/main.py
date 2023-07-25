from odoo import http
from odoo.http import request
from odoo.addons.openeducat_lms.controllers.main import OpenEduCatLms
from odoo.addons.openeducat_quiz.controllers.main import OpeneducatQuizRender


class LmsInteractiveVideo(OpeneducatQuizRender):
    @http.route(['/interactive/video'], type="json", auth="user",
                website=True, csrf=False)
    def interactive_video_data(self, video_id=None):
        data = request.env['op.material'].sudo().browse(int(video_id))
        time_data = []
        for record in data:
            if record.material_type == 'interactive_video':
                for video_data in record.interactive_video_line_ids:
                    time_data.append({
                        'question': video_data.question,
                        'data': video_data.full_description,
                        'time': (video_data.time)*60,
                        'id': video_data.id,
                        'quiz': video_data.quiz_id.id
                    })
        return time_data

    @http.route(['/interactive/quiz_data'], type="json", auth="user",
                website=True, csrf=False)
    def interactive_quiz_data(self, video_id=None):
        attempt_ids = request.env['op.quiz.result'].search([
            ('user_id', '=', request.env.uid), ('quiz_id', '=', video_id)])
        return attempt_ids.id

    @http.route(['/interactive/video/quiz'], type="json", auth="user",
                website=True, csrf=False)
    def interactive_video_quiz(self, video_id=None):
        attempt_ids = request.env['op.quiz.result'].search([
            ('user_id', '=', request.env.uid), ('quiz_id', '=', int(video_id))])
        for result in attempt_ids:
            attempt = result
        return request.env['ir.ui.view'].sudo(). \
            _render_template('openeducat_quiz.quiz_web_page_single_form', {
                'result': attempt, 'total_question': attempt.total_question})

    @http.route('/interactive/video/quiz/finish', type="json", auth="user",
                sitemap=False, website=True)
    def interactive_video_quiz_result(self, quiz_data):
        value = self.get_quiz_result_data(quiz_data)
        if value['not_attempt_answer']:
            value['not_attempt_ans'] = 1
        if value['wrong_answer']:
            value['display_wrong_ans'] = 1
        if value['right_answers']:
            value['display_true_ans'] = 1
        return request.env['ir.ui.view'].sudo().\
            _render_template('openeducat_quiz.quiz_results_form', value)


class LmsInteractiveVideoMaterial(OpenEduCatLms):
    @http.route()
    def get_course_material(self, course, section=None, material=None,
                            result=None, next_mat=0, **kwargs):
        res = super(LmsInteractiveVideoMaterial, self).get_course_material(
            course=course, section=section, material=material,
            result=result, next_mat=next_mat, **kwargs)
        if res.qcontext['response_template'] is not None:
            if res.qcontext['material'].material_type == 'interactive_video':
                for result in res.qcontext['material'].interactive_video_line_ids:
                    attempt_ids = request.env['op.quiz.result'].search([
                        ('user_id', '=', res.qcontext['user'].id),
                        ('quiz_id', '=', result.quiz_id.id)])
                    if not attempt_ids:
                        if result.interactive_video_type == 'quiz':
                            result.quiz_id.get_result_id()
                    else:
                        for attempt in attempt_ids:
                            attempt_result = attempt
                        if attempt_result.state == 'submit':
                            if result.interactive_video_type == 'quiz':
                                result.quiz_id.get_result_id()
        return res

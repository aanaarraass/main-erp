from odoo import http
from odoo.http import request


class WebTerminology(http.Controller):
    @http.route('/term/config', type='json', auth='user', website=True)
    def term_data(self, **vals):
        data = vals['dict']
        term_id = request.env['ir.config_parameter'].sudo(). \
            get_param('terminology_template')
        if term_id:
            term = request.env['terminology.configuration'].browse(int(term_id))
        else:
            request.env['ir.config_parameter'].sudo().set_param(
                'terminology_template', int(vals['id']))
            term = request.env['terminology.configuration'].browse(int(vals['id']))
        if data['course_new_label'] and data['course_new_label_plural']:
            term.label_change_query(term.base_course_label,
                                    data['course_new_label'],
                                    term.base_course_label_plural,
                                    data['course_new_label_plural'])

            term.label_change_query(term.course_old_label,
                                    data['course_new_label'],
                                    term.course_old_label_plural,
                                    data['course_new_label_plural'])

        if data['batch_new_label'] and data['batch_new_label_plural']:
            term.label_change_query(term.base_batch_label,
                                    data['batch_new_label'],
                                    term.base_batch_label_plural,
                                    data['batch_new_label_plural'])

            term.label_change_query(term.batch_old_label,
                                    data['batch_new_label'],
                                    term.batch_old_label_plural,
                                    data['batch_new_label_plural'])

        if data['subject_new_label'] and data['subject_new_label_plural']:
            term.label_change_query(term.base_subject_label,
                                    data['subject_new_label'],
                                    term.base_subject_label_plural,
                                    data['subject_new_label_plural'])

            term.label_change_query(term.subject_old_label,
                                    data['subject_new_label'],
                                    term.subject_old_label_plural,
                                    data['subject_new_label_plural'])

        if data['student_new_label'] and data['student_new_label_plural']:
            term.label_change_query(term.base_student_label,
                                    data['student_new_label'],
                                    term.base_student_label_plural,
                                    data['student_new_label_plural'])

            term.label_change_query(term.student_old_label,
                                    data['student_new_label'],
                                    term.student_old_label_plural,
                                    data['student_new_label_plural'])

        if data['faculty_new_label'] and data['faculty_new_label_plural']:
            term.label_change_query(term.base_faculty_label,
                                    data['faculty_new_label'],
                                    term.base_faculty_label_plural,
                                    data['faculty_new_label_plural'])

            term.label_change_query(term.faculty_old_label,
                                    data['faculty_new_label'],
                                    term.faculty_old_label_plural,
                                    data['faculty_new_label_plural'])

# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo.http import request
from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal


class SubjectRegistrationPortal(CustomerPortal):
    @http.route(['/subject/registration/create/',
                 '/subject/registration/create/<int:student_id>',
                 '/subject/registration/create/<int:page>'],
                type='http', auth="user", website=True)
    def portal_craete_subject_registration(self, student_id=None, **kw):

        user = request.env.user
        student_id = request.env['op.student'].sudo().search([
            ('user_id', '=', user.id)])

        elective_subjects = request.env['op.subject'].sudo().search(
            [('subject_type', '=', 'elective')])

        course_ids = request.env['op.course'].sudo().search([])

        year_ids = request.env['op.academic.year'].sudo().search([])
        term_ids = request.env['op.academic.term'].sudo().search([])
        course_credit = request.env['course.credit'].sudo().search([])

        lms_module = request.env['ir.module.module'].sudo().search(
            [('name', '=', 'openeducat_lms')])

        if lms_module.state != 'uninstalled':
            course_ids = request.env['op.course'].sudo().search(
                [('online_course', '!=', True)])

        batch_ids = request.env['op.batch'].sudo().search([])

        return request.render(
            "openeducat_core_enterprise."
            "openeducat_create_subject_registration",
            {'student_id': student_id,
             'subject_registration_ids': elective_subjects,
             'course_ids': course_ids,
             'year_ids': year_ids,
             'term_ids': term_ids,
             'course_credit': course_credit,
             'batch_ids': batch_ids,
             'page_name': 'subject_reg_form'
             })

    @http.route(['/subject/registration/submit',
                 '/subject/registration/submit/<int:page>'],
                type='http', auth="user", website=True)
    def portal_submit_subject_registration(self, **kw):

        compulsory_subject = request.httprequest. \
            form.getlist('compulsory_subject_ids')
        elective_subject = request.httprequest. \
            form.getlist('elective_subject_ids')
        vals = {
            'student_id': kw['student_id'],
            'course_id': kw['course_id'],
            'batch_id': kw['batch_id'],
            'min_unit_load': kw['min_unit_load'],
            'max_unit_load': kw['max_unit_load'],
            'compulsory_subject_ids': [[6, 0, compulsory_subject]],
            'elective_subject_ids': [[6, 0, elective_subject]],
        }
        registration_id = request.env['op.subject.registration']
        registration_id.sudo().create(vals).action_submitted()

        return request.redirect('/subject/registration/')

    @http.route(['/subject/registration/check'],
                type='json', auth="user", website=True)
    def portal_submit_subject_check_registration(self, **kw):
        compulsory_subject = kw['compulsory_subject_ids']
        compulsory_subject += kw['elective_subject_ids']
        credit_list = []

        subject = request.env['op.subject'].sudo().search([
            ('id', 'in', compulsory_subject)])

        course_credit = request.env['course.credit'].sudo().search([
            ('course_id.id', '=', kw['course_id'])])
        if course_credit.all_academic == 'general':
            return False
        else:
            course_credit = request.env['course.credit'].sudo().search([
                ('course_id.id', '=', kw['course_id']),
                ('academic_year_id.id', '=', kw['year_ids'])])
            for credit in course_credit.sem_credit_line_id:
                for sub_cred in credit.subject_credit:
                    if sub_cred.subject_id in subject:
                        credit_list.append(sub_cred.credit)
                if str(credit.semester_id.id) == kw['term_ids']:
                    if credit.min_credit <= sum(credit_list) <= credit.max_credit:
                        return False
                    else:
                        return 'Subject credit must not be ' \
                               'less than {} and more than {}'.\
                            format(credit.min_credit, credit.max_credit)
        return False

    @http.route(['/get/course_data'],
                type='json', auth="none", website=True)
    def get_course_data(self, course_id, **kw):
        batch_list = []
        subject_list = []
        credit_course = request.env['course.credit'].sudo().search([
            ('course_id', '=', int(course_id))])

        batch_ids = request.env['op.batch'].sudo().search(
            [('course_id', '=', int(course_id))])
        subject_ids = request.env['op.subject'].sudo().search([
            ('course_id', '=', int(course_id))])
        if batch_ids:
            for batch_id in batch_ids:
                batch_list.append({'name': batch_id.name,
                                   'id': batch_id.id})
        if subject_ids:
            for subject_id in subject_ids:
                if credit_course.all_academic == 'general':
                    for cre in credit_course.subject_credit:
                        if cre.subject_id == subject_id:
                            subject_list.\
                                append({
                                    'name': subject_id.name + '-' + str(
                                        cre.credit),
                                    'id': subject_id.id})
                else:
                    for cre in credit_course.sem_credit_line_id:
                        for sub_cre in cre.subject_credit:
                            if sub_cre.subject_id == subject_id:
                                if sub_cre.subject_id.subject_type == 'compulsory':
                                    subject_list.\
                                        append({
                                            'name': subject_id.name + '-' + str(
                                                sub_cre.credit),
                                            'id': subject_id.id})
        return {'batch_list': batch_list,
                'subject_list': subject_list}

    @http.route('/get/subject/total', type='json', website=True, auth='user')
    def get_subject_credit_total(self, **kw):
        crd_lst = []
        compulsory_subject = kw['compulsory_subject_ids']
        compulsory_subject += kw['elective_subject_ids']

        credit_course = request.env['course.credit'].sudo().search([
            ('course_id', '=', int(kw.get('course_id')))])
        if credit_course.all_academic == 'general':
            for cre in credit_course.subject_credit:
                if cre.subject_id.id in compulsory_subject:
                    crd_lst.append(cre.credit)
        else:
            for cre in credit_course.sem_credit_line_id:
                for sub_cre in cre.subject_credit:
                    if sub_cre.subject_id.id in compulsory_subject:
                        crd_lst.append(sub_cre.credit)

        return sum(crd_lst)

# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo.http import request
from odoo import http
from odoo.addons.openeducat_cbcs.controllers.main import SubjectRegistrationPortal


class SubjectRegistrationCreditPortal(SubjectRegistrationPortal):

    @http.route()
    def portal_submit_subject_check_registration(self, **kw):
        res = super(SubjectRegistrationCreditPortal, self).\
            portal_submit_subject_check_registration(**kw)
        if res is False:
            compulsory_subject = kw['compulsory_subject_ids']
            elective_subject = kw['elective_subject_ids']

            new_subjects = compulsory_subject + elective_subject
            student = (
                request.env["op.student"].sudo().search([
                    ("user_id", "=", request.env.user.id)])
            )
            subject_lst = request.env['op.subject'].sudo().search([
                ('id', 'in', new_subjects)])
            old_subjects = []
            for subject in student.course_detail_ids:
                for sub in subject.subject_ids:
                    old_subjects.append(sub.id)

            for check_sub in subject_lst:
                if check_sub.required_subject:
                    for i in check_sub.required_subject:
                        if i.subject_id.id in old_subjects:
                            return res
                        else:
                            return 'Subject {} is ' \
                                   'required for {}'.\
                                format(i.subject_id.name, check_sub.name)
        return res


# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import http
from odoo.http import request


class StudentAttendance(http.Controller):

    @http.route('/face-recognition/student/attendance', auth='user', type='json')
    def student_attendance_(self, **kw):
        labels_ids = []
        images_ids = request.env['op.student'].search(
            [('descriptor', '!=', False)])
        details = {}
        for image in images_ids:
            name = '%s %s %s' % (image.first_name, image.middle_name,
                                 image.last_name)
            labels_ids.append(name)
            details[name] = image.id

        descriptor_ids = images_ids.mapped('descriptor')
        return {
            'descriptor_ids': descriptor_ids,
            'labels_ids': labels_ids,
            'details': details
        }

    @http.route('/face-recognition/get/sheetdata', type='json', auth='user')
    def get_sheet_data(self, **kw):
        sheet_id = request.env['op.attendance.sheet'].sudo()\
            .search([('state', '=', 'draft')])
        sheet_list = []
        for sheet in sheet_id:
            sheet_list.append({'id': sheet.id, 'name': sheet.name})
        return sheet_list

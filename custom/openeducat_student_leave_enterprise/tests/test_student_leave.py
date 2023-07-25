# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from .test_student_leave_common import TestStudentLeaveCommon
from datetime import datetime, timedelta


class TestNoticeBoard(TestStudentLeaveCommon):
    def setUp(self):
        super(TestNoticeBoard, self).setUp()

    def test_01_student_leave(self):
        leave_type_data = {
            'name': 'Official Leave',
            'code': 'official'
        }

        leave_type_create = self.leave_types.create(leave_type_data)

        leave_data = {
            'student_id': self.ref('openeducat_core.op_student_3'),
            'faculty_id': self.ref('openeducat_core.op_faculty_1'),
            'leave_type': leave_type_create.id,
            'description': 'I need a leave for Medical Emergency in Family.',
            'start_date': datetime.today().date() + timedelta(days=10),
            'end_date': datetime.today().date() + timedelta(days=12),
        }

        student_leaves = self.student_leave_request.search([])

        for leave in student_leaves:
            if leave.state == 'confirm':
                leave.action_validate()
            if leave.state == 'validate':
                leave.action_approve()

        leave_create = self.student_leave_request.create(leave_data)

        leave_create.action_confirm()
        leave_create.action_validate()
        leave_create.action_cancel()

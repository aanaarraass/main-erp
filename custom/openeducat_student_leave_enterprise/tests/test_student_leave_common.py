# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo.tests import TransactionCase
from odoo.tests.common import HttpCase, tagged


class TestStudentLeaveCommon(TransactionCase):
    def setUp(self):
        super(TestStudentLeaveCommon, self).setUp()
        self.leave_types = self.env['student.leave.type']
        self.student_leave_request = self.env['student.leave.request']


@tagged('post_install', '-at_install')
class TestUi(HttpCase):

    def setUp(self):
        super(TestUi, self).setUp()
        student = self.env['res.users'].search(
            [('login', '=', 'student@openeducat.com')])
        student.login = "student"
        parent = self.env['res.users'].search(
            [('login', '=', 'parent@openeducat.com')])
        parent.login = "parent"

    def test_01_student_leave_request(self):
        self.start_tour("/", "student_leave_list", login="student")
        self.start_tour("/", "student_leave_request", login="student")

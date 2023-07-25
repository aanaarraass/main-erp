
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################
from odoo.tests import common
import odoo.tests
from ..controller import main


class SubjectMaterialTest(common.TransactionCase):
    def setUp(self):
        super(SubjectMaterialTest, self).setUp()


class TestSubjectMaterialAllocation(main.SubjectMaterialAllocation):
    def subject_material_allocation(self):
        self.subject_material = main.SubjectMaterialAllocation()
        self.subject_material._prepare_portal_layout_values()
        self.subject_material._parent_prepare_portal_layout_values(student_id=1)


@odoo.tests.tagged('post_install', '-at_install')
class TestUi(odoo.tests.HttpCase):
    def setUp(self):
        super(TestUi, self).setUp()
        student = self.env['res.users'].search(
            [('login', '=', 'student@openeducat.com')])
        student.login = "student"
        parent = self.env['res.users'].search(
            [('login', '=', 'parent@openeducat.com')]
        )
        parent.login = "parent"

    def test_01_subject_details(self):
        self.start_tour("/", "test_student_subject_details", login="student")
        self.start_tour("/", "test_student_subject_details", login="parent")

    def test_02_subject_material_details(self):
        self.start_tour("/", "test_subject_material_details", login="student")
        self.start_tour("/", "test_subject_material_details", login="parent")

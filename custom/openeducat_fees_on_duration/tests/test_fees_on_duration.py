
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################


from .common import TestFeesTermExtCommon


class TestOpAdmission(TestFeesTermExtCommon):

    def setUp(self):
        super(TestOpAdmission, self).setUp()

    def test_enroll_student(self):
        vals = {
            'student_id': self.env.ref('openeducat_core.op_student_6').id,
            'course_id': self.env.ref('openeducat_core.op_course_3').id,
            'batch_id': self.env.ref('openeducat_core.op_batch_1').id,
            'fees_term_id': self.env.ref('openeducat_fees.op_fees_term_6').id,
        }
        data = self.op_student_course.create(vals)

        for rec in data:
            rec.cron_create_invoice()

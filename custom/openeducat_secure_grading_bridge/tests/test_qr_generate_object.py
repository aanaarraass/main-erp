# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################
from logging import info
from .test_qr_generate_common import QRGenerateTestCommon


class QRGenerateTestObject(QRGenerateTestCommon):
    def setUp(self):
        super(QRGenerateTestObject, self).setUp()

    def test_qr_generation(self):
        super(QRGenerateTestObject, self).test_data()
        grade_book = self.grade_book.create({
            'student_id': self.env.ref('openeducat_core.op_student_9').id,
            'course_id': self.env.ref('openeducat_core.op_course_2').id,
            'academic_year_id':
                [(6, 0, [self.env.ref(
                    'openeducat_core.academic_year_1').id, self.env.ref(
                    'openeducat_core.academic_year_2').id])],
        })
        if grade_book.hash_key:
            info('      QR Code: %s' % grade_book.hash_key)

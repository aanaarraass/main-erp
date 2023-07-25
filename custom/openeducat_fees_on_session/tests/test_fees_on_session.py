
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################


from .common import TestFeesTermExtCommon


class TestOpAttendanceSheet(TestFeesTermExtCommon):

    def setUp(self):
        super(TestOpAttendanceSheet, self).setUp()

    def test_attendance_done(self):
        attendance_obj = self.op_attendance_sheet.search([])

        for rec in attendance_obj:
            rec.attendance_done()

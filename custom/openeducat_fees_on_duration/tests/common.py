
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo.tests import common


class TestFeesTermExtCommon(common.TransactionCase):

    def setUp(self):
        super(TestFeesTermExtCommon, self).setUp()
        self.op_student_course = self.env['op.student.course']

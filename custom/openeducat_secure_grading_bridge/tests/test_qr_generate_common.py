# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################
from odoo.tests.common import TransactionCase


class QRGenerateTestCommon(TransactionCase):
    def setUp(self):
        super(QRGenerateTestCommon, self).setUp()

    def test_data(self):
        self.grade_book = self.env['gradebook.gradebook']

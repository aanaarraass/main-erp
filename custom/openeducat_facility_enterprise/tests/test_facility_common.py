
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo.tests import common


class TestFacilityCommon(common.TransactionCase):
    def setUp(self):
        super(TestFacilityCommon, self).setUp()
        self.op_facility = self.env['op.facility']
        self.op_facility_line = self.env['op.facility.line']

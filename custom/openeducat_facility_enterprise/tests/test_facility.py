
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

import logging

from .test_facility_common import TestFacilityCommon


class TestFacility(TestFacilityCommon):

    def setUp(self):
        super(TestFacility, self).setUp()

    def test_case_facility(self):
        types = self.op_facility.search([])
        for facility in types:
            logging.info('Name : %s' % facility.company_id.name)


class TestFacilityLine(TestFacilityCommon):

    def setUp(self):
        super(TestFacilityLine, self).setUp()

    def test_case_facility_line(self):
        res_company = self.env['res.company'].search([], limit=1)
        facility = self.env['op.facility'].search([], limit=1)

        types = self.op_facility_line.create({
            'facility_id': facility.id,
            'quantity': '1.0',
            'company_id': res_company.id
        })
        for facilityline in types:
            logging.info('Name : %s' % facilityline.company_id.name)

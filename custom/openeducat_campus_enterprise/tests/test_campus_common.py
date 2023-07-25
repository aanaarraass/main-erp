
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo.tests import common, TransactionCase
from ..controller import onboard
from odoo.addons.website.tools import MockRequest


class TestCampusCommon(common.TransactionCase):
    def setUp(self):
        super(TestCampusCommon, self).setUp()
        self.campus_onboard = self.env['res.company']
        self.op_campus_facility = self.env['op.campus.facility']
        self.facility_invoice = self.env['facility.invoice']


class CampusContollerTests(TransactionCase):

    def setUp(self):
        super().setUp()
        self.campuscontroller = onboard.OnboardingController()


class TestCampusController(CampusContollerTests):

    def setUp(self):
        super(TestCampusController, self).setUp()

    def test_case_alumni_group(self):
        self.campuscontroller = onboard.OnboardingController()

        with MockRequest(self.env):
            self.onboard = self.campuscontroller. \
                openeducat_campus_enterprise_onboarding_panel()

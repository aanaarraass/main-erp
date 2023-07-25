
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo.tests import common, TransactionCase
from odoo.addons.website.tools import MockRequest
from ..controllers import onboard, main
import odoo.tests


class TestLibraryCommon(common.TransactionCase):
    def setUp(self):
        super(TestLibraryCommon, self).setUp()
        self.op_media_type = self.env['op.media.type']
        self.op_media_queue = self.env['op.media.queue']
        self.op_media_movement = self.env['op.media.movement']
        self.op_media = self.env['op.media']
        self.op_media_publisher = self.env['op.publisher']
        self.op_library_card = self.env['op.library.card']
        self.op_library_card_type = self.env['op.library.card.type']
        self.op_media_author = self.env['op.author']
        self.op_company = self.env['res.company']
        self.barcode_issue_media = self.env['barcode.issue.media']


class LibraryControllerTests(TransactionCase):
    def setUp(self):
        super(LibraryControllerTests, self).setUp()
        self.LibraryController = onboard.OnboardingController()


class TestLibraryController(LibraryControllerTests):

    def setUp(self):
        super(TestLibraryController, self).setUp()

    # def test_case_library_onboarding(self):
    #     self.LibraryController = onboard.OnboardingController()
    #     with MockRequest(self.env):
    #         self.cookies = \
    #             self.LibraryController.openeducat_library_onboarding_panel()


class LibraryDashboardControllerTests(TransactionCase):
    def setUp(self):
        super(LibraryDashboardControllerTests, self).setUp()
        self.DashboardController = main.OpenEduCatLibraryController()


class TestLibraryDashboardController(LibraryDashboardControllerTests):

    def setUp(self):
        super(TestLibraryDashboardController, self).setUp()

    def test_case_library_dashboard(self):
        self.DashboardController = main.OpenEduCatLibraryController()
        with MockRequest(self.env):
            self.cookies = \
                self.DashboardController.compute_library_dashboard_data()


@odoo.tests.tagged('post_install', '-at_install')
class TestUi(odoo.tests.HttpCase):

    def setUp(self):
        super(TestUi, self).setUp()
        stud = self.env['res.users'].search(
            [('login', '=', 'student@openeducat.com')])
        stud.login = 'student'
        parent = self.env['res.users'].search(
            [('login', '=', 'parent@openeducat.com')])
        parent.login = 'parent'

    def test_library_media(self):
        self.start_tour("/", "library_media", login="student")
        self.start_tour("/", "library_media", login="parent")

    def test_media_request(self):
        self.start_tour("/", "test_media_queue_request", login="student")

    def test_media_purchase_request(self):
        self.start_tour("/", "test_media_purchase_request", login="student")

    def test_media_purchase_list(self):
        self.start_tour("/", "media_purchase_list", login="student")

    def test_media_movement_list(self):
        self.start_tour("/", "media_movement_list", login="student")
        self.start_tour("/", "media_movement_list", login="parent")

    # def test_media_movement_information(self):
    #     self.start_tour("/", "media_movement_information", login="student")

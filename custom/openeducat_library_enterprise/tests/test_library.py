
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from logging import info

from .test_library_common import TestLibraryCommon


class TestMediaType(TestLibraryCommon):

    def setUp(self):
        super(TestMediaType, self).setUp()

    def test_case_media_type(self):
        mediatype = self.op_media_type.search([])
        if not mediatype:
            raise AssertionError(
                'Error in data, please check for media type details')
        info('  Details Of Media Type:.....')
        for record in mediatype:
            record._compute_issued()
            record._compute_available()
            record._compute_total_copies()
            record._compute_due_media_today()
            record._compute_due_media_month()
            record._compute_kanban_dashboard_graph()
            record.get_bar_graph_datas()
            record.create_new_media_type()
            record.action_onboarding_media_type_layout()


class TestMediaQueue(TestLibraryCommon):

    def setUp(self):
        super(TestMediaQueue, self).setUp()

    def test_case_media_queue(self):
        mediaqueue = self.op_media_queue.search([])
        if not mediaqueue:
            raise AssertionError(
                'Error in data, please check for media queue date details')
        info('  Details Of Media Queue:.....')
        for record in mediaqueue:
            record._check_date()


class TestMediaMovement(TestLibraryCommon):

    def setUp(self):
        super(TestMediaMovement, self).setUp()

    def test_case_media_movement(self):
        movement = self.op_media_movement.search([])
        if not movement:
            raise AssertionError(
                'Error in data, please check for media queue date details')
        info('  Details Of Media Movement:.....')
        for record in movement:
            record._compute_media_count()
            record.renew_media()


class TestMedia(TestLibraryCommon):

    def setUp(self):
        super(TestMedia, self).setUp()

    def test_case_media(self):
        media = self.op_media.search([])
        if not media:
            raise AssertionError(
                'Error in data, please check for total media units')
        info('  Total Media Units:.....')
        for record in media:
            record._compute_total_units()


class TestPublisher(TestLibraryCommon):

    def setUp(self):
        super(TestPublisher, self).setUp()

    def test_case_publisher(self):
        publisher = self.op_media_publisher.search([])
        if not publisher:
            raise AssertionError(
                'Error in data, please check for onboarding function')
        info('  Onboarding Publisher Layout:.....')
        for record in publisher:
            record.action_onboarding_publisher_layout()


class TestLibraryCard(TestLibraryCommon):

    def setUp(self):
        super(TestLibraryCard, self).setUp()

    def test_case_library_card(self):
        card = self.op_library_card.search([])
        if not card:
            raise AssertionError(
                'Error in data, please check for onboarding function')
        info('  Onboarding Library Card Layout:.....')
        for record in card:
            record.action_onboarding_library_card_layout()


class TestLibraryCardType(TestLibraryCommon):

    def setUp(self):
        super(TestLibraryCardType, self).setUp()

    def test_case_library_card_type(self):
        card_type = self.op_library_card_type.search([])
        if not card_type:
            raise AssertionError(
                'Error in data, please check for onboarding function')
        info('  Onboarding Library Card Type Layout:.....')
        for record in card_type:
            record.action_onboarding_library_card_type_layout()


class TestMediaAuthor(TestLibraryCommon):

    def setUp(self):
        super(TestMediaAuthor, self).setUp()

    def test_media_author(self):
        author = self.op_media_author.search([])
        if not author:
            raise AssertionError(
                'Error in data, please check for onboarding function')
        info('  Onboarding Author Layout:.....')
        for record in author:
            record.action_onboarding_author_layout()


class TestCompany(TestLibraryCommon):

    def setUp(self):
        super(TestCompany, self).setUp()

    def test_company(self):
        company = self.op_company.search([])
        if not company:
            raise AssertionError(
                'Error in data, please check for onboarding function')
        info('  Library Onboarding Panel:.....')
        for record in company:
            record.action_close_library_panel_onboarding()
            record.action_onboarding_library_card_layout()
            record.action_onboarding_publisher_layout()
            record.action_onboarding_author_layout()
            record.action_onboarding_media_type_layout()
            record.action_onboarding_library_card_type_layout()
            record.update_library_onboarding_state()


class TestWizardIssueMedia(TestLibraryCommon):

    def setUp(self):
        super(TestWizardIssueMedia, self).setUp()

    def test_wizard_issue_media(self):
        wizard = self.barcode_issue_media.create({
            'transaction_type': 'issue',
            'media_unit_number':
                self.env.ref('openeducat_library.op_media_unit_3').barcode,
            'library_card_number':
                self.env.ref('openeducat_library.op_library_card_1').number
        })
        info('  Wizard Issue Media:.....')
        wizard.barcode_do_issue()

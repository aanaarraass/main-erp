# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################


from odoo.tests.common import TransactionCase
import odoo.tests


class RequestAssetsCommon(TransactionCase):
    def setUp(self):
        super(RequestAssetsCommon, self).setUp()

    def test_data(self):
        self.request_asset = self.env['account.asset.request']
        self.request_reason = self.env['asset.request.reason']


@odoo.tests.tagged('post_install', '-at_install')
class TestUi(odoo.tests.HttpCase):

    def setUp(self):
        super(TestUi, self).setUp()
        student = self.env['res.users'].search(
            [('login', '=', 'student@openeducat.com')])
        student.login = "student"
        parent = self.env['res.users'].search(
            [('login', '=', 'parent@openeducat.com')])
        parent.login = "parent"

    def test_asset_request_detail(self):
        self.start_tour("/", 'test_asset_request_detail', login="student")
        self.start_tour("/", 'test_asset_request_detail', login="parent")

    def test_asset_request_student(self):
        self.start_tour("/", 'test_asset_request_student', login="student")

    def test_asset_request(self):
        self.start_tour("/", 'test_asset_request', login="student")
        self.start_tour("/", 'test_asset_request', login="parent")

    def test_asset_request_submit(self):
        self.start_tour("/", 'test_request_asset_submit', login="student")

# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################


import datetime
from .test_request_assets_common import RequestAssetsCommon


class RequestAssetTestObject(RequestAssetsCommon):
    def setUp(self):
        super(RequestAssetTestObject, self).setUp()

    def test_request_assets(self):
        asset_record = self.env['account.asset.request'].create({
            'request_for': 'student',
            'student_id': self.env.ref('openeducat_core.op_student_1').id,
            'request_reason_id': self.env.ref('openeducat_asset_request_enterprise.'
                                              'asset_request_reason_1').id,
            'request_date': datetime.date.today(),
            'state': 'draft',
            'requested_asset': 'computer'
        })
        account_account = self.env['account.account'].create({
            'code': '10123',
            'name': 'Real Assets',
            'user_type_id': self.env.ref('account.data_account_type_current_assets').id
        })
        account_journals = self.env['account.journal']. \
            search([('name', '=', 'Vendor Bills')])
        account_assets_categories = []
        for account_journal in account_journals:
            account_assets_categories.append(self.env['account.asset.category'].create({
                'name': 'Computer',
                'journal_id': account_journal.id,
                'account_asset_id': account_account.id,
                'account_depreciation_id': account_account.id,
                'account_depreciation_expense_id': account_account.id,
            }))
        analytic_account = self.env['account.analytic.account'].create({
            'name': 'Analytic Account'
        })
        account_assets = []
        for account_assets_category in account_assets_categories:
            account_assets.append(self.env['account.asset.asset'].create({
                'name': 'PHILIPS',
                'category_id': account_assets_category.id,
                'code': 'philips',
                'value': 0.00,
                'value_residual': 0.00,
                'date': datetime.datetime.today().date(),
                'date_first_depreciation': 'manual',
                'first_depreciation_manual_date': datetime.datetime.today().date(),
                'account_analytic_id': analytic_account.id
            }))

        for data in asset_record:
            for account_asset in account_assets:
                data.student_or_faculty()
                data.approved_progressbar()
                data.asset_id = account_asset.id
                data.allocate_progressbar()


# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo.tests import common


class TestHealthCommon(common.TransactionCase):
    def setUp(self):
        super(TestHealthCommon, self).setUp()
        self.op_health = self.env['op.health']
        self.op_health_line = self.env['op.health.line']

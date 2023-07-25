
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo.tests import common


class TestAchievementCommon(common.TransactionCase):
    def setUp(self):
        super(TestAchievementCommon, self).setUp()
        self.op_achievement_type = self.env['op.achievement.type']
        self.op_achievement = self.env['op.achievement']
        self.op_progression_achievement = self.env['op.student.progression']
        self.op_progression_wizard = self.env['achievement.progress.wizard']

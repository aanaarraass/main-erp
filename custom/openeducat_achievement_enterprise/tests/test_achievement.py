
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from logging import info

from .test_achievement_common import TestAchievementCommon


class TestAchievement(TestAchievementCommon):

    def setUp(self):
        super(TestAchievement, self).setUp()

    def test_case_achievement_1(self):
        achievement = self.op_achievement.search([])
        if not achievement:
            raise AssertionError(
                'Error in data, please check for reference ')
        for record in achievement:
            info('      Progression No : %s' % record.progression_id.name)
            info('      Student : %s' % record.student_id.name)
            info('      Faculty : %s' %
                 record.faculty_id.name)
            info('      Achievement Type : %s' %
                 record.achievement_type_id.name)
            info('      Description : %s' % record.description)
            info('      Date : %s' % record.achievement_date)
            record.onchange_student_achievement_progrssion()

    def test_case_1_achievement_type(self):
        achievement_type = self.op_achievement_type.search([])
        if not achievement_type:
            raise AssertionError(
                'Error in data, please check for achievement_type')
        info('Details of achievement_type')
        info('  Name     :   Code')
        for category in achievement_type:
            info('%s :    %s' % (category.name, category.code))

    def test_case_progression_achievement_1(self):
        progression_achievement = \
            self.op_progression_achievement.search([])
        for record in progression_achievement:
            info('      Achievements : %s' %
                 record.achievement_lines.achievement_type_id.name)
            info('      Total Achievement Counts : %s' %
                 record.total_achievement)
            record._compute_total_achievemenet()

    def test_case_1_progression_wizard(self):
        progression = self.op_progression_wizard.create({
            'student_id': self.env.ref('openeducat_core.op_student_1').id,
        })
        progression._get_default_student()

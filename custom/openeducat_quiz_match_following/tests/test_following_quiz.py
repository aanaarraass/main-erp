# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

import logging

from ...openeducat_quiz.tests.test_quiz_common import TestQuizCommon


class TestFollowingQuiz(TestQuizCommon):

    def setUp(self):
        super(TestFollowingQuiz, self).setUp()

    def check_data(self, msg, first_value, quiz_ref):
        if first_value != self.env.ref(quiz_ref):
            raise AssertionError(
                'Error in data, please check %s for referenced: '
                '%s' % (msg, quiz_ref))

    def check_config(self, quiz_config):
        config_list = ['normal', 'quiz_bank_selected', 'quiz_bank_random']
        if quiz_config not in config_list:
            raise AssertionError(
                'Error in data, %s is not valid please check Configuration '
                'for reference : openeducat_quiz_match_following.following_quiz1'
                % quiz_config)

    def test_case_4_quiz_1(self):
        quiz = self.env.ref('openeducat_quiz_match_following.following_quiz1')
        if not quiz:
            raise AssertionError(
                'Error in data, please check for reference : '
                'openeducat_quiz_match_following.following_quiz1')
        info = logging.info
        info('Details of Quiz :: %s' % quiz.name)
        self.check_data('Category', quiz.categ_id,
                        'openeducat_quiz_match_following.following_op_qz_ctg_b')
        info('Category : %s' % quiz.categ_id.name)
        self.check_config(quiz.quiz_config)
        info('Confguration: %s' % quiz.quiz_config)


class TestFollowingQuizOnboard(TestQuizCommon):

    def setUp(self):
        super(TestFollowingQuizOnboard, self).setUp()

    def test_quiz_onboard(self):
        quiz = self.quiz_onboard.search([])

        quiz.action_close_quiz_panel_onboarding()
        quiz.action_onboarding_quiz_layout()
        quiz.action_onboarding_question_bank_layout()
        quiz.update_quiz_onboarding_state()

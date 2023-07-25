
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields


class OpCourse(models.Model):
    _inherit = "op.course"

    subject_selection_option = fields.Selection([('regular', ' Regular'),
                                                 ('credit_based', 'Credit Based'),
                                                 ('subject_based', 'Subject Based')],
                                                string="Subject Selection",
                                                default='regular')

    def course_credit(self):
        action = self.env.ref('openeducat_cbcs.'
                              'act_open_course_credit_view').read()[0]
        action['domain'] = [('course_id', 'in', self.ids)]
        return action

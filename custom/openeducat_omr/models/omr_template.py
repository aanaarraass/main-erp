# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields


class OpOmrTemplate(models.Model):
    _name = 'op.omr.template'
    _inherit = ['mail.thread']
    _description = "Omr Template"
    _rec_name = 'name'

    name = fields.Char(string="Template Name", readonly=True)
    question_option = fields.Selection(string='Question Options', selection=[
        ('4', '4 Option'), ('5', '5 Option')], default='4', readonly=True)
    json_data = fields.Char(string="json data", readonly=True)

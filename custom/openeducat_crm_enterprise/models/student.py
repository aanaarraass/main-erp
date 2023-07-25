# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields, api


class OpStudent(models.Model):
    _inherit = "op.student"

    crm_lead_ids = fields.One2many(
        'crm.lead', 'student_id', 'CRM Leads')
    crm_lead_count = fields.Integer(compute="_compute_crm_lead_details")

    @api.depends('crm_lead_ids')
    def _compute_crm_lead_details(self):
        for crm in self:
            crm.crm_lead_count = self.env['crm.lead'].search_count([
                ('student_id', '=', self.id)])

    def count_crm_lead(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'CRM Lead',
            'view_mode': 'tree,form',
            'res_model': 'crm.lead',
            'domain': [('student_id', '=', self.id)],
            'target': 'current',
        }

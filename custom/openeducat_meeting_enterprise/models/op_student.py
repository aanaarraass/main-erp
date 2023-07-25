
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, api


class OpStudent(models.Model):
    _inherit = "op.student"

    @api.model
    def create(self, vals):
        res = super(OpStudent, self).create(vals)
        students = self.env['res.partner.category'].search(
            [('name', '=', 'Student')])
        partner_id = res.partner_id
        partner_id.write({'category_id': [(6, 0, students.ids)]}),
        return res

# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################


from odoo import models, fields, api, _
import datetime
from odoo.exceptions import ValidationError


class RequestAssets(models.Model):
    _name = "account.asset.request"
    _inherit = ['mail.thread']
    _description = "Asset Requests"

    def approved_progressbar(self):

        self.write({
            'state': 'approved',
            'approve_date': datetime.date.today(),

        })

    def reject_progressbar(self):
        self.write({
            'state': 'rejected',
            'reject_date': datetime.date.today(),

        })

    def allocate_progressbar(self):
        if not self.asset_id:
            raise ValidationError(_("Please select Asset"))
        else:
            self.write({
                'state': 'allocate',
                'allocate_date': datetime.date.today(),
            })
            self.asset_id.assign_state = True

    def return_progressbar(self):
        self.asset_id.assign_state = False
        self.write({
            'state': 'returned',
            'return_date': datetime.date.today(),
        })

    @api.onchange("request_for")
    def student_or_faculty(self):
        if self.request_for == 'student':
            self.faculty_id = None

        if self.request_for == 'faculty':
            self.student_id = None

    name = fields.Char(readonly=True)
    request_for = fields.Selection([('student', 'Student'), (
        'faculty', 'Faculty')], string="Request By", default="student", required=True)
    student_id = fields.Many2one(
        'op.student', string="Student")
    faculty_id = fields.Many2one('op.faculty', string="Faculty")
    request_reason_id = fields.Many2one('asset.request.reason', string="Reason",
                                        required=True, index=True,
                                        tracking=True)
    request_date = fields.Date(default=datetime.date.today())
    approve_date = fields.Date(string="Approve Date")
    allocate_date = fields.Date(string="Allocate Date", index=True, tracking=True)
    return_date = fields.Date(string="Return Date", index=True, tracking=True)
    reject_date = fields.Date(string="Reject Date")
    asset_id = fields.Many2one('account.asset.asset', string="Assets",
                               domain=[('assign_state', '=', False)],
                               index=True, tracking=True)
    requested_asset = fields.Char(string="Requested Asset", required=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('approved', 'Approved'),
         ('rejected', 'Rejected'), ('allocate', 'Allocated'),
         ('returned', 'Returned')], default="draft", index=True, tracking=True)
    color = fields.Integer('Color Index', default=1)

    @api.model
    def create(self, vals):

        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('request.sequence')
            vals.update({'name': seq})
            result = super(RequestAssets, self).create(vals)
            return result

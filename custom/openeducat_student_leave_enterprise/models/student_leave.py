# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError
from datetime import datetime


class StudentLeaveRequest(models.Model):
    _name = "student.leave.request"
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']
    _description = "Student Leave Request"
    _rec_name = "student_id"

    description = fields.Text(string="Description", required=True)
    leave_type = fields.Many2one("student.leave.type", required=True)
    start_date = fields.Datetime(string="Start Date",
                                 default=datetime.today(), tracking=True, required=True)
    end_date = fields.Datetime(default=datetime.today(), tracking=True, required=True)
    duration = fields.Char(string="Duration",
                           compute="_compute_leave_duration", tracking=True)
    approved_by_id = fields.Many2one("res.users", readonly=True, tracking=True)
    approve_date = fields.Date(string="Approve Date", tracking=True)
    student_id = fields.Many2one("op.student", string="Student", tracking=True)
    faculty_id = fields.Many2one("op.faculty", string="Faculty", required=True)
    attachment_ids = fields.One2many('ir.attachment', 'res_id',
                                     domain=[('res_model', '=',
                                              'student.leave.request')],
                                     string='Attachments',
                                     readonly=True)
    state = fields.Selection([
        ('draft', 'To Submit'),
        ('confirm', 'To Approve'),
        ('validate', 'Validated'),
        ('approve', 'Approved'),
        ('refuse', 'Refused'),
        ('cancel', 'Cancelled')], string="Status", default='draft', tracking=True)
    color = fields.Char('Color Index', compute="_compute_change_color_on_kanban")
    request_number = fields.Char(string="Request Number")

    @api.model
    def create(self, vals):
        if vals.get('request_number', 'New') == 'New':
            vals['request_number'] = self.env['ir.sequence'].next_by_code(
                'student.leave.request') or 'New'
        result = super(StudentLeaveRequest, self).create(vals)
        return result

    def _compute_change_color_on_kanban(self):
        for record in self:
            if record.state == "approve":
                record.color = 'background-color: #88d08b;'
            elif record.state == "cancel":
                record.color = 'background-color: #ff8178;'
            elif record.state == "refuse":
                record.color = 'background-color: #a4d4d4;'
            elif record.state == "validate":
                record.color = 'background-color: #ffce75;'
            else:
                record.color = 'white'

    @api.depends("start_date", "end_date")
    def _compute_leave_duration(self):
        for req in self:
            if req.end_date >= req.start_date:
                duration = req.end_date - req.start_date
                req.duration = str(int(duration.days) + 1) + ' Days'
            else:
                raise ValidationError(_(
                    'Start End Date should after Start Date.'
                ))

    def action_confirm(self):
        self.state = 'confirm'

    def action_validate(self):
        self.state = 'validate'

    def action_cancel(self):
        self.state = 'cancel'
        self.approved_by_id = self.env.uid
        self.approve_date = datetime.today().date()

    def action_approve(self):
        self.state = 'approve'
        self.approved_by_id = self.env.uid
        self.approve_date = datetime.today().date()

    def action_refuse(self):
        self.state = 'refuse'
        self.approved_by_id = self.env.uid
        self.approve_date = datetime.today().date()

    def action_draft(self):
        self.state = 'draft'

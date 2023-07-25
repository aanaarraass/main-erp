# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ExamTimeSlots(models.Model):
    _name = 'exam.timeslots'
    _rec_name = 'name'
    _description = 'exam.timeslots'

    name = fields.Char('Name')
    date_start = fields.Date('Start Date')
    date_stop = fields.Date('End Date')
    slot_1 = fields.Float('Time Slot 1')
    slot_2 = fields.Float('Time Slot 2')
    slot_3 = fields.Float('Time Slot 3')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('cancel', 'Cancelled'),
        ('done', 'Done'),
    ], string="status", default='draft')

    def action_confirm(self):
        self.state = 'confirm'

    def action_cancel(self):
        self.state = 'cancel'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'



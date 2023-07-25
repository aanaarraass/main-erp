# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ExamRoom(models.Model):
    _name = 'exam.room'
    _rec_name = 'name'
    _description = 'exam_management.exam_management'

    name = fields.Char('Name')
    capacity = fields.Integer('Capacity')
    # classroom_id = fields.Many2one('op.classroom', 'Class Room')
    company_id = fields.Many2one(comodel_name='res.company', string='Company', ondelet='cascade',
                                 default=lambda self: self.env.company)




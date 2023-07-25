# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ExamResult(models.Model):
    _name = 'exam.result'
    _rec_name = 'name'
    _description = 'Exam Result'

    name = fields.Char('Name')
    subjects = fields.Char('Subjects')
    grade = fields.Char('Grade')
    cgpa = fields.Char('CGPA')
    total_marks = fields.Integer('Total Marks')
    passing_marks = fields.Integer('Passing Marks')
    obtained_marks = fields.Integer('Marks')
    course_id = fields.Many2one(comodel_name='op.course', string='Course', ondelet='cascade')





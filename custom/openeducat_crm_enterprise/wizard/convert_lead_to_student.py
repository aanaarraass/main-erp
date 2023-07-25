
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields, api


class ConvertLeadToStudent(models.TransientModel):
    _name = "lead.to.student"
    _description = "Convert Lead To Student"

    lead_create_method = fields.Selection([
        ('create_admission', 'Create Admission and Convert To Student'),
        ('create_student_directly', 'Create Student Directly'),
        ('merge_in_student', 'Merge with existing student'),
    ], string='What do you want to create?', required=True)
    first_name = fields.Char('First Name', size=128)
    last_name = fields.Char('Last Name', size=128)
    gender = fields.Selection([
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other')
    ], 'Gender', default='m')
    birth_date = fields.Date(
        'Birth Date')
    register_id = fields.Many2one(
        'op.admission.register', 'Admission Register')
    student_id = fields.Many2one('op.student', 'Student')
    batch_id = fields.Many2one(
        'op.batch', 'Batch')
    course_id = fields.Many2one('op.course', 'Course')

    def convert_to_student(self):
        admission = self.env['op.admission']
        student = self.env['op.student']
        crm_lead = self.env['crm.lead'].browse(self.env.context['active_ids'])
        if self.lead_create_method == 'create_admission':
            admission.create({
                'name': self.first_name,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'register_id': self.register_id.id,
                'course_id': self.course_id.id,
                'batch_id': self.batch_id.id,
                'gender': self.gender,
                'birth_date': self.birth_date,
                'email': crm_lead.email_from
            })
        if self.lead_create_method == 'create_student_directly':
            student.create({
                'name': self.first_name,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'gender': self.gender,
                'mobile': crm_lead.phone,
                'email': crm_lead.email_from,
                'course_detail_ids': [(0, 0, {
                    'course_id': self.course_id.id,
                    'batch_id': self.batch_id.id
                })],
                'crm_lead_ids': [(0, 0, {
                    'name': crm_lead.name,
                    'expected_revenue': crm_lead.expected_revenue,
                    'user_id': crm_lead.user_id.id,
                    'probability': crm_lead.probability,
                })]
            })
        if self.lead_create_method == 'merge_in_student':
            current_student = self.env['op.student'].search(
                [('id', '=', self.student_id.id)])
            crm_lead.student_id = current_student.id

    @api.onchange('lead_create_method')
    def name_fetch(self):
        crm_lead = self.env['crm.lead'].browse(self.env.context['active_ids'])
        if crm_lead.partner_id:
            self.first_name = crm_lead.contact_name

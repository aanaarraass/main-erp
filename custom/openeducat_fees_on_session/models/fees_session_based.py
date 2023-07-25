
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields


class OpFeesTermsInherit(models.Model):
    _inherit = "op.fees.terms"

    fees_terms = fields.Selection(
        selection_add=[('session_based', 'Session Based Fees'),
                       ('faculty_based', 'Faculty Session Based Fees')],
        string='Term Type', default='fixed_days')


class OpSubjectCost(models.Model):
    _name = "op.subject.cost"
    _description = "Subject Cost"

    faculty_id = fields.Many2one('op.faculty', 'Faculty')
    subject_id = fields.Many2one('op.subject', 'Subject')
    product_id = fields.Many2one('product.product', 'product')
    cost = fields.Float('Cost', related="product_id.lst_price")


class OpFacultyInherit(models.Model):
    _inherit = "op.faculty"

    subject_cost_ids = fields.One2many('op.subject.cost', 'faculty_id', 'Subject Cost')


class OpAttendanceSheetInherit(models.Model):
    _inherit = "op.attendance.sheet"

    def attendance_done(self):

        stud_course_obj = self.env['op.student.course']
        attendance_obj = self.env['op.attendance.line'].search(
            [('attendance_id', '=', self.id), '|',
             ('present', '=', True), ('late', '=', True)])

        for rec in attendance_obj:
            amount = 0.0
            student_data = stud_course_obj.search(
                [('student_id', '=', rec.student_id.id),
                 ('course_id', '=', rec.session_id.course_id.id)])
            if student_data.fees_term_id.fees_terms in \
                    ['session_based', 'faculty_based']:
                for line in student_data.fees_term_id.line_ids:
                    product_id = line.fees_element_line.product_id.id
                    per_amount = line.value
                    if student_data.fees_term_id.fees_terms == 'session_based':
                        amount += line.fees_element_line.product_id.lst_price
                    elif student_data.fees_term_id.fees_terms == 'faculty_based':
                        for sub_cost in self.session_id.faculty_id.subject_cost_ids:
                            if sub_cost.subject_id == self.session_id.subject_id:
                                amount += sub_cost.product_id.lst_price
                    student_data.student_id.write({
                        'fees_detail_ids':
                            [(0, 0, {
                                'fees_line_id': line.id,
                                'amount': amount,
                                'fees_factor': per_amount,
                                'product_id': product_id,
                                'state': 'draft',
                                'date': self.attendance_date,
                            })]
                    })

        self.state = 'done'

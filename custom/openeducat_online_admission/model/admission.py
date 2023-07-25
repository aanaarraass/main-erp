
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#


from odoo import models, fields


class OpAdmission(models.Model):
    _inherit = "op.admission"

    state = fields.Selection(selection_add=[
        ('draft', 'Admission Detail'), ('online', 'Online Admission'),
        ('submit', 'Submitted'), ('confirm', 'Confirmed'),
        ('admission', 'Admission Confirm'), ('reject', 'Rejected'),
        ('pending', 'Pending'), ('cancel', 'Cancelled'), ('done', 'Done')], tracking=True)
    order_id = fields.Many2one('sale.order', 'Registration Fees Ref')
    merit_list_id = fields.Many2one('op.admission.merit.list', 'Merit List')
    application = fields.Char()
    ag_score = fields.Float(string="Aggregate")
    interview_score = fields.Integer(string="Interview Score")

class OpAdmissionEducationDetail(models.Model):
    _inherit = "op.admission.education.detail"

    previous_degrees = fields.Selection(
        [('1', 'Secondary School/Equivalence Certification'), ('2', 'Intermediate/Equivalence Certification'),('6', 'BSc (14 Years)'),
         ('3', 'BS (16 Years)'), ('4', 'Master (16 Years)'),
         ('5', 'MS/MPhil (18 Years)')],
        'Previous Degrees', tracking=True)
class OpAdmissionMeritList(models.Model):
    _name = "op.admission.merit.list"

    name = fields.Char(string='Name')
    seats = fields.Integer(string='No. of Seats')
    program_id = fields.Many2one('op.program',string='Program')
    applicant_ids = fields.One2many('op.admission', 'merit_list_id', 'Applicants')

class OpBatch(models.Model):
    _inherit = "op.batch"


class OpStudentCourse(models.Model):
    _inherit = "op.student.course"


class OpSubject(models.Model):
    _inherit = "op.subject"

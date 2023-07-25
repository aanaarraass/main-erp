# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from datetime import datetime, date

from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import random


class OpAdmission(models.Model):
    _name = "op.admission"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "application_number"
    _description = "Admission"
    _order = 'id DESC'

    name = fields.Char('Name',translate=True)
    roll_number = fields.Char(string='Roll Number', default=lambda self:  _('new'))

    # first_name = fields.Char(
    #     'First Name', size=128, required=True, translate=True)
    # middle_name = fields.Char(
    #     'Middle Name', size=128, translate=True,
    #     states={'done': [('readonly', True)]})
    # last_name = fields.Char(
    #     'Last Name', size=128, required=True, translate=True,
    #     states={'done': [('readonly', True)]})
    # title = fields.Many2one(
    #     'res.partner.title', 'Title', states={'done': [('readonly', True)]})
    application_number = fields.Char(
        'Application Number', size=16, copy=False,
        required=True, readonly=True, store=True,
        default=lambda self:
        self.env['ir.sequence'].next_by_code('op.admission'))

    education_detail_ids = fields.One2many('op.admission.education.detail', 'op_admission_id', string='Education Detail')

    admission_date = fields.Date('Admission Date', copy=False, states={'done': [('readonly', True)]}, default= lambda self: fields.Date.today())
    application_date = fields.Datetime('Application Date',copy=False, states={'done': [('readonly', True)]},
        default=lambda self: fields.Datetime.now())
    birth_date = fields.Date(
        'Birth Date', states={'done': [('readonly', True), ]}, default=date.today())
    course_id = fields.Many2one('op.course', 'Course', states={'done': [('readonly', True)]})
    batch_id = fields.Many2one(
        'op.batch', 'Batch', required=False,
        states={'done': [('readonly', True)],
                'submit': [('required', True)],
                'fees_paid': [('required', True)]})
    street = fields.Char(
        'Street', size=256, states={'done': [('readonly', True)]})
    street2 = fields.Char(
        'Street2', size=256, states={'done': [('readonly', True)]})
    phone = fields.Char(
        'Phone', size=16, states={'done': [('readonly', True)]})
    mobile = fields.Char(
        'Mobile', size=16,
        states={'done': [('readonly', True)]})
    whatsapp = fields.Char(
        'Whatsapp', size=16,
        states={'done': [('readonly', True)]})
    email = fields.Char(
        'Email', size=256,
        states={'done': [('readonly', True)]})
    city = fields.Char('City', size=64, states={'done': [('readonly', True)]})
    zip = fields.Char('Zip', size=8, states={'done': [('readonly', True)]})
    state_id = fields.Many2one(
        'res.country.state', 'States', states={'done': [('readonly', True)]})
    country_id = fields.Many2one(
        'res.country', 'Country', states={'done': [('readonly', True)]})
    fees = fields.Float('Fees', states={'done': [('readonly', True)]})
    image = fields.Image('image', states={'done': [('readonly', True)]})
    # ('edu', 'Pre. Edu. Detail'),
    state = fields.Selection(
        [('pd', 'Personal Details'),('gd', 'Guardian Details'), ('ad', 'Academic details'), ('draft', 'Admission Detail'),
         ('submit', 'Submitted'),
         ('confirm', 'Confirmed'), ('admission', 'Admission Confirm'),
         ('reject', 'Rejected'), ('pending', 'Pending'),
         ],default='pd', string='State', tracking=True)
    due_date = fields.Date('Due Date', states={'done': [('readonly', True)]})
    prev_institute_id = fields.Char('Previous Institute',
                                    states={'done': [('readonly', True)]})
    prev_course_id = fields.Char('Previous Course',
                                 states={'done': [('readonly', True)]})
    prev_result = fields.Char(
        'Previous Result', size=256, states={'done': [('readonly', True)]})
    family_business = fields.Char(
        'Family Business', size=256, states={'done': [('readonly', True)]})
    family_income = fields.Float(
        'Family Income', states={'done': [('readonly', True)]})
    gender = fields.Selection(
        [('m', 'Male'), ('f', 'Female'), ('o', 'Other')],
        string='Gender',
        states={'done': [('readonly', True)]})
    student_id = fields.Many2one(
        'op.student', 'Student', states={'done': [('readonly', True)]})
    nbr = fields.Integer('No of Admission', readonly=True)
    register_id = fields.Many2one(
        'op.admission.register', 'Admission Register', states={'done': [('readonly', True)]})
    partner_id = fields.Many2one('res.partner', 'Partner')
    is_student = fields.Boolean('Is Already Student')
    fees_term_id = fields.Many2one('op.fees.terms', 'Fees Term')
    active = fields.Boolean(default=True)
    discount = fields.Float(string='Discount (%)',
                            digits='Discount', default=0.0)

    fees_start_date = fields.Date('Fees Start Date')
    company_id = fields.Many2one(
        'res.company', string='Campus',
        default=lambda self: self.env.user.company_id)

    studetn_cnic_number = fields.Char('Student CNIC', required = True,)
    cnic_image = fields.Binary('CNIC Image', required = True,)
    bank_name = fields.Char('Bank Name')
    bank_branch_code = fields.Char('Branch Code')
    bank_deposit_amount = fields.Char('deposit Amount')
    bank_vouher_image = fields.Binary('Bank Voucher')

    quota_id = fields.Many2one(
        'op.admission.quota', 'Quota',
        states={'draft': [('readonly', False)]}, tracking=True)

    department_id = fields.Many2one(
        'op.department', 'Department',
        states={'draft': [('readonly', False)]}, tracking=True)

    program_id = fields.Many2one(
        'op.program', 'Program',
        states={'draft': [('readonly', False)]}, tracking=True)

    _sql_constraints = [
        ('unique_application_number',
         'unique(application_number)',
         'Application Number must be unique per Application!'),
    ]
    #fields for guardian detail page
    father_name = fields.Char('Father Full Name', states={'gd': [('required', True)]})
    father_cnic = fields.Char('Father CNIC', states={'gd': [('required', True)]})
    guardian_mobile = fields.Char('Father/Guardian Mobile')
    guardian_name = fields.Char('Guardian Name(if any)')
    relation_guardian = fields.Char('Relation with Guardian(if any)')
    father_occupation = fields.Char('Father Occupation')
    father_income = fields.Float('Father/Mother/Guardian Income')
    guardian_income = fields.Float('Guardian Income')
    mother_income = fields.Float('Mother(if any)')

    is_father_alive = fields.Selection([
        ('alive', 'Alive'),
        ('late', 'Late'),
    ], string='Is Father Alive', default='alive')

    @api.onchange('student_id', 'is_student')
    def onchange_student(self):
        if self.is_student and self.student_id:
            sd = self.student_id
            # self.title = sd.title and sd.title.id or False
            # self.first_name = sd.first_name
            # self.middle_name = sd.middle_name
            # self.last_name = sd.last_name
            self.name = str(sd.first_name)+' ' + str(sd.middle_name)+' ' + str(sd.last_name)
            self.birth_date = sd.birth_date
            self.gender = sd.gender
            self.image = sd.image_1920 or False
            self.street = sd.street or False
            self.street2 = sd.street2 or False
            self.phone = sd.phone or False
            self.mobile = sd.mobile if sd.mobile else False
            self.email = sd.email or False
            self.zip = sd.zip or False
            self.city = sd.city or False
            self.country_id = sd.country_id and sd.country_id.id or False
            self.state_id = sd.state_id and sd.state_id.id or False
            self.partner_id = sd.partner_id and sd.partner_id.id or False
        else:
            self.birth_date = ''
            self.gender = ''
            self.image = False
            self.street = ''
            self.street2 = ''
            self.phone = ''
            self.mobile = '' if self.mobile else +92
            self.zip = ''
            self.city = ''
            self.country_id = False
            self.state_id = False
            self.partner_id = False

    @api.constrains('phone', 'mobile','whatsapp','studetn_cnic_number','father_cnic','guardian_mobile')
    def _check_phone_number(self):
        for rec in self:
            if rec.phone:
                if not rec.phone.isdigit():
                    raise ValidationError(_("You can only put Integers as Phone Number"))
            if rec.mobile:
                if not rec.mobile.isdigit():
                    raise ValidationError(_("You can only put Integers as Mobile Number"))
            if rec.whatsapp:
                if not rec.whatsapp.isdigit():
                    raise ValidationError(_("You can only put Integers as Whatsapp Number"))
            if rec.studetn_cnic_number:
                if not rec.studetn_cnic_number.isdigit():
                    raise ValidationError(_("You can only put Integers as CNIC Number"))
            if rec.father_cnic:
                if not rec.father_cnic.isdigit():
                    raise ValidationError(_("You can only put Integers as CNIC Number"))
            if rec.guardian_mobile:
                if not rec.guardian_mobile.isdigit():
                    raise ValidationError(_("You can only put Integers as Contact Number"))


    @api.onchange('register_id')
    def onchange_register(self):
        self.course_id = self.register_id.course_id
        self.fees = self.register_id.product_id.lst_price
        self.company_id = self.register_id.company_id

    @api.onchange('course_id')
    def onchange_course(self):
        self.batch_id = False
        term_id = False
        if self.course_id and self.course_id.fees_term_id:
            term_id = self.course_id.fees_term_id.id
        self.fees_term_id = term_id


    @api.constrains('register_id', 'application_date')
    def _check_admission_register(self):
        print("_check_admission_register")
        for rec in self:
            start_date = fields.Date.from_string(rec.register_id.start_date)
            end_date = fields.Date.from_string(rec.register_id.end_date)
            application_date = fields.Date.from_string(rec.application_date)
            if application_date:
                if any([start_date,end_date]):
                    if application_date < start_date or application_date > end_date:
                        raise ValidationError(_(
                            "Application Date should be between Start Date & \
                            End Date of Admission Register."))


    @api.constrains('birth_date')
    def _check_birthdate(self):
        today_date = fields.Date.today()
        for record in self:
           if record.birth_date:
               if record.birth_date >= today_date:
                   raise ValidationError(_(
                       "Birth Date can't be greater than current date!"))
               elif record:
                   day = (today_date - record.birth_date).days
                   years = day // 365
                   if years < self.register_id.minimum_age_criteria:
                       raise ValidationError(_(
                           "Not Eligible for Admission minimum required age is : %s " % self.register_id.minimum_age_criteria))

    def submit_form(self):
        self.state = 'submit'

    def admission_confirm(self):
        self.state = 'admission'
        if self.roll_number == _('new') or self.roll_number == '':
            self.roll_number = self.env['ir.sequence'].next_by_code('op.admission.roll') or _('new')

    def confirm_in_progress(self):
        for record in self:
            record.state = 'confirm'

    def get_student_vals(self):
        for student in self:
            student_user = self.env['res.users'].create({
                'name': student.name,
                'login': student.email,
                'image_1920': self.image or False,
                'is_student': True,
                'company_id': self.company_id.id,
                'groups_id': [
                    (6, 0,
                     [self.env.ref('base.group_portal').id])]
            })
            details = {
                'phone': student.phone,
                'mobile': student.mobile,
                'roll_number': student.roll_number,
                'father_name': student.father_name,
                'studetn_cnic_number': student.studetn_cnic_number ,
                'email': student.email,
                'street': student.street,
                'street2': student.street2,
                'city': student.city,
                'country_id':
                    student.country_id and student.country_id.id or False,
                'state_id': student.state_id and student.state_id.id or False,
                'image_1920': student.image,
                'zip': student.zip,
            }
            student_user.partner_id.write(details)
            details.update({
                # 'title': student.title and student.title.id or False,
                'name': student.name,
                'first_name': student.name,
                # 'middle_name': student.middle_name,
                # 'last_name': student.last_name,
                'birth_date': student.birth_date,
                'gender': student.gender,
                'image_1920': student.image or False,
                'course_detail_ids': [[0, False, {
                    'course_id':
                        student.course_id and student.course_id.id or False,
                    'batch_id':
                        student.batch_id and student.batch_id.id or False,
                    'academic_years_id': student.register_id.academic_years_id.id or False,
                    'academic_term_id': student.register_id.academic_term_id.id or False,
                    'fees_term_id': student.fees_term_id.id,
                    'fees_start_date': student.fees_start_date,
                }]],
                'user_id': student_user.id,
                'company_id': self.company_id.id,
                'partner_id': student_user.partner_id.id,
            })
            return details

    def enroll_student(self):
        for record in self:
            if record.register_id.max_count:
                total_admission = self.env['op.admission'].search_count(
                    [('register_id', '=', record.register_id.id),
                     ('state', '=', 'done')])
                if not total_admission < record.register_id.max_count:
                    msg = 'Max Admission In Admission Register :- (%s)' % (
                        record.register_id.max_count)
                    raise ValidationError(_(msg))
            if not record.student_id:
                vals = record.get_student_vals()
                record.partner_id = vals.get('partner_id')
                record.student_id = student_id = self.env[
                    'op.student'].create(vals).id

            else:
                student_id = record.student_id.id
                record.student_id.write({
                    'course_detail_ids': [[0, False, {
                        'course_id':
                            record.course_id and record.course_id.id or False,
                        'batch_id':
                            record.batch_id and record.batch_id.id or False,
                        'fees_term_id': record.fees_term_id.id,
                        'fees_start_date': record.fees_start_date,
                    }]],
                })
            if record.fees_term_id.fees_terms in ['fixed_days', 'fixed_date']:
                val = []
                product_id = record.register_id.product_id.id
                for line in record.fees_term_id.line_ids:
                    no_days = line.due_days
                    per_amount = line.value
                    amount = (per_amount * record.fees) / 100
                    dict_val = {
                        'fees_line_id': line.id,
                        'amount': amount,
                        'fees_factor': per_amount,
                        'product_id': product_id,
                        'discount': record.discount or record.fees_term_id.discount,
                        'state': 'draft',
                        'course_id': record.course_id and record.course_id.id or False,
                        'batch_id': record.batch_id and record.batch_id.id or False,
                    }
                    if line.due_date:
                        date = line.due_date
                        dict_val.update({
                            'date': date
                        })
                    elif self.fees_start_date:
                        date = self.fees_start_date + relativedelta(
                            days=no_days)
                        dict_val.update({
                            'date': date,
                        })
                    else:
                        date_now = (datetime.today() + relativedelta(
                            days=no_days)).date()
                        dict_val.update({
                            'date': date_now,
                        })
                    val.append([0, False, dict_val])
                record.student_id.write({
                    'fees_detail_ids': val
                })
            record.write({
                'nbr': 1,
                'state': 'done',
                'admission_date': fields.Date.today(),
                'student_id': student_id,
                'is_student': True,
            })
            reg_id = self.env['op.subject.registration'].create({
                'student_id': student_id,
                'batch_id': record.batch_id.id,
                'course_id': record.course_id.id,
                'min_unit_load': record.course_id.min_unit_load or 0.0,
                'max_unit_load': record.course_id.max_unit_load or 0.0,
                'state': 'draft',
            })
            if not record.phone or not record.mobile:
                raise UserError(
                    _('Please fill in the mobile number'))
            reg_id.get_subjects()

    def confirm_rejected(self):
        self.state = 'reject'

    def confirm_pending(self):
        self.state = 'pending'

    def confirm_to_draft(self):
        self.state = 'draft'
    def open_next_page(self):
        if self.state == 'pd':
            self.state = 'gd'
        elif self.state == 'gd':
            self.state = 'ad'
        elif self.state == 'ad':
            self.state = 'draft'

        return {
            'type': 'ir.actions.act_window',
            'name': 'Application Form',
            'view_mode': 'form',
            'res_model': 'op.admission',
            'res_id': self.id,
            'target': 'inline' if self.state in ['ad','pd','gd','draft'] else 'current',
        }

    def open_pre_page(self):
        if self.state == 'draft':
            self.state = 'ad'
        elif self.state == 'ad':
            self.state = 'gd'
        elif self.state == 'gd':
            self.state = 'pd'
        return {
            'type': 'ir.actions.act_window',
            'name': 'Application Form',
            'view_mode': 'form',
            'res_model': 'op.admission',
            'res_id': self.id,
            'target': 'inline' if self.state in ['ad', 'pd', 'gd'] else 'current',
        }


    def confirm_cancel(self):
        self.state = 'cancel'
        if self.is_student and self.student_id.fees_detail_ids:
            self.student_id.fees_detail_ids.state = 'cancel'

    def payment_process(self):
        self.state = 'fees_paid'

    def open_student(self):
        form_view = self.env.ref('openeducat_core.view_op_student_form')
        tree_view = self.env.ref('openeducat_core.view_op_student_tree')
        value = {
            'domain': str([('id', '=', self.student_id.id)]),
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'op.student',
            'view_id': False,
            'views': [(form_view and form_view.id or False, 'form'),
                      (tree_view and tree_view.id or False, 'tree')],
            'type': 'ir.actions.act_window',
            'res_id': self.student_id.id,
            'target': 'current',
            'nodestroy': True
        }
        self.state = 'done'
        return value

    def create_invoice(self):
        """ Create invoice for fee payment process of student """

        partner_id = self.env['res.partner'].create({'name': self.name})
        account_id = False
        product = self.register_id.product_id
        if product.id:
            account_id = product.property_account_income_id.id
        if not account_id:
            account_id = product.categ_id.property_account_income_categ_id.id
        if not account_id:
            raise UserError(
                _('There is no income account defined for this product: "%s". \
                   You may have to install a chart of account from Accounting \
                   app, settings menu.') % (product.name,))
        if self.fees <= 0.00:
            raise UserError(
                _('The value of the deposit amount must be positive.'))
        amount = self.fees
        name = product.name
        invoice = self.env['account.invoice'].create({
            'name': self.name,
            'origin': self.application_number,
            'move_type': 'out_invoice',
            'reference': False,
            'account_id': partner_id.property_account_receivable_id.id,
            'partner_id': partner_id.id,
            'invoice_line_ids': [(0, 0, {
                'name': name,
                'origin': self.application_number,
                'account_id': account_id,
                'price_unit': amount,
                'quantity': 1.0,
                'discount': 0.0,
                'uom_id': self.register_id.product_id.uom_id.id,
                'product_id': product.id,
            })],
        })
        invoice.compute_taxes()
        form_view = self.env.ref('account.invoice_form')
        tree_view = self.env.ref('account.invoice_tree')
        value = {
            'domain': str([('id', '=', invoice.id)]),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.invoice',
            'view_id': False,
            'views': [(form_view and form_view.id or False, 'form'),
                      (tree_view and tree_view.id or False, 'tree')],
            'type': 'ir.actions.act_window',
            'res_id': invoice.id,
            'target': 'current',
            'nodestroy': True
        }
        self.partner_id = partner_id
        self.state = 'payment_process'
        return value

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Admission'),
            'template': '/openeducat_admission/static/xls/op_admission.xls'
        }]


    def _calc_point(self):
        if self:
            m_val = 0
            i_val = 0
            b_val = 0
            mf_val = 0
            p_f_val = 0
            p_mf_val = 0
            b_i_val = 0
            p_i_val = 0
            p_m_val = 0
            try:
                # for rec in self.education_detail_ids:
                for rec in self.education_detail_ids.filtered(lambda w: w.previous_degrees in ('1', '2')):
                    # if rec.previous_degrees not in ('3', '4', '5') and rec.previous_degrees in ('1', '2'):
                    #     if rec.previous_degrees == '1':
                    #         m_val = ((rec.marks_obtained / rec.total_marks ) * 30) or 0
                    #     if rec.previous_degrees == '2':
                    #         i_val = ((rec.marks_obtained / rec.total_marks) * 70) or 0
                    #
                    # if rec.previous_degrees in ('1', '2', '3', '4') and rec.previous_degrees not in ('5',):
                    #     if rec.previous_degrees == '1':
                    #         m_val = ((rec.marks_obtained / rec.total_marks) * 10) or 0
                    #     if rec.previous_degrees == '2':
                    #         i_val = ((rec.marks_obtained / rec.total_marks) * 15) or 0
                    #     if rec.previous_degrees == '3':
                    #         b_val = ((rec.marks_obtained / rec.total_marks) * 25) or 0
                    #     if rec.previous_degrees == '4':
                    #         mf_val = ((rec.marks_obtained / rec.total_marks) * 50) or 0

                    if rec.previous_degrees in ('1', '2', '3', '4', '5'):
                        if rec.previous_degrees == '1':
                            m_val = ((rec.marks_obtained / rec.total_marks) * 10) or 0
                            p_m_val = self._get_score(rec.marks_obtained,rec.total_marks,rec.marks_type, rec.previous_degrees,rec.cgpa_or_marks)
                        if rec.previous_degrees == '2':
                            i_val = ((rec.marks_obtained / rec.total_marks) * 15) or 0
                            p_i_val = self._get_score(rec.marks_obtained, rec.total_marks, rec.marks_type,
                                                      rec.previous_degrees, rec.cgpa_or_marks)
                        if rec.previous_degrees == '3':
                            b_val = ((rec.marks_obtained / rec.total_marks) * 25) or 0
                            b_i_val = self._get_score(rec.marks_obtained, rec.total_marks, rec.marks_type,
                                                      rec.previous_degrees, rec.cgpa_or_marks)
                        if rec.previous_degrees == '4':
                            mf_val = ((rec.marks_obtained / rec.total_marks) * 50) or 0
                            p_mf_val = self._get_score(rec.marks_obtained, rec.total_marks, rec.marks_type,
                                                      rec.previous_degrees, rec.cgpa_or_marks)

                        if rec.previous_degrees == '5':
                            p_f_val = self._get_score(rec.marks_obtained, rec.total_marks, rec.marks_type,
                                                      rec.previous_degrees, rec.cgpa_or_marks)


                self.point_score = m_val + i_val + b_val + mf_val
                self.point_score_second = p_f_val + p_mf_val + b_i_val + p_i_val + p_m_val
            except:
                self.point_score = 0
                self.point_score_second = 0
                pass


    def _get_score(self, ob_marks, total_marks, marks_type, edu_level, cgpa_or_marks):
        try:
            # 1 = Matric (10 year) 2 = Inter (12 year) 3 = Bachelor (16 year) 4 = MS 18 year
            score = 0
            if marks_type == 'marks':
                marks = (ob_marks / total_marks) * 100
                if marks >= 45 and marks <= 49:
                    if edu_level == '1':
                        score = 5
                    elif edu_level == '2':
                        score = 5
                    elif edu_level == '3':
                        score = 10
                    elif edu_level == '4':
                        score = 20

                elif marks >= 50 and marks <= 54:
                    if edu_level == '1':
                        score = 6
                    elif edu_level == '2':
                        score = 6
                    elif edu_level == '3':
                        score = 12
                    elif edu_level == '4':
                        score = 24

                elif marks >= 55 and marks <= 59:
                    if edu_level == '1':
                        score = 7
                    elif edu_level == '2':
                        score = 7
                    elif edu_level == '3':
                        score = 14
                    elif edu_level == '4':
                        score = 28
                elif marks >= 60 and marks <= 69:
                    if edu_level == '1':
                        score = 8
                    elif edu_level == '2':
                        score = 8
                    elif edu_level == '3':
                        score = 16
                    elif edu_level == '4':
                        score = 32

                elif marks >= 70 and marks <= 79:
                    if edu_level == '1':
                        score = 9
                    elif edu_level == '2':
                        score = 9
                    elif edu_level == '3':
                        score = 18
                    elif edu_level == '4':
                        score = 36
                elif marks >= 80:
                    if edu_level == '1':
                        score = 9
                    elif edu_level == '2':
                        score = 9
                    elif edu_level == '3':
                        score = 18
                    elif edu_level == '4':
                        score = 36

            elif marks_type == 'cgpa':
                if cgpa_or_marks >= 2.5 and cgpa_or_marks <= 2.9:
                    if edu_level == '3':
                        score = 20
                    elif edu_level == '4':
                        score = 30
                if cgpa_or_marks >= 3.0 and cgpa_or_marks <= 3.3:
                    if edu_level == '3':
                        score = 28
                    elif edu_level == '4':
                        score = 42

                if cgpa_or_marks >= 3.4 and cgpa_or_marks <= 3.7:
                    if edu_level == '3':
                        score = 36
                    elif edu_level == '4':
                        score = 54

                if cgpa_or_marks >= 3.8:
                    if edu_level == '3':
                        score = 40
                    elif edu_level == '4':
                        score = 60


            return score


        except:
            return 0



    point_score = fields.Float(string='Point Score', compute='_calc_point')

    point_score_second = fields.Float(string='Point Score Second')

    @api.onchange('is_student', 'student_id')
    def _roll_number(self):
        for rec in self:
            if rec.is_student:
                rec.roll_number = rec.student_id.roll_number


class OpAdmissionEduDetails(models.Model):
    _name = "op.admission.education.detail"
    # _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Admission Education Detail"
    _order = 'id'

    op_admission_id = fields.Many2one(
        'op.admission', 'Admission')

    previous_degrees = fields.Selection(
        [('1', 'Secondary School/Equivalence Certification'), ('2', 'Intermediate/Equivalence Certification'),
         ('3', 'Bachelor'), ('4', 'Master'),
         ('5', 'MS/MPhil')],
        'Previous Degrees', tracking=True)

    degree_name = fields.Char('Degree Name')

    total_marks = fields.Integer('Total Marks')
    marks_obtained = fields.Integer('Marks Obtained')


    marks_type = fields.Selection(
        [('cgpa', 'CGPA'), ('marks', 'Marks %')],
        'Type', tracking=True)
    cgpa_or_marks = fields.Float('CGPA/Marks %', digits=(16, 2))
    passing_year = fields.Char('Passing Year')
    name_of_institution = fields.Char('Board/University')

    @api.onchange('total_marks', 'marks_obtained', 'marks_type')
    def _calc_percentage(self):
        if self:
            for rec in self:
                if rec.marks_type == 'marks' and rec.total_marks > 0 and rec.marks_obtained > 0:
                    rec.cgpa_or_marks = (rec.marks_obtained / rec.total_marks) * 100






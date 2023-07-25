
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import timedelta


class OpFeesTermsInherit(models.Model):
    _inherit = "op.fees.terms"

    fees_terms = fields.Selection(
        selection_add=[('duration_based', 'Duration Based Fees')],
        string='Term Type', default='fixed_days')
    expires_after = fields.Integer(string='Invoice Cycles',
                                   help="Expires after number of Invoices")
    term_duration = fields.Integer(default=1)
    bill_selection = fields.Selection([('days', 'Day'),
                                       ('weeks', 'Week'),
                                       ('months', 'Month'), ('years', 'Year')],
                                      string="Bill Every",
                                      help='Generate Invoice Every ('
                                           'Day/Week/Month/Year)')


class OpStudentCourseInherit(models.Model):
    _inherit = "op.student.course"

    expires_after = fields.Integer(string='Invoice Cycles',
                                   help="Expires after number of Invoices")
    generated_invoices = fields.Integer(string='Generated Invoices',
                                        help="Number of Invoices Generated")
    next_invoice_date = fields.Date(string="Next Invoice Date", readonly=True)
    prev_invoice_date = fields.Date(string="Previous Invoice Date", readonly=True)

    @api.model
    def create(self, values):
        res = super(OpStudentCourseInherit, self).create(values)
        if res.fees_term_id.fees_terms == 'duration_based':
            if not res.fees_start_date:
                res.fees_start_date = fields.Date.today()
            if res.fees_start_date != fields.Date.today():
                res.next_invoice_date = res.fees_start_date
            else:
                res.next_invoice_date = res.fees_start_date
            res.expires_after = res.fees_term_id.expires_after
            res.cron_create_invoice()
        return res

    def cron_create_invoice(self):
        current_date = fields.Date.today()
        stud_course_obj = self.env['op.student.course'].search(
            [('fees_term_id.fees_terms', '=', 'duration_based')])

        for stud in stud_course_obj:
            if stud.generated_invoices == stud.expires_after:
                stud.next_invoice_date = False
            if stud.course_id.id == stud.course_id.id and \
                    stud.generated_invoices < stud.expires_after and \
                    stud.next_invoice_date == current_date:
                stud.generated_invoices += 1
                if stud.next_invoice_date == current_date:
                    if stud.fees_term_id.bill_selection == 'days':
                        term_duration = stud.fees_term_id.term_duration
                        stud.prev_invoice_date = stud.next_invoice_date
                        stud.next_invoice_date = \
                            (stud.next_invoice_date + timedelta(days=term_duration))
                    elif stud.fees_term_id.bill_selection == 'weeks':
                        term_duration = stud.fees_term_id.term_duration
                        stud.prev_invoice_date = stud.next_invoice_date
                        stud.next_invoice_date = \
                            (stud.next_invoice_date + relativedelta(
                                weeks=term_duration))
                    elif stud.fees_term_id.bill_selection == 'months':
                        term_duration = stud.fees_term_id.term_duration
                        stud.prev_invoice_date = stud.next_invoice_date
                        stud.next_invoice_date = \
                            (stud.next_invoice_date + relativedelta(
                                months=term_duration))
                    elif stud.fees_term_id.bill_selection == 'years':
                        term_duration = stud.fees_term_id.term_duration
                        stud.prev_invoice_date = stud.next_invoice_date
                        stud.next_invoice_date = \
                            (stud.next_invoice_date + relativedelta(
                                years=term_duration))
                else:
                    stud.next_invoice_date = stud.fees_start_date
                amount = stud.fees_term_id. \
                    line_ids.fees_element_line.product_id.lst_price
                per_amount = stud.fees_term_id.line_ids.value
                product_id = stud.fees_term_id. \
                    line_ids.fees_element_line.product_id.id
                line = stud.fees_term_id.line_ids.id
                stud.student_id.write({
                    'fees_detail_ids':
                        [(0, 0, {
                            'fees_line_id': line,
                            'amount': amount,
                            'fees_factor': per_amount,
                            'product_id': product_id,
                            'state': 'draft',
                            'date': current_date,
                        })]
                })

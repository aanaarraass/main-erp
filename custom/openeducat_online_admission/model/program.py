# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
import pdb

from odoo import models, api, fields, _
from odoo.exceptions import ValidationError


class OpProgram(models.Model):
    _inherit = "op.program"

    level = fields.Selection([('matric', 'Matric'), ('fsc', 'F.Sc.'), ('bs', 'Graduation'), ('ms', 'Post Graduation')],
                             string="Degree Level")


class OpAdmissionRegister(models.Model):
    _inherit = "op.admission.register"

    level = fields.Selection(related="program_id.level", string="Degree Level")
    matric = fields.Integer('Matric %')
    fsc = fields.Integer('F.Sc. %')
    bs = fields.Integer('BS %')
    merit_list_for = fields.Selection([('bs', 'BS'), ('ms', 'MS'), ('ms', 'MS')], string="Merit List For")
    merit_list = fields.Many2one('op.admission.merit.list', string="Merit List")
    seats = fields.Integer('Total Seats')
    ag_done = fields.Boolean('Aggregate Done', default=False)

    def calculate_aggregate(self):
        if not self.merit_list_for:
            raise ValidationError(_('Please set Merit List for value'))
        elif self.merit_list_for == 'bs':
            self.calculate_bs_aggregate()
        elif self.merit_list_for == 'ms':
            self.calculate_ms_aggregate()

    def calculate_bs_aggregate(self):
        for rec in self.admission_ids:
            metric = rec.education_detail_ids.filtered(
                lambda x: x.previous_degrees == '1')
            fsc = rec.education_detail_ids.filtered(
                lambda x: x.previous_degrees == '2')
            if metric and fsc and metric.total_marks and fsc.total_marks:
                rec.ag_score = ((metric.marks_obtained / metric.total_marks) * 30) + (
                            (fsc.marks_obtained / fsc.total_marks) * 70)
            else:
                rec.ag_score = 0
        if self.admission_ids:
            self.ag_done = True

    def create_merit_list(self):
        count = 1
        merit_list = False
        data = []
        if self.admission_ids:
            values = {
                'name': self.program_id.name + " Merit List",
                'seats': self.seats,
                'program_id': self.program_id.id
            }
            merit_list = self.env['op.admission.merit.list'].create(values)
        for rec in self.admission_ids.sorted(
                key=lambda l: l.ag_score, reverse=True):
            if count > self.seats:
                continue
            else:
                data.append(rec.id)
            count += 1

        merit_list.applicant_ids = data
        self.merit_list = merit_list

    def matric_marks(self, metric_marks):

        if metric_marks:
            if metric_marks.cgpa_or_marks > 0 and metric_marks.cgpa_or_marks >= 45 and metric_marks.cgpa_or_marks < 50:
                return (5)
            elif metric_marks.cgpa_or_marks >= 50 and metric_marks.cgpa_or_marks < 55:
                return (6)
            elif metric_marks.cgpa_or_marks >= 55 and metric_marks.cgpa_or_marks < 60:
                return (7)
            elif metric_marks.cgpa_or_marks >= 60 and metric_marks.cgpa_or_marks < 70:
                return (8)
            elif metric_marks.cgpa_or_marks >= 70 and metric_marks.cgpa_or_marks < 80:
                return (9)
            else:
                return (10)
        else:
            return 0

    def fsc_marks(self, fsc_marks):
        if fsc_marks:
            if fsc_marks.cgpa_or_marks > 0 and fsc_marks.cgpa_or_marks >= 45 and fsc_marks.cgpa_or_marks < 50:
                return (5)
            elif fsc_marks.cgpa_or_marks >= 50 and fsc_marks.cgpa_or_marks < 55:
                return (6)
            elif fsc_marks.cgpa_or_marks >= 55 and fsc_marks.cgpa_or_marks < 60:
                return (7)
            elif fsc_marks.cgpa_or_marks >= 60 and fsc_marks.cgpa_or_marks < 70:
                return (8)
            elif fsc_marks.cgpa_or_marks >= 70 and fsc_marks.cgpa_or_marks < 80:
                return (9)
            else:
                return (10)
        else:
            return 0

    def bsc_marks(self, bsc_marks):
        if bsc_marks:
            if bsc_marks.cgpa_or_marks > 0 and bsc_marks.cgpa_or_marks >= 45 and bsc_marks.cgpa_or_marks < 50:
                return (10)
            elif bsc_marks.cgpa_or_marks >= 50 and bsc_marks.cgpa_or_marks < 55:
                return (12)
            elif bsc_marks.cgpa_or_marks >= 55 and bsc_marks.cgpa_or_marks < 60:
                return (14)
            elif bsc_marks.cgpa_or_marks >= 60 and bsc_marks.cgpa_or_marks < 70:
                return (16)
            elif bsc_marks.cgpa_or_marks >= 70 and bsc_marks.cgpa_or_marks < 80:
                return (18)
            else:
                return (20)
        else:
            return 0

    def msc_marks(self, msc_marks):
        if msc_marks:
            if msc_marks.marks_type == 'marks':
                if msc_marks.cgpa_or_marks > 0 and msc_marks.cgpa_or_marks >= 45 and msc_marks.cgpa_or_marks < 50:
                    return (20)
                elif msc_marks.cgpa_or_marks >= 50 and msc_marks.cgpa_or_marks < 55:
                    return (24)
                elif msc_marks.cgpa_or_marks >= 55 and msc_marks.cgpa_or_marks < 60:
                    return (28)
                elif msc_marks.cgpa_or_marks >= 60 and msc_marks.cgpa_or_marks < 70:
                    return (32)
                elif msc_marks.cgpa_or_marks >= 70 and msc_marks.cgpa_or_marks < 80:
                    return (36)
                else:
                    return (40)
            elif msc_marks.marks_type == 'cgpa':
                if msc_marks.cgpa_or_marks > 0 and msc_marks.cgpa_or_marks >= 2.5 and msc_marks.cgpa_or_marks < 3:
                    return (20)
                elif msc_marks.cgpa_or_marks >= 3 and msc_marks.cgpa_or_marks < 3.3:
                    return (28)
                elif msc_marks.cgpa_or_marks >= 3.3 and msc_marks.cgpa_or_marks < 3.7:
                    return (36)
                else:
                    return (40)

        else:
            return 0

    def bs_marks(self, bs_marks):
        if bs_marks:
            if bs_marks.cgpa_or_marks > 0 and bs_marks.cgpa_or_marks >= 2.5 and bs_marks.cgpa_or_marks < 3:
                return (30)
            elif bs_marks.cgpa_or_marks >= 3 and bs_marks.cgpa_or_marks < 3.3:
                return (42)
            elif bs_marks.cgpa_or_marks >= 3.3 and bs_marks.cgpa_or_marks < 3.7:
                return (54)
            else:
                return (60)
        else:
            return 0

    def calculate_ms_aggregate(self):
        for rec in self.admission_ids:
            education_marks = 0
            metric_marks = rec.education_detail_ids.filtered(
                lambda x: x.previous_degrees == '1')
            fsc_marks = rec.education_detail_ids.filtered(
                lambda x: x.previous_degrees == '2')
            bsc_marks = rec.education_detail_ids.filtered(
                lambda x: x.previous_degrees == '6')
            msc_marks = rec.education_detail_ids.filtered(
                lambda x: x.previous_degrees == '4')
            bs_marks = rec.education_detail_ids.filtered(
                lambda x: x.previous_degrees == '3')
            if not bs_marks:
                education_marks = self.matric_marks(metric_marks) + self.fsc_marks(fsc_marks) + self.bsc_marks(
                    bsc_marks) + self.msc_marks(msc_marks)
            elif bsc_marks:
                education_marks = self.matric_marks(metric_marks) + self.fsc_marks(fsc_marks) + self.bs_marks(bs_marks)
            rec.ag_score = education_marks + rec.interview_score
        if self.admission_ids:
            self.ag_done = True


class OpAdmissionEducationDetail(models.Model):
    _inherit = "op.admission.education.detail"

    level = fields.Selection([('matric', 'Matric'), ('fsc', 'F.Sc.'), ('bs', 'Graduation'), ('ms', 'Post Graduation')],
                             string="Degree Level")

# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

import json
from odoo import models, fields, api
import base64
from datetime import datetime
from ..omrs import main
from ..omrs import cropimage


class OpOmrExam(models.Model):
    _name = 'op.omr.exam'
    _description = "Omr Exam"
    _inherit = ['mail.thread']
    _rec_name = 'name'

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('self.sequence')
        return super(OpOmrExam, self).create(vals)

    def action_draft_progressbar(self):
        self.write({'state': 'draft'})

    def action_confirm_progressbar(self):
        self.write({'state': 'confirm'})

    def action_cancel_progressbar(self):
        self.write({'state': 'cancel'})

    def action_done_progressbar(self):
        self.write({'state': 'done'})

    def action_check_state(self):
        flag = False
        if self.state == 'done':
            flag = True
        return flag

    def action_prev_omr_sheet(self):
        sample = 0
        for data in self.answer_sheets_line:
            sample = data
        new_dict = {}
        new_dict['Student Name'] = sample.student_id.name
        new_dict['Roll Number'] = sample.roll_number
        new_dict['Paper Set'] = sample.key_type
        new_dict['Right Answers'] = sample.right_answer
        new_dict['Wrong Answers'] = sample.wrong_answer
        new_dict['Not Attempted'] = sample.not_attampted
        new_dict['Total Score'] = sample.score
        return new_dict

    def action_check_omr_sheet(self):
        flag = False
        json_data = self.template_id.json_data
        template_data = json.loads(json_data)
        answer_dict = {}
        for data1 in self.answersheet_configuration_id.answer_set_line:
            question_answer = {}
            for i in data1.question_answer_line:
                answer = i.answer
                if answer:
                    question_answer['q' + str(i.question)] = i.answer.upper()
                else:
                    question_answer['q' + str(i.question)] = ''
            answer_dict[data1.paper_set.upper()] = question_answer
        temp = 0
        for i in self.omr_image_line:
            temp = i
        input_data = base64.decodebytes(temp.image)
        Omrcrop = cropimage.Cropimage.start_crop(input_data)
        if Omrcrop is False:
            flag = False
            return flag
        else:
            demo = main.start_check(Omrcrop, template_data)
            data = demo[0]
            if len(data['Roll']) == 10:
                for key, value in answer_dict.items():
                    if key == data['key_type']:
                        flag = data['Roll']
                        right_answer = 0
                        wrong_answer = 0
                        not_attampted = 0
                        for key in value:
                            if value[key] == data[key]:
                                right_answer = right_answer + 1
                            elif data[key] == '':
                                not_attampted = not_attampted + 1
                            else:
                                wrong_answer = wrong_answer + 1

                        score = right_answer
                        date_time = datetime.now()
                        roll_number = flag.lstrip('0')
                        student_id = self.env['op.student'].sudo().search([
                            ('course_detail_ids.roll_number', '=', roll_number)])
                        self.answer_sheets_line = [
                            (0, 0, {'roll_number': data['Roll'],
                                    'key_type': data['key_type'],
                                    'right_answer': right_answer,
                                    'wrong_answer': wrong_answer,
                                    'not_attampted': not_attampted,
                                    'score': score,
                                    'date_time': date_time,
                                    'student_id': student_id.id,
                                    'image_id': temp.id})]
                        return flag
                    else:
                        flag = 2
            else:
                flag = 3
        return flag

    name = fields.Char(string="Exam Name", readonly=True,
                       required=True, copy=False, default='EXAM')
    subject_id = fields.Many2one('op.subject', required=True,
                                 readonly=True,
                                 states={'draft': [('readonly', False)]})
    omr_image_line = fields.One2many('op.omr.image',
                                     'omr_exam_id', string="Omr Images",
                                     readonly=True,
                                     states={'draft': [('readonly', False)]})
    template_id = fields.Many2one("op.omr.template", readonly=True,
                                  required=True,
                                  states={'draft': [('readonly', False)]})
    answersheet_configuration_id = fields.Many2one("op.answersheet.configuration",
                                                   readonly=True,
                                                   string="Answer Sheet",
                                                   required=True,
                                                   states={
                                                       'draft': [('readonly', False)]
                                                   })
    answer_sheets_line = fields.One2many("op.answer.sheets", "omr_exam_id",
                                         readonly=True,
                                         states={'draft': [('readonly', False)]})
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('cancel', 'Cancel'),
        ('done', 'Done'),
    ], 'Status', default='draft', tracking=True)

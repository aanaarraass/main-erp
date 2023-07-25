# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################


from odoo import api, fields, models


class WizardTerminology(models.TransientModel):
    _name = "wizard.terminology"
    _description = 'Terminology'
    terminology_setting_id = fields.Many2one('terminology.configuration', 'Terminology')

    @api.onchange('terminology_setting_id')
    def terminology_setting_id_change(self):
        context = dict(self.env.context)
        active_id = context.get('active_id')
        config_id = self.env['res.config.settings'].browse(active_id)
        terminology_old_data = self.env['terminology.configuration'].\
            browse(config_id.terminology_setting_id.id)
        terminology_new_data = self.env['terminology.configuration'].\
            browse(self.terminology_setting_id.id)

        if config_id.terminology_setting_id:
            terminology_new_data.update({
                'course_old_label':
                    terminology_old_data.course_new_label,
                'subject_old_label':
                    terminology_old_data.subject_new_label,
                'batch_old_label':
                    terminology_old_data.batch_new_label,
                'student_old_label':
                    terminology_old_data.student_new_label,
                'faculty_old_label':
                    terminology_old_data.faculty_new_label,
                'course_old_label_plural':
                    terminology_old_data.course_new_label_plural,
                'subject_old_label_plural':
                    terminology_old_data.subject_new_label_plural,
                'batch_old_label_plural':
                    terminology_old_data.batch_new_label_plural,
                'student_old_label_plural':
                    terminology_old_data.student_new_label_plural,
                'faculty_old_label_plural':
                    terminology_old_data.faculty_new_label_plural,
            })

    @api.model
    def default_get(self, fields):
        res = super(WizardTerminology, self).default_get(fields)
        context = dict(self.env.context)
        active_id = context.get('active_id')
        config_id = self.env['res.config.settings'].browse(active_id)
        terminology_data = self.env['terminology.configuration'].\
            browse(config_id.terminology_setting_id)
        if config_id.terminology_setting_id:
            res.update({
                'terminology_setting_id': terminology_data.id,
            })
        return res

    def change_name(self):
        context = dict(self.env.context)
        active_id = context.get('active_id')
        config_id = self.env['res.config.settings'].browse(active_id)
        if config_id.terminology_setting_id:
            terminology_new_data = self.env['terminology.configuration'].\
                browse(self.terminology_setting_id.id)
            self.env['ir.config_parameter'].set_param('terminology_template',
                                                      self.terminology_setting_id.id)
            terminology_new_data.label_name_change()

        else:
            self.env['ir.config_parameter'].set_param('terminology_template',
                                                      self.terminology_setting_id.id)
            terminology_new_data = self.env['terminology.configuration'].\
                browse(self.terminology_setting_id.id)
            terminology_new_data.label_name_change()

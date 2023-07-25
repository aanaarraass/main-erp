# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################


from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    terminology_setting_id = fields.Many2one('terminology.configuration', 'Terminology',
                                             config_parameter="terminology_template")


class TerminologyConfiguration(models.Model):
    _name = 'terminology.configuration'
    _inherit = ['mail.thread']
    _description = 'Terminology Configuration'

    # FOR SINGULAR

    name = fields.Char('Name', index=True, tracking=True)
    base_course_label = fields.Char('Base Course Label',
                                    readonly=True,
                                    default="Course")
    course_old_label = fields.Char('Course Old Label', readonly=True)
    course_new_label = fields.Char('Course New Label')

    base_subject_label = fields.Char('Base Subject Label',
                                     readonly=True, default="Subject")
    subject_old_label = fields.Char('Subject Old Label', readonly=True)
    subject_new_label = fields.Char('Subject New Label')

    base_batch_label = fields.Char('Base Batch Label',
                                   readonly=True, default="Batch")
    batch_old_label = fields.Char('Batch Old Label', readonly=True)
    batch_new_label = fields.Char('Batch New Label')

    base_student_label = fields.Char('Base Student Label',
                                     readonly=True, default="Student")
    student_old_label = fields.Char('Student Old Label', readonly=True)
    student_new_label = fields.Char('Student New Label')

    base_faculty_label = fields.Char('Base Faculty Label',
                                     readonly=True, default="Faculty")
    faculty_old_label = fields.Char('Faculty Old Label', readonly=True)
    faculty_new_label = fields.Char('Faculty New Label')

    # FOR PLURAL
    base_course_label_plural = fields.Char('Base Course Labels', readonly=True)
    course_old_label_plural = fields.Char('Course Old Labels', readonly=True)
    course_new_label_plural = fields.Char('Course New Labels')

    base_subject_label_plural = fields.Char('Base Subject Labels', readonly=True)
    subject_old_label_plural = fields.Char('Subject Old Labels', readonly=True)
    subject_new_label_plural = fields.Char('Subject New Labels')

    base_batch_label_plural = fields.Char('Base Batch Labels', readonly=True)
    batch_old_label_plural = fields.Char('Batch Old Labels', readonly=True)
    batch_new_label_plural = fields.Char('Batch New Labels')

    base_student_label_plural = fields.Char('Base Student Labels', readonly=True)
    student_old_label_plural = fields.Char('Student Old Labels', readonly=True)
    student_new_label_plural = fields.Char('Student New Labels')

    base_faculty_label_plural = fields.Char('Base Faculty Labels', readonly=True)
    faculty_old_label_plural = fields.Char('Faculty Old Labels', readonly=True)
    faculty_new_label_plural = fields.Char('Faculty New Labels')

    def execute_expression(self, exp, var1, var2, domain, var3):
        data = ("%s%s', '%s') %s '%s';") % (exp, var1, var2, domain, var3)
        query = data.format(self._table)
        self.env.cr.execute(query)

    def label_change_query(self, old_label_singular, new_label_singular,
                           old_label_plural, new_label_plural):

        view_type = ['qweb', 'kanban', 'form', 'graph', 'pivot',
                     'search', 'tree', 'activity', 'calendar']

        exp1 = "update ir_model_fields set field_description = " \
               "regexp_replace(field_description,'(?i)"
        if old_label_plural and new_label_plural:
            domain = "where field_description ~*"
            self.execute_expression(exp1, old_label_plural, new_label_plural,
                                    domain, old_label_plural)
        if old_label_singular and new_label_singular:
            domain = 'where field_description ~*'
            self.execute_expression(exp1, old_label_singular, new_label_singular,
                                    domain, old_label_singular)

        exp2 = "update ir_ui_menu set name = regexp_replace(name,'(?i)"
        if old_label_plural and new_label_plural:
            domain = "where name = "
            self.execute_expression(exp2, old_label_plural, new_label_plural,
                                    domain, old_label_plural)
        if old_label_singular and new_label_singular:
            domain = 'where name ~*'
            self.execute_expression(exp2, old_label_singular, new_label_singular,
                                    domain, old_label_singular)

        exp3 = "update ir_actions set name = regexp_replace(name,'(?i)"
        if old_label_plural and new_label_plural:
            domain = "where name ="
            self.execute_expression(exp3, old_label_plural, new_label_plural,
                                    domain, old_label_plural)
        if old_label_singular and new_label_singular:
            domain = 'where name ~*'
            self.execute_expression(exp3, old_label_singular, new_label_singular,
                                    domain, old_label_singular)

        exp4 = "update ir_model set name = regexp_replace(name,'(?i)"
        if old_label_plural and new_label_plural:
            domain = "where name ="
            self.execute_expression(exp4, old_label_plural, new_label_plural,
                                    domain, old_label_plural)
        if old_label_singular and new_label_singular:
            domain = 'where name ~*'
            self.execute_expression(exp4, old_label_singular, new_label_singular,
                                    domain, old_label_singular)

        exp5 = "update ir_act_report_xml set print_report_name = " \
               "regexp_replace(print_report_name,'(?i)"
        if old_label_plural and new_label_plural:
            domain = "where print_report_name ="
            self.execute_expression(exp5, old_label_plural, new_label_plural,
                                    domain, old_label_plural)
        if old_label_singular and new_label_singular:
            domain = 'where print_report_name ~*'
            self.execute_expression(exp5, old_label_singular, new_label_singular,
                                    domain, old_label_singular)

        exp6 = "update ir_ui_view set arch_db = regexp_replace(arch_db,'(?i)[ ]%s"
        if old_label_plural and new_label_plural:
            kanban_data_plural = exp6 % ("%s', '%s','g') where type = 'kanban' and "
                                         "arch_db ~* '%s';" % (str(old_label_plural),
                                                               str(new_label_plural),
                                                               str(old_label_plural)))
            kanban_query_plural = kanban_data_plural.format(self._table)
            self.env.cr.execute(kanban_query_plural)
        if old_label_singular and new_label_singular:
            kanban_data_singular = exp6 % ("%s', '%s','g') where type = 'kanban' and "
                                           "arch_db ~* '%s';" %
                                           (str(old_label_singular),
                                            str(new_label_singular),
                                            str(old_label_singular)))
            kanban_query_singular = kanban_data_singular.format(self._table)
            self.env.cr.execute(kanban_query_singular)

        for value in view_type:
            exp7 = "update ir_ui_view set arch_db = regexp_replace(arch_db,'(?i)[ ]%s"
            if old_label_plural and new_label_plural:
                data_view_plural = exp7 % ("%s[ |:|.|=]', ' %s ','g') where "
                                           "type = '%s' and arch_db = '%s';" %
                                           (str(old_label_plural),
                                            str(new_label_plural),
                                            str(value), str(old_label_plural)))
                data_query_plural = data_view_plural.format(self._table)
                self.env.cr.execute(data_query_plural)
            if old_label_singular and new_label_singular:
                data_view_singular = exp7 % ("%s[ |:|.|=]', ' %s ','g') where "
                                             "type = '%s' and arch_db ~* '%s';" %
                                             (str(old_label_singular),
                                              str(new_label_singular),
                                              str(value), str(old_label_singular)))
                data_query_singular = data_view_singular.format(self._table)
                self.env.cr.execute(data_query_singular)

            exp8 = "update ir_ui_view set arch_db = regexp_replace(arch_db,'(?i)%s"
            if old_label_plural and new_label_plural:
                data_ui_view_plural = exp8 % ("%s[ |:|.|=]', ' %s ','g') where"
                                              " type = '%s' and arch_db ='%s';" %
                                              (str(old_label_plural),
                                               str(new_label_plural),
                                               str(value), str(old_label_plural)))
                query_ui_view_plural = data_ui_view_plural.format(self._table)
                self.env.cr.execute(query_ui_view_plural)
            if old_label_singular and new_label_singular:
                data_ui_view_singular = exp8 % ("%s[ |:|.|=]', ' %s ','g') where "
                                                "type = '%s' and arch_db ~* '%s';" %
                                                (str(old_label_singular),
                                                 str(new_label_singular),
                                                 str(value), str(old_label_singular)))
                query_ui_view_singular = data_ui_view_singular.format(self._table)
                self.env.cr.execute(query_ui_view_singular)

    def label_name_change(self):
        models_str = self.env['ir.config_parameter'].sudo(). \
            get_param('terminology_template')
        term = self.env['terminology.configuration'].browse(int(models_str))
        for data in term:
            if data.course_new_label and data.course_new_label_plural:
                self.label_change_query(self.base_course_label,
                                        self.course_new_label,
                                        self.base_course_label_plural,
                                        self.course_new_label_plural)

                self.label_change_query(self.course_old_label,
                                        self.course_new_label,
                                        self.course_old_label_plural,
                                        self.course_new_label_plural)

            if data.subject_new_label and data.subject_new_label_plural:
                self.label_change_query(self.base_subject_label,
                                        self.subject_new_label,
                                        self.base_subject_label_plural,
                                        self.subject_new_label_plural)

                self.label_change_query(self.subject_old_label,
                                        self.subject_new_label,
                                        self.subject_old_label_plural,
                                        self.subject_new_label_plural)

            if data.batch_new_label and data.batch_new_label_plural:
                self.label_change_query(self.base_batch_label,
                                        self.batch_new_label,
                                        self.base_batch_label_plural,
                                        self.batch_new_label_plural)

                self.label_change_query(self.batch_old_label,
                                        self.batch_new_label,
                                        self.batch_old_label_plural,
                                        self.batch_new_label_plural)

            if data.student_new_label and data.student_new_label_plural:
                self.label_change_query(self.base_student_label,
                                        self.student_new_label,
                                        self.base_student_label_plural,
                                        self.student_new_label_plural)

                self.label_change_query(self.student_old_label,
                                        self.student_new_label,
                                        self.student_old_label_plural,
                                        self.student_new_label_plural)

            if data.faculty_new_label and data.faculty_new_label_plural:
                self.label_change_query(self.base_faculty_label,
                                        self.faculty_new_label,
                                        self.base_faculty_label_plural,
                                        self.faculty_new_label_plural)

                self.label_change_query(self.faculty_old_label,
                                        self.faculty_new_label,
                                        self.faculty_old_label_plural,
                                        self.faculty_new_label_plural)

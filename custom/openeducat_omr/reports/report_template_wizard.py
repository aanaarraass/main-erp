# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################


from odoo import models, api


class HundredReportTemplate(models.AbstractModel):
    _name = "report.openeducat_omr.report_layout_hundred"
    _description = "100 Omr Sheet Layout"

    @api.model
    def _get_report_values(self, docids, data=None):
        option = int(data['form']['option'])
        que = int(data['form']['que'])
        instruction = data['form']['instruction']
        signature = data['form']['signature']
        batch = data['form']['batch']
        mobile_no = data['form']['mobile_no']
        date = data['form']['date']
        var_que = que // 10
        is_five = False
        if que % 10 != 0:
            is_five = True

        fields = {'option': option, 'que': que, 'var_que': var_que,
                  'five': is_five, 'instruction': instruction, 'signature': signature,
                  'batch': batch, 'mobile_no': mobile_no, 'date': date}
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'fields': fields,
            'docs': docs,
        }

# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

from odoo import fields, models


class TemplateWizard(models.TransientModel):
    _name = 'op.omr.template.wizard'
    _description = "Omr Sheet Generate"

    no_option = fields.Selection(
        string='No of Options',
        selection=[('4', 'Four'),
                   ('5', 'Five')], default='4', required=True
    )
    no_que = fields.Selection(
        string='No of Questions',
        selection=[('20', 20), ('50', 50), ('100', 100)], default='20', required=True)

    instruction = fields.Boolean(string='Instruction Block', default=True)
    signature = fields.Boolean(string='Signature Block', default=True)
    batch = fields.Boolean(string='Batch Field', default=True)
    mobile_no = fields.Boolean(string='Mobile No', default=True)
    date = fields.Boolean(string='Date', default=True)

    def get_template(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'option': self.no_option,
                'que': self.no_que,
                'instruction': self.instruction,
                'signature': self.signature,
                'batch': self.batch,
                'mobile_no': self.mobile_no,
                'date': self.date
            },
        }
        return self.env.ref('openeducat_omr.action_omr_sheet_template_report'). \
            report_action(self, data=data)

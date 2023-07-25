# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields


class RegisterFeeQuota(models.Model):
    _name = 'register.fee.quota'
    _rec_name = 'quota_id'

    quota_id = fields.Many2one(comodel_name='op.admission.quota', string="Quota")
    amount = fields.Float('Amount')

# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import fields, models

class PosConfig(models.Model):
    _inherit = 'pos.config'
    
    invoice_offline = fields.Boolean(string="Invoice Offline", help="Enalble this options to Invoice the Orders when POS is Offline.", default=True)
    download_invoice = fields.Boolean(string="Download Invoice", help="Enable this option to download the invoice when the connection is restored.", default=True)

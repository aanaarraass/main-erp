# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "POS Invoice Offline",
  "summary"              :  """This module allows to generate invoices even if the POS is offline.Offline Invoice|Download Invoice|Download Offline Invoice.""",
  "category"             :  "Point Of Sale",
  "version"              :  "1.0.0",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com",
  "description"          :  """Odoo POS Invoice Offline.
  Download Invoice
  Offline Invoice
  Invoice Download Offline
  Offline Downlaod Invoice
  Generate Invoice Offline
  Invoice Generate""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=wk_pos_invoice_offline&custom_url=/pos/auto",
  "depends"              :  ['point_of_sale'],
  "data"                 :  ['views/pos_config_view.xml',],
  "demo"                 :  ['demo/demo.xml'],
  "images"               :  ['static/description/banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "assets"               :  {
                              'point_of_sale.assets': ["/wk_pos_invoice_offline/static/src/js/models.js"],
                            },
  "price"                :  69,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
}

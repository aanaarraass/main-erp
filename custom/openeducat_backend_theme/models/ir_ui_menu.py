# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################
from odoo import models


class IrUiMenu(models.Model):
    _inherit = "ir.ui.menu"

    def load_web_menus(self, debug):
        res = super(IrUiMenu, self).load_web_menus(debug=debug)
        menus = self.load_menus(debug)
        for menu in menus.values():
            if res.get(menu['id']):
                res.get(menu['id']).update({
                    "parentId": menu['parent_id'][0] if menu['parent_id'] else False,
                })
        return res

# -*- coding: utf-8 -*-
# from odoo import http


# class JtsSale(http.Controller):
#     @http.route('/jts_sale/jts_sale', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/jts_sale/jts_sale/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('jts_sale.listing', {
#             'root': '/jts_sale/jts_sale',
#             'objects': http.request.env['jts_sale.jts_sale'].search([]),
#         })

#     @http.route('/jts_sale/jts_sale/objects/<model("jts_sale.jts_sale"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('jts_sale.object', {
#             'object': obj
#         })

# -*- coding: utf-8 -*-
# from odoo import http


# class EstateCommission(http.Controller):
#     @http.route('/estate_commission/estate_commission', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/estate_commission/estate_commission/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('estate_commission.listing', {
#             'root': '/estate_commission/estate_commission',
#             'objects': http.request.env['estate_commission.estate_commission'].search([]),
#         })

#     @http.route('/estate_commission/estate_commission/objects/<model("estate_commission.estate_commission"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('estate_commission.object', {
#             'object': obj
#         })

# -*- coding: utf-8 -*-
# from odoo import http


# class ExamManagement(http.Controller):
#     @http.route('/exam_management/exam_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/exam_management/exam_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('exam_management.listing', {
#             'root': '/exam_management/exam_management',
#             'objects': http.request.env['exam_management.exam_management'].search([]),
#         })

#     @http.route('/exam_management/exam_management/objects/<model("exam_management.exam_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('exam_management.object', {
#             'object': obj
#         })

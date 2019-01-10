# -*- coding: utf-8 -*-
from odoo import http

# class Inheritance(http.Controller):
#     @http.route('/inheritance/inheritance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inheritance/inheritance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inheritance.listing', {
#             'root': '/inheritance/inheritance',
#             'objects': http.request.env['inheritance.inheritance'].search([]),
#         })

#     @http.route('/inheritance/inheritance/objects/<model("inheritance.inheritance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inheritance.object', {
#             'object': obj
#         })
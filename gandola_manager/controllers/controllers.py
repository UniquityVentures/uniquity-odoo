# -*- coding: utf-8 -*-
# from odoo import http


# class GandolaManager(http.Controller):
#     @http.route('/gandola_manager/gandola_manager', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gandola_manager/gandola_manager/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gandola_manager.listing', {
#             'root': '/gandola_manager/gandola_manager',
#             'objects': http.request.env['gandola_manager.gandola_manager'].search([]),
#         })

#     @http.route('/gandola_manager/gandola_manager/objects/<model("gandola_manager.gandola_manager"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gandola_manager.object', {
#             'object': obj
#         })


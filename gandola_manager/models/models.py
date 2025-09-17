# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Gandola(models.Model):
    _name = 'gandola_manager.gandola'
    _description = 'Gandola Management'

    name = fields.Char(string='Gandola Name', required=True)
    current_site = fields.Many2one('gandola_manager.site', string='Current Site')
    sites = fields.Many2many('gandola_manager.site', string='Associated Sites')


class Site(models.Model):
    _name = 'gandola_manager.site'
    _description = 'Site Management'

    name = fields.Char(string='Site Name', required=True)
    address = fields.Text(string='Address')
    gandolas = fields.One2many('gandola_manager.gandola', 'current_site', string='Gandolas')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')


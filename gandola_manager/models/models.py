# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Gandola(models.Model):
    _name = 'gandola_manager.gandola'
    _description = 'Gandola Management'

    name = fields.Char(string='Gandola Name', required=True)
    lending_records = fields.Many2one('gandola_manager.lending_record')


class LendingRecord(models.Model):
    _name = 'gandola_manager.lending_record'
    _description = 'Lending Records'

    gandola = fields.One2many('gandola_manager.gandola', 'lending_records')
    site = fields.One2many('gandola_manager.site', 'lending_records')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')


class Site(models.Model):
    _name = 'gandola_manager.site'
    _description = 'Site Management'

    name = fields.Char(string='Site Name', required=True)
    address = fields.Text(string='Address')
    lending_records = fields.Many2one('gandola_manager.lending_record')
    invoices = fields.Many2one('gandola_manager.invoice')

class Invoice(models.Model):
    _name = 'gandola_manager.invoice'
    _description = 'Invoice Management'

    site = fields.One2many('gandola_manager.site', 'invoices')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

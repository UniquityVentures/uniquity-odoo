# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Gandola(models.Model):
    _name = 'gandola_manager.gandola'
    _description = 'Gandola Management'

    name = fields.Char(string='Gandola Name', required=True)
    lending_records = fields.Many2one('gandola_manager.lending_record', "gandola")


class LendingRecord(models.Model):
    _name = 'gandola_manager.lending_record'
    gandola = fields.One2many('gandola_manager.gandola', 'lending_records')
    site = fields.One2many('gandola_manager.site', 'lending_records')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')


class Site(models.Model):
    _name = 'gandola_manager.site'
    _description = 'Site Management'

    name = fields.Char(string='Site Name', required=True)
    address = fields.Text(string='Address')
    lending_records = fields.Many2one('gandola_manager.lending_record', "site")
    invoices = fields.Many2one('gandola_manager.invocie', "site")

class Invoice(models.Model):
    _name = 'gandola_manager.invoice'
    site = fields.One2many('gandola_manager.site', 'invoices')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

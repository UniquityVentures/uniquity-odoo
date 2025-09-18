# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Gandola(models.Model):
    _name = "gandola_manager.gandola"
    _description = "Gandola Management"

    name = fields.Char(string="Gandola Name", required=True)
    site_ids = fields.Many2many("gandola_manager.site", string="Sites")
    current_site_id = fields.Many2one("gandola_manager.site", string="Current Site", compute="_compute_current_site", store=False)
    is_assigned = fields.Boolean(string="Is Currently Assigned", compute="_compute_current_site", store=False)

    @api.depends('site_ids', 'site_ids.start_date', 'site_ids.end_date')
    def _compute_current_site(self):
        today = fields.Date.context_today(self)
        for gandola in self:
            current_site = False
            for site in gandola.site_ids:
                # Check if today falls between start_date and end_date (inclusive)
                if site.start_date and site.end_date:
                    if site.start_date <= today <= site.end_date:
                        current_site = site
                        break
                # If only start_date is set, check if today is after start_date
                elif site.start_date and not site.end_date:
                    if site.start_date <= today:
                        current_site = site
                        break
                # If only end_date is set, check if today is before end_date
                elif not site.start_date and site.end_date:
                    if today <= site.end_date:
                        current_site = site
                        break
            
            gandola.current_site_id = current_site
            gandola.is_assigned = bool(current_site)


class ResCompany(models.Model):
    _inherit = 'res.company'

    gandola_products = fields.Many2many("product.product", string="Products for invoice generation")
    gandola_payment_term = fields.Many2one("account.payment.term", "Invoice payment term")


class GandolaSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    gandola_product_ids = fields.Many2many(
        "product.product", 
        string="Products for invoice generation", 
        related='company_id.gandola_products', 
        readonly=False
    )
    gandola_payment_term_id = fields.Many2one(
        "account.payment.term", 
        "Invoice payment term",
        related='company_id.gandola_payment_term', 
        readonly=False
    )


class Site(models.Model):
    _name = "gandola_manager.site"
    _description = "Site Management"

    name = fields.Char(string="Site Name", required=True)
    address = fields.Text(string="Address")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    gandola_ids = fields.Many2many("gandola_manager.gandola", string="Gandolas")
    customer_id = fields.Many2one("res.partner", string="Customer", required=True)
    invoice_ids = fields.One2many("account.move", "site_id", string="Invoices")
    status = fields.Selection([
        ('started', 'Started'),
        ('docs_done', 'Docs Done'),
        ('completed', 'Completed'),
        ('payment_settled', 'Payment Settled')
    ], string="Status", default='started')

    @api.model
    def create(self, vals):
        new_site_record = super(Site, self).create(vals)

        if not new_site_record.customer_id:
            return new_site_record

        products = self.env.company.gandola_products
        payment_term = self.env.company.gandola_payment_term

        for product in products:
            self.env["account.move"].create({
                "partner_id": new_site_record.customer_id.id,
                "move_type": "out_invoice",
                "invoice_date": fields.Date.context_today(self),
                "invoice_payment_term_id": payment_term,
                "site_id": new_site_record.id,
                "invoice_line_ids": [(0, 0, {
                    "product_id": product.id,
                    "quantity": 2,
                })],
            })

        return new_site_record


class AccountMove(models.Model):
    _inherit = "account.move"

    site_id = fields.Many2one("gandola_manager.site", string="Related Site", index=True)


class ResPartner(models.Model):
    _inherit = "res.partner"

    site_ids = fields.One2many("gandola_manager.site", "customer_id", string="Sites")
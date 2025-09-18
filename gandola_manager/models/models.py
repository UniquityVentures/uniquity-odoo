# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Gandola(models.Model):
    _name = "gandola_manager.gandola"
    _description = "Gandola Management"

    name = fields.Char(string="Gandola Name", required=True)




class GandolaSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    gandola_product_ids = fields.Many2one("product.product", "Products that are used to invoice generation")
    gandola_payment_term_id = fields.Many2one("account.payment.term", "Payment term that will be used in invoices")

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

    @api.model
    def create(self, vals):
        """
        Overrides create to generate one invoice with three product lines.
        """
        # Step 1: Create the site record first to get its ID.
        new_site_record = super(Site, self).create(vals)

        # Ensure a customer is set before proceeding
        if not new_site_record.customer_id:
            return new_site_record

        # Define the product SKUs you want to find.
        products = self.env.company.gandola_products

        payment_term = self.env.company.gandola_payment_term

        for product in products:
            # Prepare the values for one invoice line
            self.env["account.move"].create(
                {
                    "partner_id": new_site_record.customer_id.id,
                    "move_type": "out_invoice",
                    "invoice_date": fields.Date.context_today(self),
                    "invoice_payment_term_id": payment_term,
                    # --- FIX 3: Pass the site's ID to the new inverse field ---
                    # This automatically links the invoice back to this site.
                    "site_id": new_site_record.id,
                    "invoice_line_ids": [
                        (
                            0,
                            0,
                            {
                                "product_id": product.id,
                                "quantity": 2,
                                # The price will be determined automatically based on the product and partner pricelist.
                            },
                        )
                    ],
                }
            )

        # Step 3: Return the created site record.
        return new_site_record


class AccountMove(models.Model):
    """
    Inherit account.move to add the inverse relationship field.
    This is necessary for the One2many field on the 'site' model to work.
    """

    _inherit = "account.move"

    site_id = fields.Many2one("gandola_manager.site", string="Related Site", index=True)


class ResPartner(models.Model):
    """
    Inherit res.partner to add a One2many field to easily see all sites
    associated with a customer directly from the contact form.
    This is optional but good practice for usability.
    """

    _inherit = "res.partner"

    site_ids = fields.One2many("gandola_manager.site", "customer_id", string="Sites")

# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Gandola(models.Model):
    _name = 'gandola_manager.gandola'
    _description = 'Gandola Management'

    name = fields.Char(string='Gandola Name', required=True)


class Site(models.Model):
    _name = 'gandola_manager.site'
    _description = 'Site Management'

    name = fields.Char(string='Site Name', required=True)
    address = fields.Text(string='Address')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    gandola = fields.Many2many('gandola_manager.gandola')
    customer = fields.One2many('res.partner')

    @api.model
    def create(self, vals):
        """
        Overrides the create method to also create an invoice.
        """

        GANDOLA_REF_ID = "GRC_001"
        TPI_REF_ID = "TPI_001"
        DTI_REF_ID = "DTI_001"

        gandola = self.env['product.product'].search([('default_code', '=', GANDOLA_REF_ID)], limit=1)
        tpi = self.env['product.product'].search([('default_code', '=', TPI_REF_ID)], limit=1)
        dti = self.env['product.product'].search([('default_code', '=', DTI_REF_ID)], limit=1)

        # Step 1: Create the original record by calling the parent method
        new_record = super(Site, self).create(vals)

        # Step 2: Prepare and create the invoice
        self.env['account.move'].create({
            'state': 'draft',
            'move_type': 'out_invoice',
            'partner_id': new_record.customer.id,
            'invoice_date': fields.Date.context_today(self),
            'invoice_line_ids': [
                (0, 0, {
                    'product_id': gandola,
                    'quantity': 2,
                })
            ]
        })

        self.env['account.move'].create({
            'state': 'draft',
            'move_type': 'out_invoice',
            'partner_id': new_record.customer.id,
            'invoice_date': fields.Date.context_today(self),
            'invoice_line_ids': [
                (0, 0, {
                    'product_id': tpi,
                    'quantity': 2,
                })
            ]
        })

        self.env['account.move'].create({
            'state': 'draft',
            'move_type': 'out_invoice',
            'partner_id': new_record.customer.id,
            'invoice_date': fields.Date.context_today(self),
            'invoice_line_ids': [
                (0, 0, {
                    'product_id': dti,
                    'quantity': 2,
                })
            ]
        })
        
        # Step 3: Return the created record
        return new_record

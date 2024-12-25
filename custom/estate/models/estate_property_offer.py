#!/usr/bin/env python
# -*- coding:utf-8 -*-

from odoo import models, fields, api

import datetime
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'estate property offer'

    price = fields.Float(string='Price')
    status = fields.Selection(string='Status',
                              selection=[('Accepted', 'Accepted'), ('Refused', 'Refused')],
                              copy=False
                              )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(days=record.validity)
            else:
                record.date_deadline = datetime.datetime.now().date() + timedelta(days=record.validity)

    @api.depends('validity', 'create_date')
    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = 7
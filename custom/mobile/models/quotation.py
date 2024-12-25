#!/usr/bin/env python
# -*- coding: utf-8 -*-


from odoo import models, fields, _, api # _ = GettextAlias()


class Main(models.Model):
    _name = 'mobile.quotation'
    _description = 'estate mobile'

    ddd = fields.Char('abc')


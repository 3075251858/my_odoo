#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import openpyxl

from odoo import models, fields, _, api # _ = GettextAlias()

from tempfile import TemporaryFile

class Main(models.Model):
    _name = 'mobile.main'
    _description = 'estate mobile'

    services = fields.Char('服务名称')
    combo = fields.Char('套餐')
    month_of_purchase = fields.Char('购买月')
    price = fields.Char('月单价')
    total_price = fields.Char('总金额')
    note = fields.Char('备注')
    whitespace = fields.Char('')


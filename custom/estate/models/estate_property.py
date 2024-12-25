#!/usr/bin/env python
# -*- coding: utf-8 -*-

from odoo import models,fields,api

import base64
import openpyxl
from importlib_resources._common import _
from source.odoo.exceptions import UserError
from tempfile import TemporaryFile


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'estate property table'

    name = fields.Char(size=15)
    description = fields.Text()
    postcode = fields.Char(size=15)
    date_availability = fields.Datetime('Availability Date')
    expected_price = fields.Float('expected price', digits=(8, 2)) # 最大8位，小数占2位
    selling_price = fields.Float('selling price', digits=(8, 2))
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean('garage')
    garden = fields.Boolean('garden')
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('West','West')],
        help="garden orientation"
    )

    active = fields.Boolean('Active', default=True, invisible=True)
    state = fields.Selection(
        string='State',
        selection=[('New', 'New'),
                   ('Offer Received', 'Offer Received'),
                   ('Offer Accepted', 'Offer Accepted'),
                   ('Sold', 'Sold'),
                   ('Canceled', 'Canceled')],
        copy=False
    )

    property_type_id = fields.Many2one("estate.property.type", "PropertyType")
    salesman_id = fields.Many2one("res.users", string="Salesman")
    tag_ids = fields.Many2many("estate.property.tag")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False, default=lambda self: self.env.user)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="PropertyOffer")

    def create_customer_from_attachment(self, attachment_ids=None):
        """
        :param attachment_ids: 上传的数据文件ID列表
        """

        attachments = self.env['ir.attachment'].browse(attachment_ids)
        if not attachments:
            raise UserError(_("未找到上传的文件"))

        for attachment in attachments:
            file_name_suffix = attachment.name.split('.')[-1]
            # 针对文本文件，暂时不实现数据存储，仅演示如何处理文本文件
            if file_name_suffix in ['txt', 'html']:  # 文本文件
                lines = base64.decodebytes(attachment.datas).decode('utf-8').split('\n')
                for line in lines:
                    print(line)
            elif file_name_suffix in ['xlsx', 'xls']:  # excel文件
                file_obj = TemporaryFile('w+b')
                file_obj.write(base64.decodebytes(attachment.datas))
                book = openpyxl.load_workbook(file_obj, read_only=False)
                sheets = book.worksheets
                for sheet in sheets:
                    rows = sheet.iter_rows(min_row=2, max_col=3)  # 从第二行开始读取，每行读取3列
                    for row in rows:
                        name_cell, age_cell, description_cell = row
                        self.create(
                            {'name': name_cell.value, 'age': age_cell.value, 'description': description_cell.value})
            else:
                raise UserError(_("不支持的文件类型，暂时仅支持.txt,.html,.xlsx,.xls文件"))

            return {
                'action_type': 'reload',  # 导入成功后，希望前端执行的动作类型， reload-刷新tree列表, do_action-执行action
            }


    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_offer')

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            prices = record.mapped('offer_ids.price')
            if prices:
                record.best_price = max(prices)
            else:
                record.best_price = 0.00

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'North'
        else:
            self.garden_area = 0
            self.garden_orientation = ''
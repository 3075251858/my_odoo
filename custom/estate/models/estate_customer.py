#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import openpyxl

from odoo.exceptions import UserError
from odoo import models, fields, _, api # _ = GettextAlias()

from tempfile import TemporaryFile

class EstateCustomer(models.Model):
    _name = 'estate.customer'
    _description = 'estate customer'

    name = fields.Char()
    age = fields.Integer()
    description = fields.Text()

    def create_customer_from_attachment(self, attachment_ids=None):
        """
        :param attachment_ids: 上传的数据文件ID列表
        """
        print(self)
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
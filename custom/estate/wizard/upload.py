#!/usr/bin/env python
# -*- coding:utf-8 -*-
import base64
import logging
from odoo import models, fields, api
import xlrd
logger = logging.getLogger(__name__)


class DemoWizard(models.TransientModel):
    _inherit = 'estate.customer'
    _name = 'upload.wizard'
    _description = 'upload wizard'
    file = fields.Binary('文件')

    def excel_upload(self):
        book = xlrd.open_workbook(file_contents=base64.decodebytes(self.file))
        sh = book.sheet_by_index(0)
        for rx in range(1 , sh.nrows):
            self.env['estate.customer'].create({
                'name': sh.cell_value(rx, 0),
                'age': sh.cell_value(rx, 1),
                'description': sh.cell_value(rx, 2)
            })
            print(sh.row(rx))

    def create_quotation(self):
        print(self.file)
        print(xlrd.open_workbook(file_contents=base64.decodebytes(self.file)))



from odoo import fields, models, api

# 继承 父模块 library 的 library_book

class Book(models.Model):
    _inherit = 'library.book'

    is_available = fields.Boolean('is Available')
    # help:鼠标以上去显示的提示信息
    isbn = fields.Char(help="Use a valid ISBN-13 or ISBN-10")
    publisher_id = fields.Many2one(index=True)

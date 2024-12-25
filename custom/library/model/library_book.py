from odoo import models, fields, _, api # _ = GettextAlias()

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(string='Title', required=True)
    author = fields.Char(string='Author')
    published_date = fields.Date(string='Published Date')
    isbn = fields.Char('ISBN')
    active = fields.Boolean('Active?',default=True)
    publisher_id = fields.Many2one('res.partner',string='Publisher')
    author_ids = fields.Many2many('res.partner',string='Author_ID')
    image = fields.Binary('Cover')


@api.model
def _check_isbn(self):
    digits = [int(x) for x in self.isbn if x.isdigit()]

    if len(digits) != 13:
        return False

    ponderations = [1, 3] * 6  # 加权系数
    terms = [a * b for a, b in zip(digits[:12], ponderations)]  # 计算前12位的加权和
    remain = sum(terms) % 10  # 求余数
    check = 10 - remain if remain != 0 else 0  # 校验码

    return digits[-1] == check

@api.multi
def button_check_isbn(self):
    for book in self:
        if not book.isbn:
            raise Warning('请提供ISBN：%s' % book.name)
        if book.isbn and book.__check_isbn():
            raise Warning('%s 是一个无效的ISBN' % book.isbn)
    return True
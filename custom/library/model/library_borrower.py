from odoo import models, fields, _, api # _ = GettextAlias()

class LibraryBorrower(models.Model):
    _name = 'library.borrower'
    _description = 'Library Borrower'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    address = fields.Text(string='Address')

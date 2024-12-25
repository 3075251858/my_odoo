from odoo import http
class Books(http.Controller):
    @http.route('/library/books',auth='public', csrf=False)
    def list(self, mod=None,**kwargs):
        Book = http.request.env['library.book']
        books = Book.sudo().search([])
        return http.request.render('library.book_list_template',{'books':books})
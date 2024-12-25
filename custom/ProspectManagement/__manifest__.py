# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'library',
    'version' : '1.0',
    'summary': '无',
    'sequence': 12,
    'description': """
    无介绍
    """,
    'category': '.....',
    'images' : ['static/energy.png'],
    'depends' : ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/library_menu.xml',
        'views/view_library_book.xml',
        'views/view_library_borrower.xml',
        'views/book_list_template.xml',
    ],
    'demo': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

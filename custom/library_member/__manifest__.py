# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'library Members',
    'version' : '1.0',
    'summary': '无',
    'sequence': 12,
    'description': """
    无介绍
    """,
    'category': '.....',
    'depends' : ['library'],
    'data': [
        'security/ir.model.access.csv',
        'views/library_menu.xml',
        'views/library_member.xml'
    ],
    'demo': [

    ],
    # 'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}

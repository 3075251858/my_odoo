# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'mobile',
    'version' : '1.2',
    'summary': '无',
    'sequence': 15,
    'description': """
    无介绍
    """,
    'category': '.....',
    'images' : ['static/energy.png'],
    'depends' : ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/main.xml',
        'views/mobile_menus.xml',
        'views/test.xml',
        'views/webclient_templates.xml',
        'views/quotation.xml',
        'views/huisuanzhang.xml',
        'views/library_menu.xml',
        'static/qweb/homepsge.xml',
        'static/qweb/advantage.xml',
        'static/qweb/process.xml',
        'static/qweb/service.xml',
        'static/qweb/service_context.xml',
    ],
    'demo': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

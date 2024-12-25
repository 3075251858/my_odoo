# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Properties',
    'version' : '1.1',
    'summary': '无',
    'sequence': 15,
    'description': """
    无介绍
    """,
    'category': 'Invoicing Management',
    'images' : ['static/description/icon.png'],
    'depends' : ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_customer_views.xml',
        'views/estate_customer_views.xml',
        'wizard/demo_wizard_views.xml',
        'wizard/upload.xml',
        'views/estate_menus.xml',
        'views/webclient_templates.xml',
    ],
    'demo': [

    ],
    'qweb': [
        'static/src/xml/estate_customer_tree_view_buttons.xml',
        'static/src/xml/tree_view_buttons.xml',
        'static/src/xml/common.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

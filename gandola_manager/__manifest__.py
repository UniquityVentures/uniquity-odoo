# -*- coding: utf-8 -*-
{
    'name': "Gandola",

    'description': """
Gandola Manager App for Uniquity Ventures
=========================================

    """,

    'author': "Uniquity Ventures",
    'category': 'Administration',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    "auto_install": True,
    "license": "LGPL-3",
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}


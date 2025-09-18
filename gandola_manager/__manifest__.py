# -*- coding: utf-8 -*-
{
    "name": "Gandola",
    "description": """
Gandola Manager App for Uniquity Ventures
=========================================

    """,
    "author": "Uniquity Ventures",
    "category": "Inventory",
    "version": "0.2",
    # any module necessary for this one to work correctly
    "depends": ["base", "account", "web"],
    "auto_install": True,
    "license": "LGPL-3",
    # always loaded
    "data": [
        "views/views.xml",
        "views/templates.xml",
        "views/settings.xml",
        "security/ir.model.access.csv",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
}

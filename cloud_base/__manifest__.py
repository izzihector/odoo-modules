# -*- coding: utf-8 -*-
{
    "name": "Cloud Storage Solutions",
    "version": "13.0.1.3.15",
    "category": "Document Management",
    "author": "Odoo Tools",
    "website": "https://odootools.com/apps/13.0/cloud-storage-solutions-430",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "mail"
    ],
    "data": [
        "data/data.xml",
        "data/cron.xml",
        "data/sync_formats_data.xml",
        "views/sync_model.xml",
        "views/ir_attachment.xml",
        "views/sync_log.xml",
        "views/res_config_settings.xml",
        "views/view.xml",
        "security/ir.model.access.csv"
    ],
    "qweb": [
        "static/src/xml/*.xml"
    ],
    "js": [
        
    ],
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The technical core to synchronize your cloud storage solution with Odoo",
    "description": """
For the full details look at static/description/index.html

Automatic integration
Bilateral sync
Sync any documents you like
Easy accessible files
Sync logs in Odoo
Default folders for documents
# Typical use cases
""",
    "images": [
        "static/description/main.png"
    ],
    "price": "130.0",
    "currency": "EUR",
}
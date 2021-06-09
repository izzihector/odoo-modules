# -*- coding: utf-8 -*-
{
    "name": "OneDrive / SharePoint Odoo Integration",
    "version": "13.0.1.3.5",
    "category": "Document Management",
    "author": "Odoo Tools",
    "website": "https://odootools.com/apps/13.0/onedrive-sharepoint-odoo-integration-428",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "cloud_base"
    ],
    "data": [
        "data/data.xml",
        "views/res_config_settings.xml",
        "security/ir.model.access.csv"
    ],
    "qweb": [
        
    ],
    "js": [
        
    ],
    "demo": [
        
    ],
    "external_dependencies": {
        "python": [
                "microsoftgraph-python",
                "requests"
        ]
},
    "summary": "The tool to automatically synchronize Odoo attachments with OneDrive files in both ways",
    "description": """
For the full details look at static/description/index.html

Selectable documents types for sync
Automatic and bilateral integration
Direct access to OneDrive / SharePoint items
Fully integrated and compatible with Enterprise Documents
OneDrive / SharePoint Sync logs in Odoo
Default folders for documents
# Typical use cases
# How files and folders are synced from Odoo to OneDrive / SharePoint
# How items are retrieved from OneDrive / SharePoint to Odoo
# How Odoo Enterprise Documents are synced
# A few other peculiarities to take into account
Quick access to OneDrive / SharePoint files and folders
Apply to OneDrive / SharePoint right from Odoo chatter
Choose document types to be synced
Document type might have a few folders based on filters
Synced files are simply found in OneDrive / SharePoint. Add unlimited number of files or folders
Document types folders in OneDrive / SharePoint
All document of this type has an own folder
Direct access from Odoo documents to OneDrive / SharePoint
Enterprise Documents in OneDrive / SharePoint
Enterprise files in OneDrive / SharePoint
Logged synchronization activities
""",
    "images": [
        "static/description/main.png"
    ],
    "price": "264.0",
    "currency": "EUR",
    "live_test_url": "https://odootools.com/my/tickets/newticket?&url_app_id=44&ticket_version=13.0&url_type_id=3",
}
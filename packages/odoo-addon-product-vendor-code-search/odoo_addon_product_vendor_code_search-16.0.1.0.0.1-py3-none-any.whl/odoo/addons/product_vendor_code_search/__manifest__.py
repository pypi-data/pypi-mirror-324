# Copyright 2025 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Vendor Code Search",
    "summary": "Search products by vendor code",
    "version": "16.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/sygel-technology/sy-product-attribute",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "product",
    ],
    "data": ["views/product_views.xml"],
}

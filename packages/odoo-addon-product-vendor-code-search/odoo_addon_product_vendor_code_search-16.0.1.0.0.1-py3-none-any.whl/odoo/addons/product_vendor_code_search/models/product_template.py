# Copyright 2025 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    seller_code = fields.Char(
        compute="_compute_seller_codes", search="_search_seller_code"
    )

    @api.depends("seller_ids")
    def _compute_seller_code(self):
        for sel in self:
            sel.seller_code = "".join(sel.seller_ids.mapped("product_code"))

    def _search_seller_code(self, operator, value):
        products = self.search([("seller_ids.product_code", operator, value)])
        return [("id", "in", products.ids)]

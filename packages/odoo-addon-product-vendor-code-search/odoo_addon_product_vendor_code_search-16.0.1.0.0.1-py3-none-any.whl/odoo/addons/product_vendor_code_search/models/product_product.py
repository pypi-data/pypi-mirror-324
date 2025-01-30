# Copyright 2025 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    seller_code = fields.Char(
        compute="_compute_seller_codes", search="_search_seller_code"
    )

    @api.depends("seller_ids")
    def _compute_seller_code(self):
        for sel in self:
            sel.seller_code = "".join(sel.seller_ids.mapped("product_code"))

    def _search_seller_code(self, operator, value):
        suppliers = self.env["product.supplierinfo"].search(
            [("product_code", operator, value)]
        )
        products = (
            suppliers.product_id
            + suppliers.filtered(
                lambda a: not a.product_id
            ).product_tmpl_id.product_variant_ids
        )
        return [("id", "in", products.ids)]

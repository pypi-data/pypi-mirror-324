# Copyright 2025 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.fields import Command

from odoo.addons.product.tests.common import ProductAttributesCommon


class TestProductVendorCodeSearch(ProductAttributesCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.product_1 = cls.env["product.template"].create(
            {
                "name": "Product-1",
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": cls.color_attribute.id,
                            "value_ids": [
                                Command.set(
                                    [
                                        cls.color_attribute_red.id,
                                        cls.color_attribute_blue.id,
                                        cls.color_attribute_green.id,
                                    ]
                                )
                            ],
                        }
                    ),
                    Command.create(
                        {
                            "attribute_id": cls.size_attribute.id,
                            "value_ids": [
                                Command.set(
                                    [
                                        cls.size_attribute_s.id,
                                        cls.size_attribute_m.id,
                                        cls.size_attribute_l.id,
                                    ]
                                )
                            ],
                        }
                    ),
                ],
            }
        )
        cls.product_2 = cls.env["product.template"].create(
            {
                "name": "Product-2",
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": cls.color_attribute.id,
                            "value_ids": [
                                Command.set(
                                    [
                                        cls.color_attribute_red.id,
                                        cls.color_attribute_blue.id,
                                        cls.color_attribute_green.id,
                                    ]
                                )
                            ],
                        }
                    ),
                    Command.create(
                        {
                            "attribute_id": cls.size_attribute.id,
                            "value_ids": [
                                Command.set(
                                    [
                                        cls.size_attribute_s.id,
                                        cls.size_attribute_m.id,
                                        cls.size_attribute_l.id,
                                    ]
                                )
                            ],
                        }
                    ),
                ],
            }
        )

        # Product Template Supplierinfo
        cls.env["product.supplierinfo"].create(
            [
                {
                    "partner_id": cls.partner.id,
                    "product_tmpl_id": cls.product_1.id,
                    "product_code": "Product-1-A",
                },
                {
                    "partner_id": cls.partner.id,
                    "product_tmpl_id": cls.product_1.id,
                    "product_code": "Product-1-B",
                },
                {
                    "partner_id": cls.partner.id,
                    "product_tmpl_id": cls.product_2.id,
                    "product_code": "Product-2-A",
                },
                {
                    "partner_id": cls.partner.id,
                    "product_tmpl_id": cls.product_2.id,
                    "product_code": "Product-2-B",
                },
            ]
        )

        # Product Variant Supplierinfo
        cls.env["product.supplierinfo"].create(
            [
                {
                    "partner_id": cls.partner.id,
                    "product_tmpl_id": cls.product_1.id,
                    "product_id": cls.product_1.product_variant_ids[0].id,
                    "product_code": "ProductVariant-1-1-A",
                },
                {
                    "partner_id": cls.partner.id,
                    "product_tmpl_id": cls.product_1.id,
                    "product_id": cls.product_1.product_variant_ids[0].id,
                    "product_code": "ProductVariant-1-1-B",
                },
                {
                    "partner_id": cls.partner.id,
                    "product_tmpl_id": cls.product_1.id,
                    "product_id": cls.product_1.product_variant_ids[1].id,
                    "product_code": "ProductVariant-1-2-A",
                },
                {
                    "partner_id": cls.partner.id,
                    "product_tmpl_id": cls.product_1.id,
                    "product_id": cls.product_1.product_variant_ids[1].id,
                    "product_code": "ProductVariant-1-2-B",
                },
                {
                    "partner_id": cls.partner.id,
                    "product_tmpl_id": cls.product_2.id,
                    "product_id": cls.product_2.product_variant_ids[0].id,
                    "product_code": "ProductVariant-2-1-A",
                },
                {
                    "partner_id": cls.partner.id,
                    "product_tmpl_id": cls.product_2.id,
                    "product_id": cls.product_2.product_variant_ids[0].id,
                    "product_code": "ProductVariant-2-1-B",
                },
                {
                    "partner_id": cls.partner.id,
                    "product_tmpl_id": cls.product_2.id,
                    "product_id": cls.product_2.product_variant_ids[1].id,
                    "product_code": "ProductVariant-2-2-A",
                },
                {
                    "partner_id": cls.partner.id,
                    "product_tmpl_id": cls.product_2.id,
                    "product_id": cls.product_2.product_variant_ids[1].id,
                    "product_code": "ProductVariant-2-2-B",
                },
            ]
        )

    def test_product_template_vendor_code(self):
        # Equals
        product = self.env["product.template"].search(
            [("seller_code", "=", "Product-1")]
        )
        self.assertFalse(product)
        product = self.env["product.template"].search(
            [("seller_code", "=", "Product-1-A")]
        )
        self.assertEqual(len(product), 1)
        # Contains
        product = self.env["product.template"].search(
            [("seller_code", "ilike", "Product-11")]
        )
        self.assertFalse(product)
        product = self.env["product.template"].search(
            [("seller_code", "ilike", "Product")]
        )
        self.assertEqual(len(product), 2)
        # Is set
        product = self.env["product.template"].search([("seller_code", "!=", False)])
        self.assertEqual(len(product), 2)

    def test_product_variant_vendor_code(self):
        # Equals
        product = self.env["product.product"].search(
            [("seller_code", "=", "ProductVariant-1")]
        )
        self.assertFalse(product)
        product = self.env["product.product"].search(
            [("seller_code", "=", "ProductVariant-1-1-A")]
        )
        self.assertEqual(len(product), 1)
        # Contains
        product = self.env["product.product"].search(
            [("seller_code", "ilike", "Product-11")]
        )
        self.assertFalse(product)
        product = self.env["product.product"].search(
            [("seller_code", "ilike", "ProductVariant")]
        )
        self.assertEqual(len(product), 4)
        # Is set
        product = self.env["product.product"].search([("seller_code", "!=", False)])
        self.assertEqual(len(product), 18)

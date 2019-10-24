# -*- coding: utf-8 -*-
# Part of Inceptus ERP Solutions Pvt.ltd.
# See LICENSE file for copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _name = 'product.template'

    _inherit = ["product.template", "ies.base"]

    @api.one
    @api.depends('coupon_ids')
    def _get_giftcard_count(self):
        self.giftcard_count = len(
            self.coupon_ids.filtered(lambda record: record.type in ['f', 'd'] and record.coupon_type == 'gc'))

    # @api.model
    # def _get_discount_type(self):
    #     # res = super(ProductTemplate, self)._get_discount_type()
    #     if self._context.get('giftcard'):
    #         return [('f', 'Fixed'), ('d', 'Dynamic Amount')]

    @api.constrains('discount_amount', 'lst_price')
    def _check_discount_amount(self):
        for rec in self:
            if rec.discount_type == 'f' and rec.discount_amount < rec.lst_price:
                raise ValidationError(_('Discount amount can not be less than sale price!'))

    @api.multi
    def open_giftcards(self):
        domain = [('product_id', '=', self.id)]
        view_id, form_view_id = False, False
        name = False
        if self._context.get('type') == 'gc':
            name = _('Giftcards')
            domain += [('type', 'in', ['f', 'd'])]
            view_id = self.env.ref('ies_giftcards.ies_product_giftcard_tree').id
            form_view_id = self.env.ref('ies_giftcards.ies_product_giftcard_form').id

        return {
            'name': name,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'product.coupon',
            'domain': domain,
            'views': [(view_id, 'tree'), (form_view_id, 'form')]
        }

    giftcard_count = fields.Integer('Giftcard Count', compute="_get_giftcard_count")
    giftcard = fields.Boolean()

    @api.onchange('discount_amount')
    def onchange_discount_amount(self):
        if self.discount_amount:
            self.lst_price = self.discount_amount

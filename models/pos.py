# -*- coding: utf-8 -*-
# Part of Inceptus ERP Solutions Pvt.ltd.
# See LICENSE file for copyright and licensing details.

from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import time


class POSConfig(models.Model):
    _name = 'pos.config'

    _inherit = ["pos.config", "ies.base"]

    allow_discount = fields.Boolean("Discount on giftcard?", help='Allow POS discount on the giftcard?')
# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ResCompany(models.Model):
    """
    Extension point reserved for company-level cost accounting setup.

    Declares no additional fields; kept so other modules in this
    dependency chain can safely extend ``res.company`` for cost
    accounting purposes without introducing a new inherit chain.
    """

    _name = "res.company"
    _inherit = "res.company"

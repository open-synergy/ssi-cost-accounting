# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountAnalyticGroup(models.Model):
    """
    Adds a manual sort order to ``account.analytic.group``.

    The ``sequence`` field lets users control the display order of
    analytic groups in list views and selection widgets.
    """

    _name = "account.analytic.group"
    _inherit = [
        "account.analytic.group",
    ]
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10,
    )

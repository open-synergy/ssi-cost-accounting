# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMove(models.Model):
    """
    Enforces the account move lines' analytic policy when posting.

    Delegates the actual check to
    ``account.move.line._check_analytic_required``.
    """

    _inherit = "account.move"

    def _post(self, soft=True):
        """Re-run the analytic policy check after posting.

        Some policies (``posted``) only apply once a move leaves
        the ``draft`` state, so the check must run again after
        ``super()._post()`` updates the move's state.

        :param soft: whether to post in soft mode (see Odoo core)
        :return: the recordset returned by ``super()._post()``
        """
        res = super()._post(soft=soft)
        self.mapped("line_ids")._check_analytic_required()
        return res

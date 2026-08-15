# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountAccount(models.Model):
    """
    Adds an analytic account policy to ``account.account``.

    The policy controls whether an analytic account is optional,
    always required, required only on posted moves, or forbidden
    on account move lines that use this account.
    """

    _inherit = "account.account"

    property_analytic_policy = fields.Selection(
        selection=[
            ("optional", "Optional"),
            ("always", "Always"),
            ("posted", "Posted moves"),
            ("never", "Never"),
        ],
        string="Policy for analytic account",
        default="optional",
        company_dependent=True,
        help=(
            "Sets the policy for analytic accounts.\n"
            "If you select:\n"
            "- Optional: The accountant is free to put an analytic account "
            "on an account move line with this type of account.\n"
            "- Always: The accountant will get an error message if "
            "there is no analytic account.\n"
            "- Posted moves: The accountant will get an error message if no "
            "analytic account is defined when the move is posted.\n"
            "- Never: The accountant will get an error message if an analytic "
            "account is present.\n\n"
            "This field is company dependent."
        ),
    )

    def _get_analytic_policy(self):
        """Return the analytic account policy configured on this account.

        Extension point: override to compute the policy from a
        source other than ``property_analytic_policy``.

        :return: one of ``optional``, ``always``, ``posted``, ``never``
        """
        self.ensure_one()
        return self.with_company(self.company_id.id).property_analytic_policy

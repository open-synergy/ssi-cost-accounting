# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — NOT HttpCase. HttpCase in 14.0 has no cls.env in
# setUpClass (see structure-and-runner.md "Base class").
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiAccountAccount(HttpSavepointCase):
    """Tour tests for the ``account.account`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the test account and grant the analytic policy group.

        Pre-Condition: the Analytic Policy field is only rendered for
        users in the *Analytic Accounting* group
        (``analytic.group_analytic_accounting``) — without it the tour
        would time out on an element that is never in the DOM.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        cls.env.ref("analytic.group_analytic_accounting").sudo().write(
            {"users": [(4, cls.admin.id)]}
        )
        expense_type = cls.env.ref("account.data_account_type_expenses")
        cls.account = cls.env["account.account"].create(
            {
                "name": "Tour Test Account",
                "code": "CATOUR01",
                "user_type_id": expense_type.id,
                "company_id": cls.env.company.id,
            }
        )

    def test_edit(self):
        """Run the edit tour for ``account.account``.

        IK: docs/account_account/02-edit.md
        """
        self.start_tour(
            "/web", "ssi_cost_accounting_account_account_edit", login="admin"
        )

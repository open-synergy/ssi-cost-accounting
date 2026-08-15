# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiAccountAnalyticGroup(HttpSavepointCase):
    """Tour tests for the ``account.analytic.group`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Prepare the admin session for the create tour.

        No extra fixture is required: the *Analytic Account Group*
        configurator group is granted to ``base.user_admin`` by this
        module's own security data, so the menu is already visible.
        """
        super().setUpClass()

    def test_create(self):
        """Run the create tour for ``account.analytic.group``.

        IK: docs/account_analytic_group/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_cost_accounting_account_analytic_group_create",
            login="admin",
        )

# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiAccountAnalyticTag(HttpSavepointCase):
    """Tour tests for the ``account.analytic.tag`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Prepare the admin session for the access tour.

        No extra fixture is required: the *Analytic Tag* configurator
        group is granted to ``base.user_admin`` by this module's own
        security data, so the menu is already visible.
        """
        super().setUpClass()

    def test_access(self):
        """Run the access tour for ``account.analytic.tag``.

        IK: docs/account_analytic_tag/01-access.md
        """
        self.start_tour(
            "/web", "ssi_cost_accounting_account_analytic_tag_access", login="admin"
        )

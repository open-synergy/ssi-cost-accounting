# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiAccountAnalyticAccountMerge(HttpSavepointCase):
    """Tour test for the ``merge_analytic_account`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the two accounts the merge tour selects and merges.

        "Merge Tour Keep" is created first so it becomes the wizard's
        default destination (smallest ``id``); "Merge Tour Remove" is
        created second so it becomes the source account, deleted by
        the merge. The *Analytic Account* configurator group is
        already granted to ``base.user_admin`` by this module's own
        security data, so no extra group membership is needed.
        """
        super().setUpClass()
        Account = cls.env["account.analytic.account"]  # noqa: N806
        cls.account_keep = Account.create({"name": "Merge Tour Keep"})
        cls.account_remove = Account.create({"name": "Merge Tour Remove"})

    def test_merge(self):
        """Run the merge tour for ``account.analytic.account``.

        IK: docs/account_analytic_account/04-merge.md
        """
        self.start_tour(
            "/web",
            "ssi_cost_accounting_account_analytic_account_merge",
            login="admin",
        )

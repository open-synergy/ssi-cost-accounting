# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestMergeAnalyticAccount(YamlTransactionCase):
    """Scenario tests for the ``merge_analytic_account`` wizard."""

    def test_merge_analytic_account(self):
        """Run the merge wizard scenarios."""
        self.run_yaml_scenario("test_data_merge_analytic_account.yaml")

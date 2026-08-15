# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestCostAccounting(YamlTransactionCase):
    """Scenario tests for ``account.analytic.group``/``.account`` CRUD."""

    def test_cost_accounting(self):
        """Run the analytic group/account CRUD scenario."""
        self.run_yaml_scenario("test_data_cost_accounting.yaml")

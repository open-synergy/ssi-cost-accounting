# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestAccountAnalyticAccount(YamlTransactionCase):
    """Scenario tests for ``account.analytic.account``."""

    def _create_account(self, name, state):
        """Create an analytic account fixture with a given state.

        :param name: name of the analytic account
        :param state: one of ``draft``, ``open``, ``done``
        :return: the created ``account.analytic.account`` record
        """
        return self.env["account.analytic.account"].create(
            {
                "name": name,
                "state": state,
            }
        )

    def test_name_search_excludes_done_by_default(self):
        """Exclude ``done`` accounts from ``name_search`` by default.

        Pure Python — trigger P1 (L-01: ``action: call`` discards the
        method's return value; L-02: an assert's "actual" side is
        always a dotted ``getattr`` on a registered record, so the
        list of ``(id, name)`` tuples returned by ``name_search``
        cannot be asserted from YAML at all).
        """
        draft_account = self._create_account("Draft AA", "draft")
        open_account = self._create_account("Open AA", "open")
        done_account = self._create_account("Done AA", "done")

        results = self.env["account.analytic.account"].name_search(
            name="AA", args=[], operator="ilike", limit=100
        )
        found_ids = [result[0] for result in results]

        self.assertIn(draft_account.id, found_ids)
        self.assertIn(open_account.id, found_ids)
        self.assertNotIn(done_account.id, found_ids)

    def test_name_search_includes_done_with_context_flag(self):
        """Include ``done`` accounts when the bypass context is set.

        Pure Python — trigger P1 (L-01, L-02, same as above): asserts
        the ``(id, name)`` list returned by ``name_search`` under a
        custom context, which YAML cannot inspect.
        """
        done_account = self._create_account("Done AA Bypass", "done")

        results = (
            self.env["account.analytic.account"]
            .with_context(include_done_analytic_account=True)
            .name_search(name="Done AA Bypass", args=[], operator="ilike", limit=100)
        )
        found_ids = [result[0] for result in results]

        self.assertIn(done_account.id, found_ids)

    def test_search_not_affected_by_name_search_override(self):
        """Confirm plain ``search()`` still returns ``done`` accounts.

        The fix intentionally overrides only ``_name_search`` (the
        Many2one autocomplete path), not ``_search``, so reports,
        cron jobs, ``read_group()``, and the "Search More..." list
        dialog keep seeing closed accounts. This guards against a
        future change accidentally widening the override's scope.

        Pure Python — trigger P1 (L-01: ``action: call`` discards
        the method's return value, so the recordset returned by
        ``search()`` cannot be asserted from YAML at all).
        """
        done_account = self._create_account("Done AA Plain Search", "done")

        found = self.env["account.analytic.account"].search(
            [("name", "=", "Done AA Plain Search")]
        )

        self.assertIn(done_account, found)

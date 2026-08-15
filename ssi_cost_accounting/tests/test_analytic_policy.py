# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestAnalyticPolicy(YamlTransactionCase):
    """Scenario tests for the ``account.account`` analytic policy.

    The account move create/post scenarios (optional/always/never/
    posted policy, positive and negative paths) run from
    ``test_data_analytic_policy.yaml``. This class keeps a handful
    of Python-only tests that assert a method's return value, which
    the YAML DSL cannot express.
    """

    def setUp(self):
        """Prepare accounts with each analytic policy for pure tests.

        Builds one account per policy value (``optional``,
        ``always``, ``never``, ``posted``), a counterpart account, a
        general journal, and one analytic account, all scoped to
        ``self.env.company``.
        """
        super().setUp()
        self.company = self.env.company
        expense_type = self.env.ref("account.data_account_type_expenses")

        # Find or create a general journal
        self.journal = self.env["account.journal"].search(
            [("type", "=", "general"), ("company_id", "=", self.company.id)],
            limit=1,
        )
        if not self.journal:
            self.journal = self.env["account.journal"].create(
                {
                    "name": "Test General Journal CA",
                    "code": "TGCA",
                    "type": "general",
                    "company_id": self.company.id,
                }
            )

        # Counterpart account (optional policy — always valid)
        self.account_counterpart = self.env["account.account"].create(
            {
                "name": "Test Counterpart CA",
                "code": "CA99900",
                "user_type_id": expense_type.id,
                "company_id": self.company.id,
            }
        )

        # Account with optional policy (default)
        self.account_optional = self.env["account.account"].create(
            {
                "name": "Test Optional CA",
                "code": "CA99901",
                "user_type_id": expense_type.id,
                "company_id": self.company.id,
            }
        )

        # Account with always policy
        self.account_always = self.env["account.account"].create(
            {
                "name": "Test Always CA",
                "code": "CA99902",
                "user_type_id": expense_type.id,
                "company_id": self.company.id,
            }
        )
        self.account_always.property_analytic_policy = "always"

        # Account with never policy
        self.account_never = self.env["account.account"].create(
            {
                "name": "Test Never CA",
                "code": "CA99903",
                "user_type_id": expense_type.id,
                "company_id": self.company.id,
            }
        )
        self.account_never.property_analytic_policy = "never"

        # Account with posted policy
        self.account_posted = self.env["account.account"].create(
            {
                "name": "Test Posted CA",
                "code": "CA99904",
                "user_type_id": expense_type.id,
                "company_id": self.company.id,
            }
        )
        self.account_posted.property_analytic_policy = "posted"

        # Test analytic account
        self.analytic_account = self.env["account.analytic.account"].create(
            {"name": "Test Analytic CA"}
        )

    def _make_move(self, main_account, amount, analytic_account=None):
        """Create a balanced general journal entry.

        :param main_account: ``account.account`` used on the main line
        :param amount: debit amount posted on the main line
        :param analytic_account: optional ``account.analytic.account``
            set on the main line
        :return: the created ``account.move``
        """
        main_line = {
            "account_id": main_account.id,
            "debit": amount,
            "credit": 0.0,
            "name": "Test main line",
        }
        if analytic_account:
            main_line["analytic_account_id"] = analytic_account.id
        return self.env["account.move"].create(
            {
                "move_type": "entry",
                "journal_id": self.journal.id,
                "line_ids": [
                    (0, 0, main_line),
                    (
                        0,
                        0,
                        {
                            "account_id": self.account_counterpart.id,
                            "debit": 0.0,
                            "credit": amount,
                            "name": "Test counterpart line",
                        },
                    ),
                ],
            }
        )

    def test_analytic_policy_scenarios(self):
        """Run the account move create/post analytic policy scenarios."""
        self.run_yaml_scenario("test_data_analytic_policy.yaml")

    def test_get_analytic_policy_always(self):
        """``_get_analytic_policy`` returns ``always`` after setting it.

        Pure Python — trigger P1 (L-01: ``action: call`` discards
        the method's return value; L-02: an assert's "actual" side
        is always a dotted ``getattr`` on a registered record, so a
        bare method return value cannot be asserted from YAML).
        """
        self.assertEqual(self.account_always._get_analytic_policy(), "always")

    def test_get_analytic_policy_never(self):
        """``_get_analytic_policy`` returns ``never`` after setting it.

        Pure Python — trigger P1 (L-01, L-02, same as above).
        """
        self.assertEqual(self.account_never._get_analytic_policy(), "never")

    def test_get_analytic_policy_optional(self):
        """``_get_analytic_policy`` returns ``optional`` by default.

        Pure Python — trigger P1 (L-01, L-02, same as above).
        """
        self.assertEqual(self.account_optional._get_analytic_policy(), "optional")

    def test_get_analytic_policy_posted(self):
        """``_get_analytic_policy`` returns ``posted`` after setting it.

        Pure Python — trigger P1 (L-01, L-02, same as above).
        """
        self.assertEqual(self.account_posted._get_analytic_policy(), "posted")

    def test_check_analytic_msg_returns_none_for_optional(self):
        """``_check_analytic_required_msg`` returns ``None`` when valid.

        Pure Python — trigger P1 (L-01, L-02, same as above): the
        method's return value (``None`` or an error string) cannot
        be asserted from YAML, since ``call`` discards it.
        """
        line = self._make_move(self.account_optional, 100.0).line_ids.filtered(
            lambda l: l.account_id == self.account_optional
        )
        self.assertIsNone(line._check_analytic_required_msg())

    def test_has_analytic_distribution_false_without_tags(self):
        """``_has_analytic_distribution`` returns ``False`` for no tags.

        Pure Python — trigger P1 (L-01, L-02, same as above): the
        boolean return value of the method cannot be asserted from
        YAML, since ``call`` discards it.
        """
        line = self._make_move(self.account_optional, 100.0).line_ids.filtered(
            lambda l: l.account_id == self.account_optional
        )
        self.assertFalse(line._has_analytic_distribution())

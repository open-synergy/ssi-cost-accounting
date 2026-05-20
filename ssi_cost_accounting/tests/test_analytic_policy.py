# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestAnalyticPolicy(TransactionCase):
    def setUp(self):
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
        """Create a balanced general journal entry."""
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

    def test_get_analytic_policy_optional(self):
        """_get_analytic_policy returns 'optional' for default account."""
        self.assertEqual(self.account_optional._get_analytic_policy(), "optional")

    def test_get_analytic_policy_always(self):
        """_get_analytic_policy returns 'always' after setting the policy."""
        self.assertEqual(self.account_always._get_analytic_policy(), "always")

    def test_get_analytic_policy_never(self):
        """_get_analytic_policy returns 'never' after setting the policy."""
        self.assertEqual(self.account_never._get_analytic_policy(), "never")

    def test_get_analytic_policy_posted(self):
        """_get_analytic_policy returns 'posted' after setting the policy."""
        self.assertEqual(self.account_posted._get_analytic_policy(), "posted")

    def test_optional_policy_no_analytic_create(self):
        """Optional policy: no analytic account → move creates successfully."""
        move = self._make_move(self.account_optional, 100.0)
        self.assertTrue(move.id)

    def test_optional_policy_no_analytic_post(self):
        """Optional policy: no analytic account → move posts successfully."""
        move = self._make_move(self.account_optional, 100.0)
        move.action_post()
        self.assertEqual(move.state, "posted")

    def test_always_policy_with_analytic_create(self):
        """Always policy: with analytic account → move creates successfully."""
        move = self._make_move(self.account_always, 100.0, self.analytic_account)
        self.assertTrue(move.id)

    def test_always_policy_with_analytic_post(self):
        """Always policy: with analytic account → move posts successfully."""
        move = self._make_move(self.account_always, 100.0, self.analytic_account)
        move.action_post()
        self.assertEqual(move.state, "posted")

    def test_always_policy_no_analytic_raises(self):
        """Always policy: no analytic account → ValidationError on create."""
        with self.assertRaises(ValidationError):
            self._make_move(self.account_always, 100.0)

    def test_never_policy_no_analytic_create(self):
        """Never policy: no analytic account → move creates successfully."""
        move = self._make_move(self.account_never, 100.0)
        self.assertTrue(move.id)

    def test_never_policy_no_analytic_post(self):
        """Never policy: no analytic account → move posts successfully."""
        move = self._make_move(self.account_never, 100.0)
        move.action_post()
        self.assertEqual(move.state, "posted")

    def test_never_policy_with_analytic_raises(self):
        """Never policy: with analytic account → ValidationError on create."""
        with self.assertRaises(ValidationError):
            self._make_move(self.account_never, 100.0, self.analytic_account)

    def test_posted_policy_draft_no_analytic(self):
        """Posted policy: draft state, no analytic → move creates without error."""
        move = self._make_move(self.account_posted, 100.0)
        self.assertTrue(move.id)
        self.assertEqual(move.state, "draft")

    def test_posted_policy_posted_no_analytic_raises(self):
        """Posted policy: posting with no analytic → ValidationError."""
        move = self._make_move(self.account_posted, 100.0)
        with self.assertRaises(ValidationError):
            move.action_post()

    def test_posted_policy_with_analytic_post(self):
        """Posted policy: posting with analytic account → succeeds."""
        move = self._make_move(self.account_posted, 100.0, self.analytic_account)
        move.action_post()
        self.assertEqual(move.state, "posted")

    def test_check_analytic_msg_returns_none_for_optional(self):
        """_check_analytic_required_msg returns None for optional policy."""
        line = self._make_move(self.account_optional, 100.0).line_ids.filtered(
            lambda l: l.account_id == self.account_optional
        )
        self.assertIsNone(line._check_analytic_required_msg())

    def test_has_analytic_distribution_false_without_tags(self):
        """_has_analytic_distribution returns False when no analytic tags."""
        line = self._make_move(self.account_optional, 100.0).line_ids.filtered(
            lambda l: l.account_id == self.account_optional
        )
        self.assertFalse(line._has_analytic_distribution())

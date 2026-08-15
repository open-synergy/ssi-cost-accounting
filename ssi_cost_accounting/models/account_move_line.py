# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, models


class AccountMoveLine(models.Model):
    """
    Enforces the account's analytic policy on journal items.

    Validates that an analytic account is present, absent, or
    required only at posting time, depending on the policy
    configured on ``account.account.property_analytic_policy``.
    """

    _inherit = "account.move.line"

    def _has_analytic_distribution(self):
        """Return whether an analytic tag carries a distribution.

        If the move line has an analytic tag with a distribution,
        ``analytic_account_id`` may legitimately be empty, so the
        policy check must also look at tag-based distributions.

        :return: ``True`` when an active analytic distribution exists
        """
        # If the move line has an analytic tag with distribution, the field
        # analytic_account_id may be empty. So in this case, we do not check it.
        tags_with_analytic_distribution = self.analytic_tag_ids.filtered(
            "active_analytic_distribution"
        )
        return bool(tags_with_analytic_distribution.analytic_distribution_ids)

    def _check_analytic_required_msg(self):
        """Build the analytic policy violation message for this line.

        Compares the account's analytic policy against the
        presence of ``analytic_account_id``/analytic distribution
        on this line and the move's state.

        :return: an error message string, or ``None`` when the
            line already satisfies the account's policy
        """
        self.ensure_one()
        company_cur = self.company_currency_id
        if company_cur.is_zero(self.debit) and company_cur.is_zero(self.credit):
            return None
        analytic_policy = self.account_id._get_analytic_policy()
        if (
            analytic_policy == "always"
            and not self.analytic_account_id
            and not self._has_analytic_distribution()
        ):
            return _(
                "Analytic policy is set to 'Always' with account "
                "'%s' but the analytic account is missing in "
                "the account move line with label '%s'."
            ) % (
                self.account_id.display_name,
                self.name or "",
            )
        elif analytic_policy == "never" and (
            self.analytic_account_id or self._has_analytic_distribution()
        ):
            analytic_account = (
                self.analytic_account_id
                or self.analytic_tag_ids.analytic_distribution_ids[:1]
            )
            return _(
                "Analytic policy is set to 'Never' with account "
                "'%s' but the account move line with label '%s' "
                "has an analytic account '%s'."
            ) % (
                self.account_id.display_name,
                self.name or "",
                analytic_account.display_name,
            )
        elif (
            analytic_policy == "posted"
            and not self.analytic_account_id
            and self.move_id.state == "posted"
            and not self._has_analytic_distribution()
        ):
            return _(
                "Analytic policy is set to 'Posted moves' with "
                "account '%s' but the analytic account is missing "
                "in the account move line with label '%s'."
            ) % (
                self.account_id.display_name,
                self.name or "",
            )
        return None

    @api.constrains("analytic_account_id", "account_id", "debit", "credit")
    def _check_analytic_required(self):
        """Raise ``ValidationError`` when the analytic policy is violated.

        Runs ``_check_analytic_required_msg`` on every line in
        ``self`` and raises on the first violation found.

        :raises ValidationError: when the analytic policy configured
            on the line's account is not satisfied
        """
        for rec in self:
            message = rec._check_analytic_required_msg()
            if message:
                raise exceptions.ValidationError(message)

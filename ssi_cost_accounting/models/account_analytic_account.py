# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.osv import expression


class AccountAnalyticAccount(models.Model):
    """
    Adds a state field to analytic accounts and hides closed
    (``done``) accounts from Many2one search results by default, so
    they no longer show up as selectable options once a project or
    contract has been closed.
    """

    _name = "account.analytic.account"
    _inherit = [
        "account.analytic.account",
        "mixin.date_duration",
    ]
    _order = "group_id, id"

    # Mixin duration attribute
    _date_start_readonly = False
    _date_end_readonly = False
    _date_start_required = False
    _date_end_required = False

    state = fields.Selection(
        string="State",
        required=True,
        selection=[
            ("draft", "Draft"),
            ("open", "In Progress"),
            ("done", "Close"),
        ],
        default="draft",
    )
    child_balance = fields.Monetary(
        string="Child Accounts Balance",
        compute="_compute_child_balance",
        currency_field="currency_id",
        store=False,
        compute_sudo=True,
        readonly=True,
        help=(
            "Sum of the amount of every analytic line posted on all "
            "descendant analytic accounts, excluding this account's "
            "own lines. Computed directly from analytic lines so "
            "the total stays correct at any hierarchy depth."
        ),
    )
    total_balance = fields.Monetary(
        string="Total Balance",
        compute="_compute_total_balance",
        currency_field="currency_id",
        store=False,
        compute_sudo=True,
        readonly=True,
        help=(
            "Sum of the amount of every analytic line posted on "
            "this account and all its descendant analytic accounts. "
            "Computed directly from analytic lines so the total "
            "stays correct at any hierarchy depth."
        ),
    )

    def _get_total_balance_criteria(self):
        """Build the domain selecting lines for ``total_balance``.

        Extension point: override to narrow or widen which
        analytic lines are counted toward this account's total
        balance.

        :return: an Odoo search domain for ``account.analytic.line``
        """
        self.ensure_one()
        return [
            ("account_id", "child_of", self.id),
            ("company_id", "in", [False] + self.env.companies.ids),
        ]

    def _get_child_balance_criteria(self):
        """Build the domain selecting lines for ``child_balance``.

        Extension point: override to narrow or widen which
        analytic lines are counted toward this account's child
        accounts balance.

        :return: an Odoo search domain for ``account.analytic.line``
        """
        self.ensure_one()
        criteria = self._get_total_balance_criteria()
        return criteria + [("account_id", "!=", self.id)]

    def _get_analytic_line_amount_sum(self, criteria):
        """Sum the ``amount`` of analytic lines matching ``criteria``.

        Aggregates with ``read_group`` grouped by ``currency_id``,
        then converts every group to the current company currency.
        Mirrors the pattern used by Odoo core's
        ``_compute_debit_credit_balance`` and its override in
        ``account_analytic_parent``.

        :param criteria: an Odoo search domain for
            ``account.analytic.line``
        :return: the converted total amount, as a float
        """
        self.ensure_one()
        line_obj = self.env["account.analytic.line"]
        currency_obj = self.env["res.currency"]
        company_currency = self.env.company.currency_id
        today = fields.Date.today()
        groups = line_obj.read_group(
            domain=criteria,
            fields=["currency_id", "amount"],
            groupby=["currency_id"],
            lazy=False,
        )
        result = 0.0
        for group in groups:
            group_currency = currency_obj.browse(group["currency_id"][0])
            result += group_currency._convert(
                group["amount"], company_currency, self.env.company, today
            )
        return result

    @api.depends("line_ids.amount", "child_ids.line_ids.amount")
    def _compute_child_balance(self):
        """Compute the sum of descendant accounts' analytic lines.

        :return: nothing; assigns ``child_balance``
        """
        for record in self:
            result = record._get_analytic_line_amount_sum(
                record._get_child_balance_criteria()
            )
            record.child_balance = result

    @api.depends("line_ids.amount", "child_ids.line_ids.amount")
    def _compute_total_balance(self):
        """Compute this account's and its descendants' line sum.

        :return: nothing; assigns ``total_balance``
        """
        for record in self:
            result = record._get_analytic_line_amount_sum(
                record._get_total_balance_criteria()
            )
            record.total_balance = result

    def _name_search(
        self,
        name,
        args=None,
        operator="ilike",
        limit=100,
        name_get_uid=None,
    ):
        """Exclude closed analytic accounts from search results.

        Overridden so every Many2one field pointing to this model
        (across every module) stops offering ``done`` accounts once
        their underlying project/contract is closed, without each
        field needing its own domain. Mirrors the pattern used by
        Odoo core's ``sale_expense`` ``SaleOrder._name_search``:
        overriding ``_name_search`` (not ``_search``) so only
        Many2one autocomplete is affected, leaving ``search()``,
        ``search_read()``, and ``read_group()`` — used by reports,
        cron jobs, and the "Search More..." dialog — untouched.

        Extension point: pass ``include_done_analytic_account`` in
        the context to bypass the exclusion, e.g. for screens that
        must still let users find or reference closed accounts.

        :param name: search string typed by the user
        :param args: additional domain supplied by the caller
        :param operator: comparison operator used for name/code match
        :param limit: maximum number of records to return
        :param name_get_uid: user id used for the ``name_get`` check
        :return: list of ``(id, name)`` tuples matching the search
        """
        args = args or []
        if not self.env.context.get("include_done_analytic_account"):
            args = expression.AND([args, [("state", "!=", "done")]])
        return super()._name_search(
            name,
            args=args,
            operator=operator,
            limit=limit,
            name_get_uid=name_get_uid,
        )

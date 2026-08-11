# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
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

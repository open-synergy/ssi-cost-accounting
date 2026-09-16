# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

import psycopg2

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import mute_logger

_logger = logging.getLogger(__name__)


class MergeAnalyticAccount(models.TransientModel):
    """Wizard that merges several analytic accounts into one.

    The user picks two or more analytic accounts and a destination
    among them. Every reference to a source account — Many2one
    columns, many2many relation tables, ``Reference`` fields, and the
    generic ``res_model``/``res_id`` pattern used by ``mail.message``,
    ``mail.followers``, ``mail.activity``, ``ir.attachment``, and
    ``ir.model.data`` — is rewritten to point at the destination, and
    the source accounts are deleted.

    The tables to rewrite are discovered at runtime from the
    PostgreSQL catalog (``pg_constraint``) instead of being listed by
    hand, so a table introduced by a module installed after this
    wizard was written is still covered. This mirrors Odoo core's
    ``base.partner.merge.automatic.wizard``
    (``odoo/addons/base/wizard/base_partner_merge.py``), adapted for
    ``account.analytic.account``: field values on the destination are
    never overwritten, there is no maximum account count, and there
    is no automatic duplicate-detection screen — the user always
    picks the accounts to merge from the list view.
    """

    _name = "merge_analytic_account"
    _description = "Merge Analytic Accounts"

    @api.model
    def default_get(self, fields_list):
        """Prefill the wizard from the analytic accounts list.

        Only applies when the wizard is opened from the Action menu
        of the ``account.analytic.account`` list view — opening it
        any other way leaves the fields empty.

        :param fields_list: field names requested by the client
        :return: dict of default values
        """
        res = super().default_get(fields_list)
        active_ids = self.env.context.get("active_ids")
        if (
            self.env.context.get("active_model") == "account.analytic.account"
            and active_ids
        ):
            if "analytic_account_ids" in fields_list:
                res["analytic_account_ids"] = [(6, 0, active_ids)]
            if "dst_analytic_account_id" in fields_list:
                accounts = self.env["account.analytic.account"].browse(active_ids)
                res["dst_analytic_account_id"] = self._default_dst_account(accounts).id
        return res

    analytic_account_ids = fields.Many2many(
        string="Analytic Accounts",
        comodel_name="account.analytic.account",
        required=True,
        help=(
            "Analytic accounts to merge. At least two accounts are "
            "required; every record referencing one of them will be "
            "repointed at the destination account below."
        ),
    )
    dst_analytic_account_id = fields.Many2one(
        string="Destination Account",
        comodel_name="account.analytic.account",
        required=True,
        help=(
            "Analytic account the selected accounts are merged into. "
            "It must be one of the accounts listed above; its own "
            "field values are kept as-is."
        ),
    )

    @api.model
    def _default_dst_account(self, accounts):
        """Return the account created first among ``accounts``.

        :param accounts: an ``account.analytic.account`` recordset
        :return: the member of ``accounts`` with the smallest ``id``
        """
        return accounts.sorted(key=lambda account: account.id)[0]

    def action_merge(self):
        """Merge the selected analytic accounts and close the dialog.

        :return: an ``ir.actions.act_window_close`` dict
        """
        for record in self.sudo():
            record._merge()
        return {"type": "ir.actions.act_window_close"}

    def _merge(self):
        """Validate the selection, then merge the source accounts.

        Runs the four sanity checks from the class docstring, then
        rewrites every reference to a source account and deletes the
        sources, in this order: foreign keys, ``Reference``/generic
        fields, chatter log, ``unlink()``.

        :raises UserError: when the selection fails a sanity check
        """
        self.ensure_one()
        self._check_minimum_accounts()
        self._check_destination_in_selection()
        self._check_same_company()
        self._check_no_parent_child_pair()

        dst = self.dst_analytic_account_id
        src = self.analytic_account_ids - dst

        self.flush()
        self._update_foreign_keys(src, dst)
        self._update_reference_fields(src, dst)
        self._log_merge_operation(src, dst)
        src.unlink()

    def _check_minimum_accounts(self):
        """Require at least two accounts to merge.

        :raises UserError: when fewer than two accounts are selected
        """
        if len(self.analytic_account_ids) < 2:
            error_message = """
Context: Merge Analytic Accounts
Database ID: %s
Problem: At least 2 analytic accounts must be selected to merge
Solution: Select 2 or more analytic accounts before merging
""" % (
                self.id,
            )
            raise UserError(_(error_message))

    def _check_destination_in_selection(self):
        """Require the destination to be one of the selected accounts.

        :raises UserError: when the destination is not selected
        """
        if self.dst_analytic_account_id not in self.analytic_account_ids:
            error_message = """
Context: Merge Analytic Accounts
Database ID: %s
Problem: Destination account %s is not part of the selected accounts
Solution: Pick a destination account among the selected ones
""" % (
                self.dst_analytic_account_id.id,
                self.dst_analytic_account_id.display_name,
            )
            raise UserError(_(error_message))

    def _check_same_company(self):
        """Require every selected account to share one company.

        A falsy ``company_id`` (no company) still has to be identical
        across the whole selection: ``mapped()`` would silently merge
        every falsy value into one empty recordset, so a plain
        ``mapped("company_id")`` cannot distinguish "no company" from
        "several companies mixed with no company" — the id (or
        ``False``) of each account is collected into a ``set``
        instead.

        :raises UserError: when the accounts belong to different
            companies
        """
        company_ids = {account.company_id.id for account in self.analytic_account_ids}
        if len(company_ids) > 1:
            error_message = """
Context: Merge Analytic Accounts
Database ID: %s
Problem: Selected analytic accounts belong to different companies
Solution: Select analytic accounts that all belong to the same \
company
""" % (
                self.id,
            )
            raise UserError(_(error_message))

    def _check_no_parent_child_pair(self):
        """Require no parent/child pair among the selected accounts.

        Mirrors ``base_partner_merge.py``'s child/parent check
        (``:308-312``): merging a parent with its own child would
        leave the destination pointing at itself once the child's
        ``parent_id`` is repointed to the destination.

        :raises UserError: when a selected account is an ancestor or
            descendant of another selected account
        """
        Account = self.env["account.analytic.account"]  # noqa: N806
        child_ids = self.env["account.analytic.account"]
        for account in self.analytic_account_ids:
            child_ids |= Account.search([("id", "child_of", account.id)]) - account
        offenders = self.analytic_account_ids & child_ids
        if offenders:
            error_message = """
Context: Merge Analytic Accounts
Database ID: %s
Problem: Selected accounts include a parent and one of its \
descendants
Solution: Remove the parent or the descendant account from the \
selection
""" % (
                offenders.ids,
            )
            raise UserError(_(error_message))

    def _get_fk_on(self, table):
        """Return every Many2one/Many2many relation pointing at *table*.

        Copied from Odoo core's ``base_partner_merge.py`` (`_get_fk_on`,
        ``:80-102``): reads single-column foreign keys from the
        PostgreSQL catalog instead of a hand-written table list, so
        tables added by modules installed after this wizard was
        written are still discovered.

        :param table: name of the SQL table to find relations to
        :return: list of ``(table name, column name)`` tuples
        """
        query = """
            SELECT cl1.relname AS table, att1.attname AS column
            FROM pg_constraint AS con,
                 pg_class AS cl1,
                 pg_class AS cl2,
                 pg_attribute AS att1,
                 pg_attribute AS att2
            WHERE con.conrelid = cl1.oid
                AND con.confrelid = cl2.oid
                AND array_lower(con.conkey, 1) = 1
                AND con.conkey[1] = att1.attnum
                AND att1.attrelid = cl1.oid
                AND cl2.relname = %s
                AND att2.attname = 'id'
                AND array_lower(con.confkey, 1) = 1
                AND con.confkey[1] = att2.attnum
                AND att2.attrelid = cl2.oid
                AND con.contype = 'f'
        """
        self._cr.execute(query, (table,))
        return self._cr.fetchall()

    def _update_foreign_keys(self, src_accounts, dst_account):
        """Repoint every foreign key from ``src_accounts`` to ``dst_account``.

        Mirrors ``base_partner_merge.py`` (`_update_foreign_keys`,
        ``:104-179``): for each ``(table, column)`` pair found by
        :meth:`_get_fk_on`, runs a bulk ``UPDATE`` inside a savepoint;
        a unique-constraint violation (typical of many2many relation
        tables that already contain the destination) is caught and
        turned into a ``DELETE`` of the source rows instead. Tables
        belonging to this wizard itself (its own table and its
        many2many relation table for ``analytic_account_ids``) are
        skipped, mirroring the ``base_partner_merge_`` exception at
        ``:118`` — a substring check on ``self._table``, not a
        prefix check: Odoo names an implicit many2many relation table
        from the two tables sorted alphabetically
        (``models.py``, ``Many2many._setup_regular_base``), so this
        wizard's relation table is
        ``account_analytic_account_merge_analytic_account_rel`` —
        ``self._table`` appears in the middle of that name, not at
        its start.

        :param src_accounts: ``account.analytic.account`` recordset
            of the accounts being merged away (destination excluded)
        :param dst_account: destination ``account.analytic.account``
            record
        """
        _logger.debug(
            "_update_foreign_keys for dst_account: %s, src_accounts: %s",
            dst_account.id,
            src_accounts.ids,
        )
        relations = self._get_fk_on("account_analytic_account")

        for table, column in relations:
            if self._table in table:
                continue

            query = (
                'UPDATE "%(table)s" SET "%(column)s" = %%s ' 'WHERE "%(column)s" IN %%s'
            ) % {"table": table, "column": column}
            try:
                with mute_logger("odoo.sql_db"), self._cr.savepoint():
                    self._cr.execute(query, (dst_account.id, tuple(src_accounts.ids)))
            except psycopg2.Error:
                # Updating failed, most likely because of a unique
                # constraint (e.g. a many2many relation table that
                # already links the destination). Rows referencing a
                # merged-away account are useless; delete them.
                delete_query = ('DELETE FROM "%(table)s" WHERE "%(column)s" IN %%s') % {
                    "table": table,
                    "column": column,
                }
                self._cr.execute(delete_query, (tuple(src_accounts.ids),))

        self.invalidate_cache()
        analytic_account = self.env["account.analytic.account"]
        if analytic_account._parent_store:
            analytic_account._parent_store_compute()

    def _update_reference_fields(self, src_accounts, dst_account):
        """Repoint generic and ``Reference`` fields to ``dst_account``.

        Mirrors ``base_partner_merge.py`` (`_update_reference_fields`,
        ``:181-231``): rewrites the generic ``res_model``/``res_id``
        pattern used by ``mail.message``, ``mail.followers``,
        ``mail.activity``, ``ir.attachment``, and ``ir.model.data``,
        then every non-abstract, non-computed ``ir.model.fields``
        record of type ``reference`` whose value points at a source
        account.

        :param src_accounts: ``account.analytic.account`` recordset
            of the accounts being merged away (destination excluded)
        :param dst_account: destination ``account.analytic.account``
            record
        """
        _logger.debug(
            "_update_reference_fields for dst_account: %s, src_accounts: %r",
            dst_account.id,
            src_accounts.ids,
        )

        def update_records(model, src, field_model="model", field_id="res_id"):
            """Repoint one generic model's rows from ``src`` to dst.

            :param model: name of the model holding the generic
                reference (e.g. ``mail.message``)
            :param src: source ``account.analytic.account`` record
            :param field_model: field storing the target model name
            :param field_id: field storing the target record id
            """
            Model = self.env[model] if model in self.env else None  # noqa: N806
            if Model is None:
                return
            records = Model.sudo().search(
                [
                    (field_model, "=", "account.analytic.account"),
                    (field_id, "=", src.id),
                ]
            )
            try:
                with mute_logger("odoo.sql_db"), self._cr.savepoint():
                    records.sudo().write({field_id: dst_account.id})
                    records.flush()
            except psycopg2.Error:
                records.sudo().unlink()

        for src in src_accounts:
            update_records("ir.attachment", src, field_model="res_model")
            update_records("mail.followers", src, field_model="res_model")
            update_records("mail.activity", src, field_model="res_model")
            update_records("mail.message", src)
            update_records("ir.model.data", src)

        reference_fields = self.env["ir.model.fields"].search(
            [("ttype", "=", "reference")]
        )
        for reference_field in reference_fields.sudo():
            try:
                Model = self.env[reference_field.model]  # noqa: N806
                field = Model._fields[reference_field.name]
            except KeyError:
                continue

            if Model._abstract or field.compute is not None:
                continue

            for src in src_accounts:
                records_ref = Model.sudo().search(
                    [
                        (
                            reference_field.name,
                            "=",
                            "account.analytic.account,%d" % src.id,
                        )
                    ]
                )
                records_ref.sudo().write(
                    {
                        reference_field.name: (
                            "account.analytic.account,%d" % dst_account.id
                        )
                    }
                )

        self.flush()

    def _log_merge_operation(self, src_accounts, dst_account):
        """Post a chatter message on ``dst_account`` about the merge.

        :param src_accounts: ``account.analytic.account`` recordset
            of the accounts that were merged away
        :param dst_account: destination ``account.analytic.account``
            record
        """
        names = ", ".join(
            "%s [%s]" % (account.name, account.code or "-") for account in src_accounts
        )
        dst_account.message_post(body=_("Merged analytic account(s): %s") % names)
        _logger.info(
            "(uid = %s) merged analytic accounts %r into %s",
            self._uid,
            src_accounts.ids,
            dst_account.id,
        )

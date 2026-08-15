# Create Analytic Account

> **Module:** ssi_cost_accounting
>
> **Extends:** Odoo core (`analytic` module) — model `account.analytic.account`, action
> `01-create`

## Additional Pre-Condition

- **Access:** The user is a member of the **Analytic Account** group
  (`ssi_cost_accounting.account_analytic_account_configurator_group`) — this is the
  group guarding the **Cost Accounting > Account > Accounts** menu used to reach the
  create form.

## Additional Fields

When this module is installed, the create form and list gain the following fields, shown
after the **Partner** field:

- **Start Date**: The date the analytic account becomes effective. Optional.
- **End Date**: The date the analytic account stops being effective. Optional.
- **State**: Shown as a clickable status bar on the form (and as a plain column on the
  list). One of **Draft**, **In Progress**, **Close**. Defaults to **Draft**. Since the
  status bar is clickable, the user can change it directly from the form without a
  dedicated confirm/approve button.

## Additional Post-Condition

- Once **State** is set to **Close**, the analytic account no longer appears in the
  autocomplete suggestions of Many2one fields that point to `account.analytic.account`
  anywhere in the system (e.g. the **Analytic Account** field on a journal item). It
  remains visible in the Analytic Accounts list itself and in reports/searches — only
  the Many2one autocomplete is filtered.

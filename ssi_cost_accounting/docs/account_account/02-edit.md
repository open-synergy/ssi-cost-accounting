# Edit Account

> **Module:** ssi_cost_accounting
>
> **Extends:** Odoo core (`account` module) — model `account.account`, action `02-edit`

## Additional Pre-Condition

- **Access:** The user is a member of the **Analytic Accounting** group
  (`analytic.group_analytic_accounting`). Without this group the Analytic Policy field
  described below is not rendered on the list or the form — there is no error message,
  the field simply does not appear.

## Additional Fields

When this module is installed, the account list and form gain one field, shown only to
users in the **Analytic Accounting** group (`analytic.group_analytic_accounting`):

- **Analytic Policy**: Controls whether an analytic account is optional, always
  required, required only once a journal entry is posted, or forbidden on journal items
  that use this account. One of **Optional**, **Always**, **Posted moves**, **Never**.
  Defaults to **Optional**. This field is company dependent — the value applies to the
  current company only.

## Additional Post-Condition

- Once saved, every `account.move.line` created or posted against this account is
  checked against the selected policy. Saving a journal entry that violates the policy
  raises a validation error — see the journal entry Create/Post flow.

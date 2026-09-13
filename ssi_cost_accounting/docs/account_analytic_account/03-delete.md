# Delete Analytic Account

> **Module:** `ssi_cost_accounting`\
> **Model:** `account.analytic.account`\
> **Menu:** Cost Accounting > Configuration > Account > Accounts\
> **Actor:** user in group _Analytic Account_\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** No `account.analytic.line` and no `account.analytic.distribution` row
  references this account — otherwise the deletion is rejected (see the error message
  below).
- **Record:** Deleting an account also permanently deletes every child analytic account
  nested under it via **Parent Analytic Account** — children are removed automatically
  together with their parent, without a separate warning.
- **Access:** User is in group _Analytic Account_
  (`ssi_cost_accounting.account_analytic_account_configurator_group`).

## Flow

1. Open the **Cost Accounting > Configuration > Account > Accounts** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm ("Are you sure you want to delete this record?").

## Post-Condition

- If none of the selected accounts (nor their descendants) is referenced by an analytic
  line or an analytic distribution, they are permanently removed from the system,
  together with any child analytic accounts nested under them.
- If a selected account is still referenced, the operation is rejected with a validation
  error beginning "The operation cannot be completed: another model requires the record
  being deleted. If possible, archive it instead." — the record is not deleted.

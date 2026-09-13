# Edit Analytic Account

> **Module:** `ssi_cost_accounting`\
> **Model:** `account.analytic.account`\
> **Menu:** Cost Accounting > Configuration > Account > Accounts\
> **Actor:** user in group _Analytic Account_\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** None specific — the fields below can be changed regardless of the current
  **State**.
- **Access:** User is in group _Analytic Account_
  (`ssi_cost_accounting.account_analytic_account_configurator_group`).

## Flow

1. Open the **Cost Accounting > Configuration > Account > Accounts** menu.
2. Find and open the record to edit.
3. Change any of the editable fields (**Name**, **Reference**, **Customer**, **Start
   Date**, **End Date**, **Group**, **Parent Analytic Account**).
4. To change the **State**, click directly on the desired bubble (**Draft**, **In
   Progress**, or **Close**) on the status bar in the header. The status bar is
   clickable in both directions — there is no dedicated confirm/approve button and no
   confirmation dialog.
5. Click **Save**.

## Post-Condition

- The record is updated with the new values.
- Once **State** is set to **Close**, the analytic account no longer appears in the
  autocomplete suggestions of Many2one fields that point to `account.analytic.account`
  anywhere in the system (e.g. the **Analytic Account** field on a journal item). It
  remains visible in the Analytic Accounts list itself and in reports/searches — only
  the Many2one autocomplete is filtered.

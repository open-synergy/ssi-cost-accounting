# Create Analytic Account

> **Module:** `ssi_cost_accounting`\
> **Model:** `account.analytic.account`\
> **Menu:** Cost Accounting > Configuration > Account > Accounts\
> **Actor:** user in group _Analytic Account_\
> **State:** `—` → `draft`

## Pre-Condition

- **Access:** User is in group _Analytic Account_
  (`ssi_cost_accounting.account_analytic_account_configurator_group`).

## Flow

1. Open the **Cost Accounting > Configuration > Account > Accounts** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Name** _(required)_: enter a name for the analytic account (e.g. "Project XYZ").
   - **Reference**: an internal code for the account. Optional.
   - **Customer**: link a partner to this account. Optional.
   - **Start Date**: the date the analytic account becomes effective. Optional.
   - **End Date**: the date the analytic account stops being effective. Optional.
   - **Group**: classify the account under an Analytic Account Group. Optional.
   - **Parent Analytic Account**: nest this account under another analytic account to
     build a hierarchy. Optional. Selecting one also re-fills **Customer** above from
     the parent's **Customer**, if the parent has one. Change if needed.
4. On the header, note that the **State** status bar shows **Draft** — the default state
   for a new record.
5. In the **Hierarchy Balance** group, **Child Accounts Balance** and **Total Balance**
   are shown read-only; both are automatically computed from posted analytic lines and
   remain **0.00** until such lines exist.
6. Click **Save**.

## Post-Condition

- A new record is created with **State** set to **Draft**.
- **Child Accounts Balance** and **Total Balance** reflect the sum of the amount of
  every analytic line posted on this account and, once any exist, its descendant
  accounts.

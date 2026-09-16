# Merge Analytic Accounts

> **Module:** `ssi_cost_accounting`\
> **Model:** `account.analytic.account`\
> **Menu:** Cost Accounting > Configuration > Account > Accounts\
> **Actor:** user in group _Analytic Account_\
> **Requires:** `01-create`

## Pre-Condition

- **Access:** User is in group _Analytic Account_
  (`ssi_cost_accounting.account_analytic_account_configurator_group`).
- **Record:** At least 2 analytic accounts exist, to select from the list.
- **Record:** The selected accounts all belong to the same company, or all have no
  company set.
- **Record:** None of the selected accounts is the parent or the child of another
  selected account.

## Flow

1. Open the **Cost Accounting > Configuration > Account > Accounts** menu.
2. Select two or more records to merge (check the checkbox on each row).
3. Click **Action** > **Merge Analytic Accounts**.
4. In the wizard that appears:
   - **Analytic Accounts**: pre-filled with the accounts selected in step 2.
   - **Destination Account**: pre-filled with the account created first among the
     selection. Change if needed — it must be one of the selected accounts.
5. Click **Merge**.

## Post-Condition

- Every record that referenced one of the merged-away accounts — analytic lines, journal
  items, chatter messages, followers, and any other reference in the system — now points
  at the destination account instead.
- The merged-away accounts no longer appear in the list; they are permanently deleted.
- The destination account's chatter shows one message listing the name and code of each
  account that was merged into it.
- Field values on the destination account are unchanged.

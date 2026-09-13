# Delete Analytic Tag

> **Module:** `ssi_cost_accounting`\
> **Model:** `account.analytic.tag`\
> **Menu:** Cost Accounting > Configuration > Account > Tags\
> **Actor:** user in group _Analytic Tag_\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** No `account.analytic.distribution` row references this tag — including its
  own **Analytic Distribution** lines, if any were added while **Analytic Distribution**
  was checked. Otherwise the deletion is rejected (see the error message below).
- **Access:** User is in group _Analytic Tag_
  (`ssi_cost_accounting.account_analytic_tag_configurator_group`).

## Flow

1. Open the **Cost Accounting > Configuration > Account > Tags** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm ("Are you sure you want to delete this record?").

## Post-Condition

- If none of the selected tags is referenced by an analytic distribution row, they are
  permanently removed from the system.
- If a selected tag is still referenced, the operation is rejected with a validation
  error beginning "The operation cannot be completed: another model requires the record
  being deleted. If possible, archive it instead." — the record is not deleted.

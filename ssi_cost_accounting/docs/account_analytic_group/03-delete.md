# Delete Analytic Account Group

> **Module:** `ssi_cost_accounting`\
> **Model:** `account.analytic.group`\
> **Menu:** Cost Accounting > Configuration > Account > Groups\
> **Actor:** user in group _Analytic Account Group_\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Deleting a group also permanently deletes every child group nested under
  it via **Parent** — children are removed automatically together with their parent,
  without a separate warning.
- **Record:** Any analytic account still assigned to this group (or to one of its
  deleted children) simply loses that **Group** assignment — deletion of the group is
  not blocked by this.
- **Access:** User is in group _Analytic Account Group_
  (`ssi_cost_accounting.account_analytic_group_configurator_group`).

## Flow

1. Open the **Cost Accounting > Configuration > Account > Groups** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm ("Are you sure you want to delete this record?").

## Post-Condition

- The selected records, together with any child groups nested under them, are
  permanently removed from the system.
- Analytic accounts that referenced a deleted group no longer show a value in their
  **Group** field.

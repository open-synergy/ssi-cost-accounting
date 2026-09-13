# Create Analytic Account Group

> **Module:** `ssi_cost_accounting`\
> **Model:** `account.analytic.group`\
> **Menu:** Cost Accounting > Configuration > Account > Groups\
> **Actor:** user in group _Analytic Account Group_

## Pre-Condition

- **Access:** User is in group _Analytic Account Group_
  (`ssi_cost_accounting.account_analytic_group_configurator_group`).

## Flow

1. Open the **Cost Accounting > Configuration > Account > Groups** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Name** _(required)_: enter a name for the analytic account group.
   - **Parent**: nest this group under another analytic account group to build a
     hierarchy. Optional.
   - **Sequence**: determines the display order of analytic groups relative to each
     other. Defaults to **10**. Can also be reordered directly from the list using the
     drag handle in front of each row, without opening the record.
   - **Description**: free text describing the group. Optional.
4. Click **Save**.

## Post-Condition

- A new record is created and appears in the Analytic Account Groups list, ordered
  according to its **Sequence**.

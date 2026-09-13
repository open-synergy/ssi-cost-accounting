# Create Analytic Tag

> **Module:** `ssi_cost_accounting`\
> **Model:** `account.analytic.tag`\
> **Menu:** Cost Accounting > Configuration > Account > Tags\
> **Actor:** user in group _Analytic Tag_

## Pre-Condition

- **Access:** User is in group _Analytic Tag_
  (`ssi_cost_accounting.account_analytic_tag_configurator_group`).

## Flow

1. Open the **Cost Accounting > Configuration > Account > Tags** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Analytic Tag** _(required)_: enter a name for the tag.
   - **Analytic Distribution**: check to distribute analytic lines carrying this tag
     across several analytic accounts by percentage. Optional; only visible to users in
     group `analytic.group_analytic_accounting`.
   - **Company**: the company this tag belongs to. Optional; only visible with multiple
     companies.
4. If **Analytic Distribution** is checked, an **Analytic Distribution** table appears.
   Repeat the following steps as many times as needed:
   - Click **Add a line**.
   - Fill in each line with:
     - **Analytic Account** _(required)_: the account to distribute to.
     - **Percentage** _(required)_: the share of the amount for this account, between
       **0** and **100**. Defaults to **100**.
5. Click **Save**.

## Post-Condition

- A new record is created and appears in the Analytic Tags list.

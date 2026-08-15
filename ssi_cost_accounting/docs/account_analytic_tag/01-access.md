# Access Analytic Tags

> **Module:** `ssi_cost_accounting`\
> **Model:** `account.analytic.tag`\
> **Menu:** Cost Accounting > Account > Tags\
> **Actor:** user in group `Analytic Tag` (`ssi_cost_accounting.account_analytic_tag_configurator_group`)

This module does not add any field or behavior to `account.analytic.tag` itself — it
only adds a shortcut menu so Analytic Tags can be managed from the Cost Accounting app,
without navigating to Invoicing/Accounting configuration.

## Pre-Condition

- **Access:** User is in group `Analytic Tag`
  (`ssi_cost_accounting.account_analytic_tag_configurator_group`). Without this group
  the **Tags** menu item is not visible.

## Flow

1. Open the menu **Cost Accounting > Account > Tags**.
2. The standard Analytic Tags list view opens, showing every existing
   `account.analytic.tag` record. From here the user can create, edit, or delete tags
   using the standard Odoo list/form — this module does not change that behavior.

## Post-Condition

- The Analytic Tags list view is displayed, listing the existing analytic tags for
  selection or management.

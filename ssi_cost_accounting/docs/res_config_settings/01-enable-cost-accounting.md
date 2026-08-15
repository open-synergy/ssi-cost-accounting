# Enable Cost Accounting Settings

> **Module:** `ssi_cost_accounting`\
> **Model:** `res.config.settings`\
> **Menu:** Cost Accounting > Configuration > Settings\
> **Actor:** user in group `Settings` (`base.group_system`)

This module adds a **Cost Accounting** section to the General Settings screen with two
optional module installer toggles. It does not add any field to the model beyond these
two toggles.

## Pre-Condition

- **Access:** User is in group `Settings` (`base.group_system`).

## Flow

1. Open the menu **Cost Accounting > Configuration > Settings**.
2. The General Settings screen opens, scrolled to the **Cost Accounting** section.
3. Check **Financial Budget** to enable the optional Financial Budget module. Unchecked
   by default.
4. Check **Analytic Budget** to enable the optional Analytic Budget module. Unchecked by
   default.
5. Click **Save**.

## Post-Condition

- The settings are saved. For any toggle that was turned on, the corresponding module
  (`ssi_financial_budget` / `ssi_analytic_budget`) begins installing; Odoo reloads the
  page once installation completes.

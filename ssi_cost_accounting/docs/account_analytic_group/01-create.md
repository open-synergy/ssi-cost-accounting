# Create Analytic Account Group

> **Module:** ssi_cost_accounting
>
> **Extends:** Odoo core/OCA (`analytic` / `account_analytic_parent`) — model
> `account.analytic.group`, action `01-create`

## Additional Pre-Condition

- **Access:** The user is a member of the **Analytic Account Group** group
  (`ssi_cost_accounting.account_analytic_group_configurator_group`) — this is the group
  guarding the **Cost Accounting > Account > Groups** menu used to reach the create
  form.

## Additional Fields

When this module is installed, the create form gains one field, shown after the
**Parent** field:

- **Sequence**: Determines the display order of analytic groups relative to each other.
  Defaults to **10**. Editable on the form; can also be reordered directly from the list
  using the drag handle in front of each row (no need to open the record).

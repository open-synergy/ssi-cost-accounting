odoo.define("ssi_cost_accounting.account_analytic_tag_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/account_analytic_tag/01-access.md
    tour.register(
        "ssi_cost_accounting_account_analytic_tag_access",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Flow 1 — Open the Cost Accounting > Account > Tags menu
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Cost Accounting app",
                trigger:
                    '.o_app[data-menu-xmlid="ssi_cost_accounting.menu_root_cost_accounting"]',
            },
            {
                content: "Open the Configuration menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_cost_accounting.menu_cost_accounting_configuration"]',
            },
            {
                // "Account" (menu_account_configuration) is a grouping
                // header with children — it has no data-menu-xmlid and
                // cannot be clicked. Go straight to the "Tags" leaf.
                content: "Open the Tags menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_cost_accounting.account_analytic_tag_menu"]',
            },

            // ── Post-Condition — the Analytic Tags list view is displayed
            {
                content: "Analytic Tags list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Tag)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );
});

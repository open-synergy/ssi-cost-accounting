odoo.define("ssi_cost_accounting.account_account_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/account_account/02-edit.md
    tour.register(
        "ssi_cost_accounting_account_account_edit",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Flow 1 — Open the Financial Accounting > Configuration >
            //             Account > Accounts menu
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Financial Accounting app",
                trigger:
                    '.o_app[data-menu-xmlid="ssi_financial_accounting.menu_root_financial_accounting"]',
            },
            {
                content: "Open the Configuration menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_financial_accounting.menu_financial_accounting_configuration"]',
            },
            {
                // "Account" (menu_account_configuration) is a grouping
                // header with children — it has no data-menu-xmlid and
                // cannot be clicked. Go straight to the "Accounts" leaf.
                content: "Open the Accounts menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_financial_accounting.account_account_menu"]',
            },
            {
                // Gerbang: tunggu action TUJUAN benar-benar terpasang.
                content: "Accounts list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Accounts)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },

            // ── Flow 2 — Find and open the record to edit
            {
                content: "Open the test account",
                trigger: '.o_list_view .o_data_row:contains("CATOUR01")',
                extra_trigger: ".o_list_view",
            },

            // ── Additional Fields — Analytic Policy field is displayed
            {
                content: "Analytic Policy field is displayed",
                trigger: ".o_field_widget[name='property_analytic_policy']",
                extra_trigger: ".o_form_view",
                run: function () {
                    // Assertion only — this delta tour only proves the
                    // field is rendered, per the E1 pattern. It does not
                    // continue into a value change / save flow.
                },
            },
        ]
    );
});

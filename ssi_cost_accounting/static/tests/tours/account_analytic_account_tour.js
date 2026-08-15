odoo.define("ssi_cost_accounting.account_analytic_account_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/account_analytic_account/01-create.md
    tour.register(
        "ssi_cost_accounting_account_analytic_account_create",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Flow 1 — Open the Cost Accounting > Account > Accounts menu
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
                // cannot be clicked. Go straight to the "Accounts" leaf.
                content: "Open the Accounts menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_cost_accounting.account_analytic_account_menu"]',
            },
            {
                // Gerbang: tunggu action TUJUAN benar-benar terpasang.
                content: "Analytic Accounts list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Analytic Account)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },

            // ── Flow 2 — Click the New button
            {
                content: "Click Create",
                trigger: ".o_list_button_add",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open in edit mode",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },

            // ── Additional Fields — Start Date / End Date are displayed
            {
                content: "Start Date field is displayed",
                trigger: ".o_field_widget[name='date_start']",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "End Date field is displayed",
                trigger: ".o_field_widget[name='date_end']",
                run: function () {
                    // Assertion only.
                },
            },

            // ── Additional Fields — State status bar defaults to Draft
            {
                content: "State status bar shows Draft",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                run: function () {
                    // Assertion only — this delta tour only proves the
                    // additional fields are rendered, per the E1 pattern.
                    // It does not continue into save/state-change flow.
                },
            },
        ]
    );
});

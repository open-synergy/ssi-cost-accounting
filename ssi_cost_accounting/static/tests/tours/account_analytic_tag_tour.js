odoo.define("ssi_cost_accounting.account_analytic_tag_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/account_analytic_tag/01-create.md
    tour.register(
        "ssi_cost_accounting_account_analytic_tag_create",
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
            {
                // Gerbang: tunggu action TUJUAN benar-benar terpasang.
                content: "Analytic Tags list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Tag)",
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

            // ── Flow 3 — Fill in the required Analytic Tag field
            {
                content: "Fill in Analytic Tag",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text Tour Test Analytic Tag",
            },

            // ── Flow 3 — Analytic Distribution checkbox is displayed
            {
                content: "Analytic Distribution field is displayed",
                trigger: ".o_field_widget[name='active_analytic_distribution']",
                run: function () {
                    // Assertion only. Checking it and exercising the
                    // resulting one2many table is left untested here —
                    // per odoo-development-ui-test, a tour only proves
                    // the interface is usable, not every value/branch.
                },
            },

            // ── Flow 5 — Click Save
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );
});

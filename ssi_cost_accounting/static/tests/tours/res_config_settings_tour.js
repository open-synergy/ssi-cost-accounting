odoo.define("ssi_cost_accounting.res_config_settings_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/res_config_settings/01-enable-cost-accounting.md
    //
    // This tour stops at asserting the Cost Accounting settings section and
    // its two toggles are displayed and enabled. It does NOT check either
    // toggle and click Save: doing so triggers a real module installation
    // (ssi_financial_budget / ssi_analytic_budget), which has no reliable
    // DOM "finished" signal for web_tour to wait on and would leave the
    // test database permanently mutated for every run after it. Enabling
    // the module and saving is out of scope for this tour, same as any
    // other irreversible/heavy side-effecting action (see patterns.md §Q).
    tour.register(
        "ssi_cost_accounting_res_config_settings_enable_cost_accounting",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Flow 1 — Open the Cost Accounting > Configuration > Settings
            //             menu
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
                content: "Open the Settings menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_cost_accounting.res_config_settings_menu"]',
            },

            // ── Flow 2/3/4/5 — The General Settings screen opens, scrolled
            //                  to the Cost Accounting section; the two
            //                  toggles are displayed and enabled
            {
                content: "Cost Accounting settings section is displayed",
                trigger: ".app_settings_block[data-key='ssi_cost_accounting']",
                extra_trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Financial Budget toggle is displayed and enabled",
                trigger:
                    ".o_field_widget[name='module_ssi_financial_budget'] input:enabled",
                run: function () {
                    // Assertion only — see the note above `tour.register`
                    // for why this tour stops here instead of toggling
                    // and saving.
                },
            },
            {
                content: "Analytic Budget toggle is displayed and enabled",
                trigger:
                    ".o_field_widget[name='module_ssi_analytic_budget'] input:enabled",
                run: function () {
                    // Assertion only — see the note above `tour.register`.
                },
            },
        ]
    );
});

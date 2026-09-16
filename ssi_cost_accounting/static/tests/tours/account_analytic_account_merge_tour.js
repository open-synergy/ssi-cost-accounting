odoo.define("ssi_cost_accounting.account_analytic_account_merge_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/account_analytic_account/04-merge.md
    //
    // Fixture note: "Merge Tour Keep" is created FIRST in setUpClass and
    // "Merge Tour Remove" second, so the wizard's default destination
    // (account created first — see merge_analytic_account.py
    // ``_default_dst_account``) lands on "Merge Tour Keep" without any
    // extra step, matching the IK Flow that never changes it.
    tour.register(
        "ssi_cost_accounting_account_analytic_account_merge",
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

            // ── Flow 2 — Select the accounts to merge
            {
                content: "Select the Merge Tour Keep account",
                trigger:
                    ".o_data_row:contains(Merge Tour Keep) " +
                    ".o_list_record_selector input[type='checkbox']",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Select the Merge Tour Remove account",
                trigger:
                    ".o_data_row:contains(Merge Tour Remove) " +
                    ".o_list_record_selector input[type='checkbox']",
            },

            // ── Flow 3 — Open the Merge Analytic Accounts wizard
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },
            {
                content: "Click Merge Analytic Accounts",
                // Action menu items are Owl components; match the label
                // EXACTLY so a substring like "Archive" is never picked
                // instead — see patterns-dialogs-and-wizards.md §I.
                trigger: ".o_cp_action_menus .o_menu_item a",
                run: function () {
                    var $item = $(".o_cp_action_menus .o_menu_item a").filter(
                        function () {
                            return $(this).text().trim() === "Merge Analytic Accounts";
                        }
                    );
                    $item[0].click();
                },
            },

            // ── Flow 4 — The wizard is open, both fields pre-filled
            //
            // 14.0: NEVER prefix these triggers with `.modal` — the
            // trigger is already searched INSIDE the modal, so a
            // `.modal` prefix demands a modal nested inside the
            // modal, which does not exist: it matches nothing and
            // times out with a symptom that reads like "dialog never
            // opened" (patterns.md §H). Unlike the cancel-reason
            // wizard opened from a document FORM (where a background
            // `.o_form_view` already exists and this note applies),
            // this wizard opens from the Accounts LIST view, so
            // `.o_form_view` alone can only match the dialog's own
            // form.
            {
                content: "The merge wizard is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
            {
                // Many2many_tags always renders its tags as text nodes
                // (unlike a many2one input, whose label lives in the
                // DOM `value` attribute, not as text — patterns-fields.md
                // "tidak cocok pada baris yang masih .o_selected_row").
                content: "Analytic Accounts is pre-filled with both records",
                trigger:
                    ".o_field_widget[name='analytic_account_ids']" +
                    ":contains(Merge Tour Keep)" +
                    ":contains(Merge Tour Remove)",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Destination Account field is displayed",
                trigger: ".o_field_widget[name='dst_analytic_account_id']",
                run: function () {
                    // Assertion only.
                },
            },

            // ── Flow 5 — Click Merge
            {
                content: "Click the Merge button",
                trigger: ".modal-footer button[name='action_merge']",
            },

            // ── Post-Condition — dialog closed, source account is gone
            {
                content: "The wizard dialog is closed",
                trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "The removed account no longer appears in the list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(Merge Tour Remove)))",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "The kept account still appears in the list",
                trigger: ".o_data_row:contains(Merge Tour Keep)",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );
});

# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Cost Accounting",
    "version": "14.0.2.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "ssi_financial_accounting",
        "ssi_duration_mixin",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "menu.xml",
        "views/res_config_settings_views.xml",
        "views/account_analytic_account_views.xml",
        "views/account_analytic_group_views.xml",
        "views/account_analytic_tag_views.xml",
    ],
    "demo": [],
}

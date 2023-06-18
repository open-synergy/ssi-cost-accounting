# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Cost Accounting",
    "version": "14.0.1.3.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "ssi_financial_accounting",
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

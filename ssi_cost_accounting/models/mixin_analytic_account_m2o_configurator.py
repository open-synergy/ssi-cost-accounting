# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class MixinAnalyticAccountM2oConfigurator(models.AbstractModel):
    """
    Reusable Many2one configurator mixin for analytic accounts.

    Lets a transactional model restrict the analytic accounts a
    user may pick — via manual selection, a search domain, or a
    Python code snippet — and injects the configuration fields into
    the model's form view.
    """

    _name = "mixin.analytic_account_m2o_configurator"
    _inherit = [
        "mixin.decorator",
    ]
    _description = "account.analytic.account Many2one Configurator Mixin"

    _analytic_account_m2o_configurator_insert_form_element_ok = False
    _analytic_account_m2o_configurator_form_xpath = False

    analytic_account_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="Analytic Account Selection Method",
        required=True,
    )
    analytic_account_ids = fields.Many2many(
        comodel_name="account.analytic.account",
        string="Analytic Accounts",
        relation="rel_m2o_mixin_2_analytic_account",
    )
    analytic_account_domain = fields.Text(
        default="[]", string="Analytic Account Domain"
    )
    analytic_account_python_code = fields.Text(
        default="result = []", string="Analytic Account Python Code"
    )

    @ssi_decorator.insert_on_form_view()
    def _analytic_account_m2o_configurator_insert_form_element(self, view_arch):
        """Insert the analytic account configurator fields into the form.

        Runs on every model mixing this in, controlled by
        ``_analytic_account_m2o_configurator_insert_form_element_ok``
        and ``_analytic_account_m2o_configurator_form_xpath``.

        :param view_arch: the form view architecture being built
        :return: the (possibly modified) view architecture
        """
        # TODO
        template_xml = "ssi_cost_accounting."
        template_xml += "analytic_account_m2o_configurator_template"
        if self._analytic_account_m2o_configurator_insert_form_element_ok:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id=template_xml,
                xpath=self._analytic_account_m2o_configurator_form_xpath,
                position="inside",
            )
        return view_arch

# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiResConfigSettings(HttpSavepointCase):
    """Tour tests for the ``res.config.settings`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Prepare the admin session for the settings tour.

        No extra fixture is required: ``base.user_admin`` is a member
        of the *Settings* group (``base.group_system``) by default.
        """
        super().setUpClass()

    def test_enable_cost_accounting(self):
        """Run the settings tour for ``res.config.settings``.

        IK: docs/res_config_settings/01-enable-cost-accounting.md
        """
        self.start_tour(
            "/web",
            "ssi_cost_accounting_res_config_settings_enable_cost_accounting",
            login="admin",
        )

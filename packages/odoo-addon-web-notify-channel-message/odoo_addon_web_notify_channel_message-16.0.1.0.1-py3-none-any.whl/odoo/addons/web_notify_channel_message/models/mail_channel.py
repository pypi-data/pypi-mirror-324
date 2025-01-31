# pylint: disable=missing-docstring
# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models


class MailChannel(models.Model):
    _inherit = "mail.channel"

    def _notify_message(self, message):
        for partner in self.channel_partner_ids:
            users = partner.user_ids
            for user in users:
                if user in message.author_id.user_ids:
                    continue
                user.notify_info(
                    message=_("You have a new message in channel %s") % self.name
                )

    def message_post(self, *, message_type="notification", **kwargs):
        message = super().message_post(message_type=message_type, **kwargs)
        self._notify_message(message)
        return message

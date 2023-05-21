"""Adds config flow for Blueprint."""
from __future__ import annotations

from homeassistant import config_entries

from .const import DOMAIN


class AstromechFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Blueprint."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        # Check if already configured
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            return self.async_create_entry(title="Astromech", data=user_input)

        return self.async_show_form(step_id="user")

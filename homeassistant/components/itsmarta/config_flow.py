"""Config flow for MARTA integration."""
from __future__ import annotations

# from email.policy import default  # pylint:disable=unused-import
import logging

# from tkinter import E
from typing import Any
from uuid import UUID

import voluptuous as vol

from homeassistant import config_entries, exceptions
from homeassistant.const import CONF_API_KEY
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import AbortFlow

from .const import (
    CONFIG_BREEZE_CARD,
    DEFAULT_NAME,
    DOMAIN,
    TEST_API_KEY,
    TEST_BREEZE_CARD,
)
from .marta.api import MARTA
from .marta.exceptions import APIKeyError

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY, default=TEST_API_KEY): str,
        vol.Optional(CONFIG_BREEZE_CARD, default=TEST_BREEZE_CARD): str,
    }
)


def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.

     Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}

     Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.
    """

    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    data has the keys from DATA_SCHEMA with values provided by the user.
    """

    # Validate the data and test a connection.
    if not is_valid_uuid(data[CONF_API_KEY]):
        raise InvalidAPI

    if len(data[CONFIG_BREEZE_CARD]) != 20:
        raise InvalidBreeze

    # If your PyPI package is not built with async, pass your methods
    # to the executor:
    # await hass.async_add_executor_job(
    #     your_validate_func, data["username"], data["password"]
    # ) no Py
    client = MARTA(data[CONF_API_KEY])
    await hass.async_add_executor_job(client.get_trains)

    # Return info that you want to store in the config entry.
    # See `async_step_user` below for how this is used
    return {"title": DEFAULT_NAME}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MARTA."""

    VERSION = 1

    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""

        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)

                # Check if already configured
                # Doe not abort just overwrites
                # await self.async_set_unique_id("4545_567567", raise_on_progress=True)
                await self.async_set_unique_id(DEFAULT_NAME)
                self._abort_if_unique_id_configured()

                # test_train
                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAPI:
                errors[CONF_API_KEY] = "invalid_api_key"
            except InvalidBreeze:
                errors[CONFIG_BREEZE_CARD] = "invalid_access_token"
            except AbortFlow:
                errors["base"] = "already_configured_service"
            except APIKeyError:
                errors[CONF_API_KEY] = "invalid_api_key"
            except Exception as err:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception: %s", err)
                errors["base"] = "unknown"

        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAPI(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid hostname."""


class InvalidBreeze(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid hostname."""

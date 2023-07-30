import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
import voluptuous as vol
from .const import *
from .solarman import Inverter

SERVICE_WRITE_REGISTER = 'write_register'
PARAM_REGISTER = 'register'
PARAM_VALUE = 'value'
PARAM_MB_FC = 'modbus_function'

SERVICE_WRITE_MULTIPLE_REGISTERS = 'write_multiple_registers'
PARAM_REGISTERS = 'registers'
PARAM_VALUES = 'values'


# Register the services one can invoke on the inverter.
# Apart from this, it also need to be defined in the file 
# services.yaml for the Home Assistant UI in "Developer Tools"

_LOGGER = logging.getLogger(__name__)


SERVICE_WRITE_REGISTER_SCHEMA = vol.Schema(
    {
        vol.Required(PARAM_REGISTER): cv.positive_int,
        vol.Required(PARAM_VALUE): cv.positive_int,
        vol.Optional(PARAM_MB_FC): cv.byte
    }
)

SERVICE_WRITE_MULTIPLE_REGISTERS_SCHEMA = vol.Schema(
    {
        vol.Required(PARAM_REGISTERS): cv.string,
        vol.Required(PARAM_VALUES): cv.string
    }
)


def register_services (hass: HomeAssistant, inverter: Inverter ):
    async def send_command(call) -> None:
        inverter.service_write_register(
            register=call.data.get(PARAM_REGISTER),
            value=call.data.get(PARAM_VALUE),
            mb_fc=call.data.get(PARAM_MB_FC))
        return

    _LOGGER.debug(f'services.py:register_services: Register {SERVICE_WRITE_REGISTER}')
    hass.services.async_register(
        DOMAIN, SERVICE_WRITE_REGISTER, send_command, schema=SERVICE_WRITE_REGISTER_SCHEMA
    )

    async def send_command_multi(call) -> None:
        inverter.service_write_multi_registers(
            registers=call.data.get(PARAM_REGISTERS),
            values=call.data.get(PARAM_VALUES)
        )

    _LOGGER.debug(f'services.py:register_services: Register {SERVICE_WRITE_MULTIPLE_REGISTERS}')
    hass.services.async_register(
        DOMAIN, SERVICE_WRITE_MULTIPLE_REGISTERS, send_command_multi, schema=SERVICE_WRITE_MULTIPLE_REGISTERS_SCHEMA
    )
    return
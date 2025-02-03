""" SPIReg-C1101 provides predefined registers for the CC1101 chip. """

from . import status_register
from . import configuration_register

__all__ = ["status_register", "configuration_register"]

# SPIReg-C1101

**SPIReg-C1101** provides predefined register definitions for the **CC1101** transceiver using the SPIReg framework.

## Features

- Predefined register mappings for the CC1101 chip.
- Consistent access to register fields using the **SPIReg** notation.
- Supports both **status** and **configuration** registers.
- Ensures type-safe access to individual register fields.

## Installation

SPIReg-C1101 uses **spireg** under the hood.

```sh
pip install spireg_c1101
```

## Usage

```python
import spidev
from spireg_c1101.status_register import PARTNUM, VERSION
from spireg_c1101.configuration_register import IOCFG2

# Initialize SPI device
spi = spidev.SpiDev()
spi.open(0, 0)  # Use the appropriate SPI bus and device number
spi.max_speed_hz = 5000000  # Set the SPI clock speed

# Function to read a register
def read_register(register):
    address = register.register | 0x80  # Set the read bit
    response = spi.xfer2([address, 0x00])
    return response[1]

# Function to write a register
def write_register(register):
    address = register.register & 0x7F  # Clear the read bit
    spi.xfer2([address, int(register)])

# Read PARTNUM and VERSION
PARTNUM.value = read_register(PARTNUM.register)
VERSION.value = read_register(VERSION.register)
print(f"Part Number: {PARTNUM.value}")
print(f"Chip Version: {VERSION.value}")

# Read, toggle, and write IOCFG2
IOCFG2.value = read_register(IOCFG2)
IOCFG2.GDO2_INV ^= 1  # Toggle GDO2_INV
write_register(IOCFG2)
print(f"Updated IOCFG2: {IOCFG2.value}")

# Close SPI connection
spi.close()
```

## Registers

See the C1101 documentation for all available registers.

## SPI Communication

SPIReg-C1101 **only defines register structures**. The user is responsible for:

- Implementing SPI communication to read/write register values.
- Integrating with hardware-specific SPI drivers.
- Ensuring correct register access sequences as per the CC1101 datasheet.

## License
This project is licensed under **GPL-3.0-or-later**.  
For **commercial licensing**, please contact:
Daniël van den Berg
daniel@dmvandenberg.nl

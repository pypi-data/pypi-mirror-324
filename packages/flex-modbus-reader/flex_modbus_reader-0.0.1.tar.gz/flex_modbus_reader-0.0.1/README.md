# Flex Modbus Reader

Easily connect, debug and test any device that supports Modbus TCP!

## Features:
- Splitting a request by chunks with configurable chunck size value. (Modbus TCP protocol supports maximum of 260 bytes per request, but it also depends on the device's manufactorer.)
- Auto-skip no needed registers in a bytes stream.
- Supports index auth-shifting. (By default, registers are addressed starting at zero, but therefore devices that specify 1-16 are addressed as 0-15.)


# Installation Guide

## Prerequisites
- `python` version 3.9 or later

## Installation:
```shell
pip install flex-modbus-reader
```

# Integrate your modbus device

## Examples:
You can find an example of integrating Modbus energy meter in `flexmodbusreader/examples` module.

## Writing your own ModbusDevice class:

### Steps:
- Check the manufacturer documentation to find registers you need to read.
- Create the registers map
- Use this map to get the data from the device

```python3
from pymodbus.constants import Endian

from flexmodbusreader.device import ModbusDevice, Register
from flexmodbusreader.reader import ModbusDeviceDataReader


device = ModbusDevice(
    model="Energy Meter",
    registers_map=[
        Register("value_1", 3000, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("value_2", 3002, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("value_3", 3004, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("value_4", 3200, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("value_5", 3202, 2, ModbusTcpClient.DATATYPE.INT32),
        Register("value_6", 3204, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("value_7", 3250, 2, ModbusTcpClient.DATATYPE.UINT64),
        Register("value_8", 3252, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("value_9", 3340, 2, ModbusTcpClient.DATATYPE.FLOAT32),
    ],
    unit=10, # Modbus Slave ID
    index_shift=-1 # the value by which to shift the indices
)

client = ModbusTcpClient("192.168.0.1", port=5030, timeout=1)
reader = ModbusDeviceDataReader(
    client=client, # ModbusTcpClient
    byteorder=Endian.BIG, # byte endianess. Needed for decoding
    wordorder=Endian.BIG, # word endianess. Needed for decoding
    message_size=100, # Maximum size of register to read per one request
    device=device, # ModbusDevice instance
)

data = reader.read_registers() # returns a dict with decoded values 

```

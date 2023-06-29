from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from PySide6.QtCore import QThread, QTimer, Signal, Slot, QObject
from PySide6.QtWidgets import QWidget
from logging import info, debug, warning, error
import hashlib
from typing import Optional, Union
import numpy as np
from radeye.components.component import GAIN, OFFSET, ANGLE


SerialPortError = QSerialPort.SerialPortError

FILTER_KEYWORDS = "STMicroelectronics"

TOPICS = ["led", "polar", "address", "channel", "phase", "gain", "exgain"]
""" ComPort Format
| SPI communication     | Channel   | Phase     | Atten + Gain      | Ex-Gain |
-------------------------------------------------------
| 1-4 -   Address       | 1-4       | 0-127     | 0x80 + 0-127      | 0-127   |
| 5 - LED Blink         | -         | -         | -                 | -       |
| 6 - Polarization      | -         | -         | -                 | -       |
"""
""" Register Table
||          ||          ||  (MSB)   ||  Bit 6   ||   Bit 5  ||   Bit 4  ||  Bit 3   ||  Bit 2   ||  Bit 1   ||  (LSB)   ||
||  Name    ||  Address ||  Bit 7   ||  Bit 6   ||   Bit 5  ||   Bit 4  ||  Bit 3   ||  Bit 2   ||  Bit 1   ||  Bit 0   ||
------------------------------------------------------------------------------------------------------------------------------
|| SPI      ||  0x00    ||   --     ||    --    ||    --    ||    --    ||           (1-4)   address[2:0]               ||   
|| SPI      ||  0x00    ||   --     ||    --    ||    --    ||    --    ||           ( 5 )   LED                        ||   
|| SPI      ||  0x00    ||   --     ||    --    ||    --    ||    --    ||           ( 6 )   Polarization               ||   
|| Channel  ||  0x01    ||   --     ||    --    ||    --    ||    --    ||           (1-4)   channel[2:0]               ||
|| Channel  ||  0x01    ||   --     ||    --    ||    --    ||    --    ||      0 for clockwise         if SPI == 6     ||    
|| Channel  ||  0x01    ||   --     ||    --    ||    --    ||    --    ||      1 for anti-clockwise    if SPI == 6     ||    
|| Phase    ||  0x02    ||   --     ||                          phase angle (0 - 127)                                   ||
|| Gain     ||  0x03    ||   atten  ||                          gain        (0 - 127)                                   ||
|| ExGain   ||  0x04    ||   --     ||                          ex-gain     (0 - 127)                                   ||
"""
""" DATA Format
| FORMAT NAME   | Byte Address  |   Bit Address     | Byte Size     |   INPUT RANGE     | OUTPUT RANGE  |
---------------------------------------------------------------------------------------------------------
|   LED         |  0x00         |   0b00000101      | 1 (bit)       |       0-1         |       0-1     |
|   Polar       |  0x00         |   0b00000110      | 1 (bit)       |       0-1         |       0-1     |
|   Address     |  0x00         |   0b00000001      | 3 (bit)       |       0-4         |       1-4     |
|   Channel     |  0x01         |   0b00000001      | 3 (bit)       |       0-4         |       1-4     |
|   Phase       |  0x02         |   0b00000001      | 7 (bit)       |       0-360       |       0-127   |
|   Atten       |  0x03         |   0b10000000      | 1 (bit)       |       0-1         |       0-1     |
|   Gain        |  0x03         |   0b00000001      | 7 (bit)       |       0-127       |       0-127   |
|   ExGain      |  0x04         |   0b00000001      | 7 (bit)       |       0-127       |       0-127   |
"""
REGISTER_MAP = [
    ("led", 0x00, 0b00000101, 1, (0, 1), (0, 1)),
    ("polar", 0x00, 0b00000110, 1, (0, 1), (0, 1)),
    ("address", 0x00, 0b00000001, 3, (0, 4), (0, 4)),
    ("channel", 0x01, 0b00000001, 3, (1, 4), (1, 4)),
    ("phase", 0x02, 0b00000001, 7, (0, 360), (0, 127)),
    ("atten", 0x03, 0b10000000, 1, (0, 1), (0, 1)),
    ("gain", 0x03, 0b00000001, 7, (0, 127), (0, 127)),
    ("exgain", 0x04, 0b00000001, 7, (0, 127), (0, 127)),
]
POLARIZATION = {"clockwise": 0, "anti-clockwise": 1}

DATA_FORMAT = [
    "name",
    "byte_address",
    "bit_address",
    "byte_size",
    "input_range",
    "output_range",
]

TERMINATOR = b"\r"


""" Serialize a packet into a formatted bytestring
Args:
    format: order list of strings
Returns:
    object: that taken the dictionary of data will format into a serialized bytestring
"""


class Serializer(object):
    def __init__(self, register_map) -> None:
        self.register_map = register_map

    def combine(self, channel_data: dict) -> bytearray:
        byte_array = []
        num_bytes = 0
        for channel_format in self.register_map:
            (
                name,
                byte_address,
                bit_address,
                byte_size,
                input_range,
                output_range,
            ) = channel_format
            data = channel_data.get(name, 0)
            byte_data = self.to_bytes(data, channel_format)
            byte_array.append(byte_data)
            num_bytes = max(num_bytes, byte_address)

        return int.to_bytes(sum(byte_array), num_bytes)

    def to_bytes(self, data, register_map):
        (
            name,
            byte_address,
            bit_address,
            byte_size,
            input_range,
            output_range,
        ) = register_map
        # verify bit_size match output_range
        assert (
            np.log2(output_range[1] - output_range[0] + 1) <= byte_size
        ), "output range should be within bit size"

        data = (
            self.remap(
                data, input_range[0], input_range[1], output_range[0], output_range[1]
            )
            * bit_address
            * (1 << (8 * byte_address))
        )
        return int(data)

    def remap(self, data, input_min, input_max, output_min, output_max):
        assert input_max - input_min != 0, "input range should not be zero"

        result = data * (output_max - output_min) / (input_max - input_min) + output_min
        return result

    def format(self, data) -> bytearray:
        byte_data = self.combine(data)
        return b"".join([byte_data, TERMINATOR])

    def encode(self, data: dict) -> bytearray:
        result = None
        if data is None:
            error("Data is None")
            return

        try:
            result = self.format(data)
        except OverflowError as e:
            error(e)
        finally:
            return result


class Deserializer(object):
    def __init__(self, register_map) -> None:
        self.register_map = register_map

    def from_bytes(self, byte_data, register_map):
        bytes_array = sum(
            [
                int.from_bytes(byte) * (1 << 8 * idx)
                for idx, byte in enumerate(byte_data)
            ]
        )
        data_dict = {}
        for name, byte_address, bit_address, byte_size, _, _ in register_map:
            data = bytes_array & (bit_address * (1 << 8 * byte_address))

            data_dict.update({name: data if byte_size > 1 else data == bit_address})
        return data_dict

    # decode bytestring into a dictionary
    def decode(self, data: bytearray) -> dict:
        return self.from_bytes(data, self.register_map)


"""Subscriber interface
Args:
    topics: topics subscribed to update by each interval
    update interval: interval to pooling data in ms
Returns:
    _type_: _description_
"""


class Subscriber(QObject):
    dataUpdated = Signal(QSerialPort, bytes)

    def __init__(self, update_interval=100, hash_algo=hashlib.sha3_256) -> None:  # ms
        super().__init__()
        self.port_pool = []

        self.hash_history = dict()  # list of hash object
        self.hash = lambda x: hash_algo(x).hexdigest()

        self.timer = QTimer()
        self.timer.setInterval(update_interval)
        # self.timer.timeout.connect(self.listen)
        # self.timer.start()

    # def listen(self):
    #     for port in self.port_pool:
    #         self.pool(port)

    def bind_port(self, port):
        port.readyRead.connect(self.pool)
        self.port_pool.append(port)
        

    def update_port(self, ports):
        self.port_pool = ports

    def get(self, port):
        """Get data from serial port"""
        byte_data = read_data(port)
        return byte_data

    @Slot()
    def pool(self, port) -> None:
        updated = False
        """ data has to be encoded to bytes 
        """
        data = self.get(port)
        hash = self.hash
        port_hash = hash(bytes(port.portName(), encoding="utf-8"))
        data_hash = hash(data)
        hash_history = self.hash_history

        """
        Logic Table:
        port_hash in hash_history | data_hash == hash_history   | explain
        True                      | True                        | data is not updated
        False                     | True                        | impossible
        True                      | False                       | data is updated
        False                     | False                       | data is updated
        """
        if port_hash in hash_history.keys() and data_hash == hash_history.get(
            port_hash
        ):
            return
        else:
            updated = True

        if updated:
            self.hash_history.update({port_hash: data_hash})
            self.dataUpdated.emit(port, data)


class QSerialPortManger(object):
    """QSerialPortManger.
    Args:
        sub_topics      : topics subscribed to update by each interval
        register_map    : byte address data format
        update_interval : interval for subscriber to pooling data (in ms)
    """

    readReady = Signal(QSerialPort, dict)

    def __init__(self, sub_topics, register_map, update_interval=100) -> None:
        self.worker = QThread()

        """TODO: add serial port pool"""
        self.serialpool = []
        self.topics = sub_topics
        self.register_map = register_map

        self.update_interval = update_interval  # ms
        self.port_table = {}
        self.serializer = Serializer(self.register_map)
        self.deserializer = Deserializer(self.register_map)

        self.subscriber = Subscriber(self.update_interval)
        self.subscriber.moveToThread(self.worker)
        self.subscriber.dataUpdated.connect(self.read)

        self.worker.start()

    def __del__(self):
        self.worker.quit()
        self.worker.wait()

    def connect(self, port):
        self.serialpool.append(port)
        self.serialpool[-1].moveToThread(self.worker)
        self.subscriber.bind_port(self.serialpool[-1])

    """Bind serial port to patch for us to lookup which patch to update or sending data"""

    def bind(self, port: QSerialPort, patch: object):
        # use port as key to lookup patch, as port are persistent
        self.port_table.update({port: patch})

    # read bytes data from serial port and decode into dictionary
    def read(self, port, byte_data: bytearray) -> dict:
        data = self.deserializer.decode(byte_data)
        self.readReady.emit(port, data)
        return data

    def write(self, port, data: dict) -> None:
        byte_data = self.serializer.encode(data)
        send_data(port, byte_data)

    def init_serial(self):
        """
        Bind all matching available ports to the serial object
        """
        # We are using STM32 MCU, so we filter out all ports that are not matching
        available_ports = filter_ports_by_manufacturer(get_all_ports(), FILTER_KEYWORDS)
        if len(available_ports) == 0:
            warning("No available ports found")
            return
        ports = []
        for portInfo in available_ports:
            try:
                ports.append(connect_port(portInfo))
            except:
                pass
        return ports


def connect_port(portInfo):
    serialport = QSerialPort()

    if portInfo is not None:
        try:
            serialport.setPort(portInfo)
            serialport.open()
        except:
            error("Error: Could not connect to port")
            # Not implemented yet
        finally:
            return serialport


def get_all_ports():
    return QSerialPortInfo.availablePorts()


def filter_ports_by_manufacturer(ports_found, keywords):
    filtered_ports = []

    for portInfo in ports_found:
        # filter out all ports that are not matching the manufacturer keywords
        if keywords in portInfo.manufacturer():
            filtered_ports.append(portInfo)

    return filtered_ports

    # Todo: add button to ping to STM
    # Use Thread to manage multiple serial signals
    """_summary_
    | SPI communication     | Channel   | Phase     | Atten + Gain      | Ex-Gain |
    -------------------------------------------------------
    | 1-4 -   Address       | 1-4       | 0-127     | 0x80 + 0-127      | 0-127   |
    | 5 - LED Blink         | -         | -         | -                 | -       |
    | 6 - Polarization      | -         | -         | -                 | -       |
    """


def send_data(serialport, data):
    if not serialport.error() in SerialPortError:
        try:
            serialport.write(data)
        except:
            warning("Error: Could not write to port")
        finally:
            pass


def read_data(serialport):
    if not serialport.error() in SerialPortError:
        try:
            data = serialport.readLine()
            return data
        except:
            warning("Error: Could not read from port")
        finally:
            pass

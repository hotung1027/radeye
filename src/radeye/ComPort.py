from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from PySide6.QtCore import QThread,QTimer,Signal
from logging import info,debug,warning,error
import hashlib

SerialPortError = QSerialPort.SerialPortError

FILTER_KEYWORDS = "STMicroelectronics"
DATA_FORMAT = [
     "spi",
     "channel",
     "phase",
     "gain",
     "exgain"
     
]
TERMINATOR = "\r"


""" Serialize a packet into a formatted bytestring
Args:
    format: order list of strings
Returns:
    object: that taken the dictionary of data will format into a serialized bytestring
"""
class Serializer(object):
    def __init__(self,format) -> None:
       self.format = format 

    def encode(self, data:dict)-> bytearray:
        result = None
        if data is None:
            error("Data is None")
            return 
        
        try:
            result =  b''.join([
            int.to_bytes(data.get(key),1,"big") 
            for key in self.format 
                if key in data.keys()])
        except OverflowError as e:
            error(e)
        finally:
            return result
        
class Deserializer(object):
    def __init__(self,format) -> None:
       self.format = format 


    # decode bytestring into a dictionary
    def decode(self, data:bytearray)-> dict:
        return dict(
            zip(
                self.format,
                [int(byte) for byte in data]
                ))
        

    """Subscriber interface
    Args:
        topics: topics subscribed to update by each interval
        update interval: interval to pooling data in ms
    Returns:
        _type_: _description_
    """
class Subscriber(object):
    dataUpdated = Signal(bytes)
    def __init__(self,
                 topics = ["phase","gain"],
                 update_interval = 100, #ms
                 hash_algo = hashlib.sha3_256
                 ) -> None:
        self.topics = []
        self.subscriber = None
        self.timer = QTimer()
        self.hash_history = [""] # list of hash object
        self.hash = hash_algo
        pass

    def get(self,topic):
        pass
    

    def pool(self) -> None:
        updated = False
        """ data has to be encoded to bytes 
        """
        for index , (topic, history) in enumerate(zip(self.topics,self.hash_history)):
            data = self.get(topic)
            if not hash(data).hexdigest() == history.hexdigest():
            # get data
                updated = True
                self.hash_history[index] = hash(topic)

        if updated:
            self.dataUpdated.emit(data)


class QSerialPortManger(object):
    def __init__(self) -> None:
        self.worker = QThread()
        self.serialpool =  []
        self.topics = []
        self.update_interval = 100 #ms
        self.subscriber = Subscriber(self.topics,self.update_interval)

        pass

    def connect(self, port):
        self.serialpool.append(port)
        self.serialpool[-1].moveToThread(self.worker)
        self.serialpoll[-1].readRead.connect(self.read)
        pass

    def read(self,data):
        pass

    def write(self,data):
        pass







def init_serial():
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
        except:
            error("Error: Could not connect to port")
             # Not implemented yet
        finally:
            return serialport


def get_all_ports(): 
    return QSerialPortInfo.availablePorts()


def filter_ports_by_manufacturer(ports_found,keywords):
    filtered_ports = []

    for portInfo in ports_found:
        # filter out all ports that are not matching the manufacturer keywords
        if keywords in portInfo.manufacturer():
            filtered_ports.append(portInfo)

    return filtered_ports



#Todo: add button to ping to STM
# Use Thread to manage multiple serial signals
    """_summary_
    | SPI communication     | Channel   | Phase     | Atten + Gain      | Ex-Gain |
    -------------------------------------------------------
    | 1-4 -   Address       | 1-4       | 0-127     | 0x80 + 0-127      | 0-255   |
    | 5 - LED Blink         | -         | -         | -                 | -       |
    | 6 - Polarization      | -         | -         | -                 | -       |
    """

def send_data(serialport,data):
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
            return serialport.readAll()
        except:
            warning("Error: Could not read from port")
        finally:
            pass


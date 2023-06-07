from PySide6.QtSerialPort import QSerialPort
from PySide6.QtSerialPort import QSerialPortInfo
from logging import info,debug,warning,error



def init_serial():
    # We are using STM32 MCU, so we filter out all ports that are not matching 
    available_ports = filter_ports(get_all_ports(),"STMicroelectronics")
    
    for port in available_ports:
        if port is not "None":
            try:
                ser = serial.Serial(port, 4000000, timeout=10)
                ser.writeTimeout = 0.1

                if ser.isOpen():
                    GUI.set_all_check["text"] = "Connect to: " + "\n" + ser.port
                    break
            except:
                pass


def conect_port(portInfo):
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


def filter_ports(ports_found,keywords):
    filtered_ports = []

    for portInfo in ports_found:
        # filter out all ports that are not matching the manufacturer keywords
        if keywords in portInfo.manufacturer():
            filtered_ports.append(portInfo)

    return filtered_ports


#Todo: add button to ping to STM
def send_data(serialport,data):

    try:
        pass
    except:
        pass
    finally:
        pass





import sys
import numpy as np
import time

from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


from PySide6.QtUiTools import QUiLoader
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtNetwork import QTcpSocket,QAbstractSocket
from PySide6.QtCore import QFile, QIODevice, QThread, Signal, Slot, QObject
from PySide6.QtGui import QIcon,QPixmap
import pyqtgraph as pg

from ui_panel import Ui_MainWindow
from trafficlight import *

from fxpmath import Fxp

SocketState = QAbstractSocket.SocketState()

UI_PATH = "panel.ui"
HOSTNAME = ""
PORT = ""
client = QTcpSocket()
x_data = []
y_data = []

REDLIGHT = u":/resources/icons/trafficlight/redlight.png"
YELLOWLIGHT = u":/resources/icons/trafficlight/yellowlight.png"
GREENLIGHT = u":/resources/icons/trafficlight/greenlight.png"


class Data(QObject):
    dataChanged = Signal(list, list)

    def __init__(self):
        super(Data,self).__init__()
        self.x_data = []
        self.y_data = []

    def update_data(self,x,y):
        self.x_data = x
        self.y_data = y
        self.dataChanged.emit(self.x_data,self.y_data)

    def update_xdata(self, x):
        self.x_data = x
        self.dataChanged.emit(self.x_data,self.y_data)

    def update_ydata(self, y):
        self.y_data = y
        self.dataChanged.emit(self.x_data,self.y_data)

    def get_data(self):
        return self.x_data, self.y_data




@Slot()
def tcp_connect():
    client.connectToHost(HOSTNAME, PORT)
    if client.waitForConnected(1000):
        print("Connected")
    else:
        print("Not connected")


@Slot()
def update_connection_status(state : SocketState):
    if state == SocketState.ConnectedState:
        window.ui.trafficlight.setPixmap(QPixmap(GREENLIGHT))
    elif state == SocketState.UnconnectedState:
        window.ui.trafficlight.setPixmap(QPixmap(REDLIGHT))
    else:
        window.ui.trafficlight.setPixmap(QPixmap(YELLOWLIGHT))


@Slot()
def update_hostname():
    global HOSTNAME
    HOSTNAME = window.ui.addressText.toPlainText()
    print(HOSTNAME)

@Slot()
def update_port():
    global PORT
    PORT = int(window.ui.portText.toPlainText())
    print(PORT)

@Slot()
def buttonGroupCheckButton(button):
## exclusive button group, only 1 button among group toggled at a time
    return
#     for butt in ButtonGroup.buttons():
#         if butt.isChecked():
#             butt.nextCheckState()
#             print(butt.text())
#     button.nextCheckState()
#     print(button.text())

def RUN():
    query_waveform()

def STOP():
    return

def SINGLE():
    query_waveform()
    

def query_waveform():
    client.write(b"Test\n")
    print("Bytes Written")


def twos_complement(bit):
   fn = lambda x: x - 1 << bit if x > 1 << (bit-1) else x
   return fn

def vectorize(array : np.ndarray, fn) -> np.ndarray:
    return np.array(
        list(
        map( fn,
            array)
        )
    )



def get_waveform() -> bytearray:
    global y_data,x_data,waveform
    y_data = client.readLine()
    y_data = bytes(y_data).decode('utf-8').split(':')
    y_data = np.array(y_data,dtype=np.int16)
    si16 = lambda x : Fxp(bin(x),True,12,11).get_val()
    y_data = vectorize(y_data, si16)
    x_data = np.arange(0, len(y_data), 1)
    waveform.update_data(x_data,y_data)



def plot_waveform(x,y):
    global window
    window.ui.dataView.plotItem.plot(x,y)
    y_fft = np.fft.fft(y).real
    window.ui.processView.plotItem.plot(x,y_fft)

# def plot_fft():
#     return



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)




if __name__ == '__main__':
    app = QApplication(sys.argv)

    # ui_file = QFile(UI_PATH)
    # if not ui_file.open(QIODevice.ReadOnly):
    #     print(f"Cannot open {ui_file}: {ui_file.errorString()}")
    #     sys.exit(-1)

    window = MainWindow()  
    window.ui.addressText.textChanged.connect(update_hostname)
    window.ui.portText.textChanged.connect(update_port)
    window.ui.connectButton.clicked.connect(tcp_connect)

    waveform = Data()


    ButtonGroup = window.ui.buttonGroup
    ButtonGroup.buttonClicked.connect(lambda button: buttonGroupCheckButton(button))
    window.ui.singleButton.clicked.connect(SINGLE)
    window.ui.runButton.toggled.connect( RUN)
    window.ui.stopButton.toggled.connect(STOP)

    client.stateChanged.connect(lambda state : update_connection_status(state))
    client.readyRead.connect(get_waveform)
    waveform.dataChanged.connect(lambda x,y : plot_waveform(x,y))
    # ui_file.open(QFile.ReadOnly)

    # loader = QUiLoader()
    # window = loader.load(ui_file)
    # ui_file.close()
    # if not window:
    #     print(loader.errorString())
    #     sys.exit(-1)

    window.show()





    sys.exit(app.exec())
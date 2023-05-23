"""
My first application
"""
import sys
import numpy as np
import time





try:
    from importlib import metadata as importlib_metadata
except ImportError:
    # Backwards compatibility - importlib.metadata was added in Python 3.8
    import importlib_metadata

from PySide6.QtUiTools import QUiLoader
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtNetwork import QTcpSocket,QAbstractSocket
from PySide6.QtCore import QFile, QIODevice, QThread, Signal, Slot, QObject,QTimer, QTimerEvent
from PySide6.QtGui import QIcon,QPixmap
import pyqtgraph as pg

from radeye.ui_panel import Ui_MainWindow
from radeye.trafficlight import *

from fxpmath import Fxp

SocketState = QAbstractSocket.SocketState()

UI_PATH = "panel.ui"
HOSTNAME = ""
PORT = ""
client = QTcpSocket()
x_data = []
y_data = []
waveform = []
window = []
REDLIGHT = u":/resources/icons/trafficlight/redlight.png"
YELLOWLIGHT = u":/resources/icons/trafficlight/yellowlight.png"
GREENLIGHT = u":/resources/icons/trafficlight/greenlight.png"

s16i11 = lambda x : Fxp(f'0b{np.binary_repr(x,12)}',True,12,11,overflow='wrap').get_val()


class radeye(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.trafficlight.setPixmap(QPixmap(REDLIGHT))
        self.ui.addressText.textChanged.connect(update_hostname)
        self.ui.portText.textChanged.connect(update_port)
        self.ui.connectButton.clicked.connect(tcp_connect)
        ButtonGroup = self.ui.buttonGroup
        ButtonGroup.buttonClicked.connect(lambda button: buttonGroupCheckButton(button))
        self.ui.singleButton.clicked.connect(SINGLE)
        # self.ui.runButton.toggled.connect(SINGLE)
        self.ui.stopButton.toggled.connect(STOP)
        self.ui.runButton.clicked.connect(RUN)
        self.ui.applyButton.clicked.connect(update_size)
        self.timer = QTimer()
        self.timer.timeout.connect(RUN)
        self.timer.start(100)





        self.show()


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
def update_size():
    global client
    size = int(window.ui.sizeText.toPlainText())
    client.write(bytes("ConfigSize:{size}\n".format(size=size),'utf-8'))


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
    global window,client
    if window.ui.runButton.isChecked() and client.state() == SocketState.ConnectedState:
    ## #TODO: ARM Ready signal
        query_waveform()
            

def STOP():
    return

def SINGLE(checked):
    if checked:
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
    print(y_data)
    y_data = bytes(y_data).decode('utf-8').split(':')
    print(y_data)
    y_data = np.array(y_data,dtype=np.int16)
    y_data = vectorize(y_data, s16i11)
    x_data = np.arange(0, len(y_data), 1)
    waveform.update_data(x_data,y_data)



def plot_waveform(x,y):
    global window
    window.ui.dataView.plotItem.plot(x,y,clear=True)
    y_fft = np.fft.rfft(y)
    fs = int(window.ui.sampleRateText.toPlainText())
    L = len(y_fft)
    f = fs * np.arange(0,L) / L/2
    p2 = np.abs(y_fft/L)
    # p1 = p2[0:int(L/2)]
    # p1[2:-1] = 2*p1[2:-1]

    window.ui.processView.plotItem.plot(f,p2,clear=True)




def main():
    global window,waveform
    # Linux desktop environments use app's .desktop file to integrate the app
    # to their application menus. The .desktop file of this app will include
    # StartupWMClass key, set to app's formal name, which helps associate
    # app's windows to its menu item.
    #
    # For association to work any windows of the app must have WMCLASS
    # property set to match the value set in app's desktop file. For PySide2
    # this is set with setApplicationName().

    # Find the name of the module that was used to start the app
    app_module = sys.modules['__main__'].__package__
    # Retrieve the app's metadata
    metadata = importlib_metadata.metadata(app_module)

    QApplication.setApplicationName(metadata['Formal-Name'])
    app = QApplication(sys.argv)
    waveform = Data()
    window = radeye()
    textedits = [window.ui.addressText,window.ui.portText,window.ui.sizeText,window.ui.sampleRateText]
    assignPlaceHolderText = lambda obj: obj.setPlainText(obj.placeholderText())
    for te in textedits:
        assignPlaceHolderText(te)

    client.stateChanged.connect(lambda state : update_connection_status(state))
    client.readyRead.connect(get_waveform)

    waveform.dataChanged.connect(lambda x,y : plot_waveform(x,y))
    sys.exit(app.exec())
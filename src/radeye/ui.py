

import sys
import numpy as np
import time


from PySide6.QtUiTools import QUiLoader
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtNetwork import QTcpSocket,QAbstractSocket
from PySide6.QtCore import QFile, QIODevice, QThread, Signal, Slot, QObject
from PySide6.QtGui import QIcon,QPixmap
import pyqtgraph as pg


from radeye.trafficlight import *

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


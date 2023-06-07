"""
My first application
"""
import sys
from typing import Optional
import numpy as np
import time
import logging
from logging import debug,warning,error,info




try:
    from importlib import metadata as importlib_metadata
except ImportError:
    # Backwards compatibility - importlib.metadata was added in Python 3.8
    import importlib_metadata

from PySide6.QtUiTools import QUiLoader
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtNetwork import QTcpSocket,QAbstractSocket
from PySide6.QtCore import QFile, QIODevice, QThread, Signal, Slot, QObject,QTimer, QTimerEvent,QEvent
from PySide6.QtGui import (QMouseEvent)
from PySide6.QtGui import QIcon,QPixmap
import pyqtgraph as pg

from radeye.panel_ui import Ui_MainWindow
from radeye.trafficlight import *

from fxpmath import Fxp


from radeye.ui        import REDLIGHT,YELLOWLIGHT,GREENLIGHT
from plotly.graph_objects import Figure, Scatter
import plotly.express as px
import plotly
import pandas as pd
from radeye.attena_ui import Ui_AttenaUi
from radeye.patch_ui  import Ui_PatchUi
import radeye.attena_rc
from qt_material import apply_stylesheet
from radeye.components.component import TcpClient,Data,SocketState,Patch,Attena
from radeye.ulti_fn import counterclockwise_phasearray_index

waveform      = Data()


class radeye(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.client = TcpClient(self.ui)
        self.client.socket.readyRead.connect(self.client.get_waveform(waveform))

        self.ui.trafficlight.setPixmap(QPixmap(REDLIGHT))
        self.ui.addressText.textChanged.connect(lambda : self.client.update_hostname(self.ui.addressText.toPlainText()))
        self.ui.portText.textChanged.connect(lambda : self.client.update_port(self.ui.portText.toPlainText()))
        self.ui.connectButton.clicked.connect(self.client.tcp_connect)
        self.ui.singleButton.clicked.connect(self.SINGLE)
        self.ui.stopButton.toggled.connect(self.STOP)
        self.ui.runButton.clicked.connect(self.RUN)
        self.ui.applyButton.clicked.connect(self.client.update_size)
        self.ui.rowsLineEdit.textChanged.connect(self.update_patch)
        self.ui.columnsLineEdit.textChanged.connect(self.update_patch)
        

        self.antennas = [] 
        self.patches = []
        angle = (2.8125*np.arange(-127,128,1)).astype(str)
        self.ui.thetaComboBox.addItems(angle)
        self.ui.phiComboBox.addItems(angle)


        self.ui.gridLayout.update()

        self.timer = QTimer()
        self.timer.timeout.connect(self.RUN)
        self.timer.start(100)
        self.show()

    def update_antenna(self,antennas:list)->None:
        if self.ui.gridLayout_2.count() > 0:
            self.remove_antenna()
            self.antennas = []

        print(antennas[0].objectName())
        if any(word in antennas[0].objectName() for word in ["ll","lr"]) :
            self.antennas  = counterclockwise_phasearray_index(antennas,2)
        else:
            self.antennas  = counterclockwise_phasearray_index(antennas,0)
        
        for i in range(0,len(antennas)):
            self.antennas[i].show()
            self.ui.gridLayout_2.addWidget(self.antennas[i],int(i/2),i%2)


        

    def remove_antenna(self)->None:
        print(self.antennas)
        for i in range(0,len(self.antennas)):
            self.ui.gridLayout_2.removeWidget(self.antennas[i])
            self.antennas[i].hide()


    
    def change_patch_layout(self,)->None:
        pass

    def add_patch(self,numberOfPatch: int)->None:
        for i in range(0,numberOfPatch):
            if i >= len(self.patches):
                self.patches.append(Patch())            
                self.patches[i].setObjectName("PatchCH{}".format(i+1))
                self.patches[i].setupUi(self.patches[i])
                self.patches[i].setStyleSheet(u"QFrame{\n"
                    "border-image: url(:/resources/indicator/Preview - Bottom.png);\n"
                    "}\n"
                    "")
            self.patches[i].changedActivatedAntenna.connect(self.update_antenna)
            self.patches[i].show()
            self.ui.gridLayout.addWidget(self.patches[i],int(i/int(self.ui.columnsLineEdit.text())),i%int(self.ui.columnsLineEdit.text()))
            
        
    def remove_patch(self,numberOfPatch:int)->None:
        for i in reversed(range(0,numberOfPatch)):
            self.ui.gridLayout.removeWidget(self.patches[i])
            self.patches[i].hide()
    
    # def remove_patch(self,patches) -> None:
    #     for patch in patches:
    #         self.ui.gridLayout.removeWidget(patch)
    #         patch.hide()
                                        

    def update_patch(self)->None:
        # format text to integer, if not integer erase then
        if not self.ui.rowsLineEdit.text().isdigit():
               self.ui.rowsLineEdit.setText("")
        if not self.ui.columnsLineEdit.text().isdigit():
               self.ui.columnsLineEdit.setText("")
        # get the number of rows and columns
        if self.ui.rowsLineEdit.text() != "" and self.ui.columnsLineEdit.text() != "":
            nRows = int(self.ui.rowsLineEdit.text())
            nCols = int(self.ui.columnsLineEdit.text())
            if nRows * nCols > len(self.patches):
                self.add_patch(nRows * nCols)
            elif nRows * nCols < len(self.patches):
                self.remove_patch(nRows * nCols)



                       
    def set_up_attena(self,attenas:int)->None:
        if attenas > len(self.antennas):
            self.add_attena(attenas - len(self.antennas))
        elif attenas < len(self.antennas):
            self.remove_attena(len(self.antennas) - attenas)

    def RUN(self):
        if self.ui.runButton.isChecked() and self.client.socket.state() == SocketState.ConnectedState:
        ## #TODO: ARM Ready signal
            self.client.send_waveform_query()
                

    def STOP(self):
        return

    def SINGLE(self,checked):
        if checked:
            self.client.send_waveform_query()
    



def plot_waveform(x,y):
    global window,waveform

    df = pd.DataFrame(dict(
        x= x,
        y = y
    ))
    fig = px.line(df,x="sample",y="normalized Amplitude")
    window.ui.dataView.plotItem.plot(x,y,clear=True)
    y_fft = np.fft.rfft(y)
    fs = int(window.ui.sampleRateText.toPlainText())
    L = len(y_fft)
    f = fs * np.arange(0,L) / L/2
    p2 = np.abs(y_fft/L)

    window.ui.processView.plotItem.plot(f,p2,clear=True)
    waveform.flush()


# def plot_waveform(x,y):
#     global window,waveform

#     df = pd.DataFrame(dict(
#         x= x,
#         y = y
#     ))
#     fig = px.line(df,x="sample",y="normalized Amplitude")

#     html = "<html><body>"
#     html += plotly.io.to_html(fig,include_plotlyjs=True,full_html=True)
#     html += "</body></html>"
#     window.ui.processView.setHtml(html)
#     # y_fft = np.fft.rfft(y)
#     # fs = int(window.ui.sampleRateText.toPlainText())
#     # L = len(y_fft)
#     # f = fs * np.arange(0,L) / L/2
#     # p2 = np.abs(y_fft/L)

#     # window.ui.processView.plotItem.plot(f,p2,clear=True)
#     waveform.flush()







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
    window = radeye()


    textedits = [window.ui.addressText,window.ui.portText,window.ui.sizeText,window.ui.sampleRateText]
    assignPlaceHolderText = lambda obj: obj.setPlainText(obj.placeholderText())
    for te in textedits:
        assignPlaceHolderText(te)
    # filter = MousePressEventFilter()
    # window.installEventFilter(filter)
    waveform.dataChanged.connect(lambda x,y : plot_waveform(x,y))
    # apply_stylesheet(app, theme='dark_teal.xml')
    sys.exit(app.exec())
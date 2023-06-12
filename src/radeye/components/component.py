from typing import Optional
import numpy as np
from PySide6.QtCore import QObject, Signal, Slot,QEvent
from PySide6.QtNetwork import QTcpSocket, QAbstractSocket
from PySide6.QtGui import QIcon,QPixmap
from radeye.ulti_fn import s16i11, vectorize
from radeye.ui import REDLIGHT, YELLOWLIGHT, GREENLIGHT

import math
from radeye.attena_ui import Ui_AttenaUi
from radeye.patch_ui import Ui_PatchUi
from radeye.ulti_fn import counterclockwise_phasearray_index,split_patches



SocketState = QAbstractSocket.SocketState()
GAIN = np.arange(1,101,1) * 1.27
OFFSET = np.arange(-127,128,1) * 2.8125
ANGLE = np.arange(-127,128,1) * 2.8125

class Data(QObject):
    dataChanged = Signal(list, list)

    def __init__(self):
        super(Data,self).__init__()
        self.x_data = []
        self.y_data = b''

    def flush(self):
        self.x_data = []
        self.y_data = b''

    def concat(self,y):
        self.y_data = self.y_data + y
    
    def confirm(self):
        y_data = bytes(self.y_data).decode('utf-8').split(':')[0:-1]
        y_data = np.array(y_data,dtype=np.int16)
        y_data = vectorize(y_data, s16i11)
        self.y_data = y_data
        self.x_data = np.arange(0,len(self.y_data),1)
        self.dataChanged.emit(self.x_data,self.y_data)


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


class TcpClient(QObject):

    def __init__(self, parent: QObject | None = ...) -> None:
        super(TcpClient, self).__init__()
        self.socket   = QTcpSocket()
        self.HOSTNAME = ""
        self.PORT     = ""
        self.ui       = parent
        self.socket.stateChanged.connect(lambda state : self.update_connection_status(state))

    
    @Slot()
    def tcp_connect(self):
        self.socket.connectToHost(self.HOSTNAME, self.PORT)
        if self.socket.waitForConnected(1000):
            print("Connected")
        else:
            print("Not connected")


    @Slot()
    def update_connection_status(self,state : SocketState):
        if state == SocketState.ConnectedState:
            self.ui.trafficlight.setPixmap(QPixmap(GREENLIGHT))
        elif state == SocketState.UnconnectedState:
            self.ui.trafficlight.setPixmap(QPixmap(REDLIGHT))
        else:
            self.ui.trafficlight.setPixmap(QPixmap(YELLOWLIGHT))


    @Slot(str)
    def update_hostname(self,text):
        self.HOSTNAME = text
        print(self.HOSTNAME)


    @Slot(str)
    def update_port(self,text):
        if text == "":
            self.PORT = 0
        else:
            self.PORT = int(text)

        print(self.PORT)

    @Slot(str)
    def update_size(self):
        size = int(self.ui.sizeText.toPlainText())
        self.socket.write(bytes("ConfigSize:{size}\n".format(size=size),'utf-8'))

    @Slot(Data)
    def get_waveform(self, waveform : Data) -> bytearray:
        y_data = self.socket.readLine()
        waveform.concat(y_data)
        if '\n' in bytes(y_data).decode("utf-8"): 
            waveform.confirm()

    @Slot()
    def send_waveform_query(self):
        self.socket.write(b"Test\n")
        print("Bytes Written")



# Single Channel
class Attena(Ui_AttenaUi):
    def __init__(self, parent: QObject | None = ...) -> None:
        super(Attena, self).__init__()
        self.gain = 0
        self.phase = 0
        self.offset = 0
        self.channel = 0
        self.mode = 0
        self.attenuation = 0
        self.activated = 0
        self.deactivated = 0
        self.config = dict()


    def setupUi(self,antennaUI):
        super(Attena,self).setupUi(self)
        self.gainComboBox.addItems([str(i) for i in GAIN])
        self.offsetComboBox.addItems([str(i) for i in ANGLE])
        self.phaseComboBox.addItems([str(i) for i in ANGLE])   
        self.gain = self.config['gain']
        self.phase = self.config['phase']
        self.offset = self.config['offset']
        self.mode = self.config['mode']
        self.gainComboBox.currentTextChanged(lambda text: self.update_gain(float(text)))
        self.offsetComboBox.currentTextChanged(lambda text: self.update_offset(float(text)))
        self.phaseComboBox.currentTextChanged(lambda text: self.update_phase(float(text)))
        
    
    def update_gain(self, gain:float)->None:
        self.gain = gain
        self.config['gain'] = self.gain
        
    def update_phase(self, phase:float)->None:
        self.phase = phase
        self.config['phase'] = self.phase
        
    def update_offset(self, offset):
        self.offset = offset
        self.config['offset'] = self.offset

    def convert_phase(phase, offset):            
        phase = phase - 127
        offset = offset - 127
        result = phase + offset

        if(result > 127):
            result = result - 128
        elif(result < 0):
            if(result == -128):
                result = result + 128
            elif(result > -128):
                result = result + 129
            else:
                result = result + 256

        return(result)

# 2x2 Channel as single basic unit patch of Antenna
class Patch(Ui_PatchUi):
    changedActivatedAntenna = Signal(list)
    def __init__(self, parent: QObject | None = ...) -> None:
        super(Patch,self).__init__()
        xv,yv = np.meshgrid([1,3],[1,3])
        self.index = np.dstack((xv.flatten(),yv.flatten())).squeeze() 
        self.keys = ["ul","ur","ll","lr"]
        self.array = dict()
        self.activatedAttena = []

        self.mouseEventFilter = MousePressEventFilter()
        self.installEventFilter(self.mouseEventFilter)
        for key in self.keys:
            self.array[key]= [Attena() for i in range(4)]
            for i in range(4):
                self.array[key][i].setupUi(self.array[key][i])
                self.array[key][i].setObjectName("attena {} CH{}".format(key,i+1))
                self.array[key][i].channelLabel.setText("Ch{}".format(i+1))

    def setup(self,*args):
        for i in range(4):
            self.array[i].setup(args[i])

    def get_attenas(self):
        return self.array
    
    def findClosetFromItems(self,items:list[any],point:any)->int:
        return np.argmin(np.linalg.norm(items-point,2,axis=1))
    
    
    def apply(self,phases):
        phases = self.parse(phases)
        for key,phase in zip(self.keys,phases):
            if any(key in word  for word in ["ll", "lr"]):
                antennas = counterclockwise_phasearray_index(self.array[key], 2)
            else:
                antennas = counterclockwise_phasearray_index(self.array[key], 0)
            for antenna,phase in zip(antennas,phase.flatten()):
                antenna.phaseComboBox.setCurrentIndex(self.findClosetFromItems(ANGLE,phase))

    # parsing phrase into patch configuration with offset
    def parse(self,phase):
        """
        Split phases into 4 2x2 patches
        -------------
        | x x | x x |
        | x x | x x |
        -------------
        | x x | x x |
        | x x | x x |
        -------------
        """
        return split_patches(phase,2,2)
        


class MousePressEventFilter(QObject):
    def eventFilter(self, object:QObject, event:QEvent)->None:
        # debug(event,object) 
        if event.type() == QEvent.Type.MouseButtonPress and "Patch" in object.objectName():

            p = event.position()
            (x,y)=p.x(),p.y()
            print(x,y)
            geom = object.property('geometry')
            (w,h) = np.array([geom.width(),geom.height()])/4
            xv,yv = np.meshgrid([1,3],[1,3])
            ps = np.dstack((xv.flatten(),yv.flatten())) 
            dist = np.sqrt(np.sum(np.power([x,y]-ps * [w,h],2) ,axis=2))
            print(object.objectName(),ps[dist < (w+h)/4].squeeze())
            antenna = object.array
            closest_point = ps[dist < (w+h)/4].squeeze()
            for idx,key in zip(object.index,object.keys):
                if np.any(closest_point) and sum(np.abs(idx - closest_point)) == 0:
                    object.activatedAntenna=antenna[key]
                    object.changedActivatedAntenna.emit(antenna[key])

            

        return super(MousePressEventFilter, self).eventFilter(object, event)
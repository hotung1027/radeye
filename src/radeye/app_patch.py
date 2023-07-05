import sys

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtNetwork import QTcpSocket,QAbstractSocket
from PySide6.QtCore import QFile, QIODevice, QThread, Signal, Slot, QObject,QEvent,QRect
from PySide6.QtGui import QIcon,QPixmap,QMouseEvent
from patch_ui import Ui_PatchUi
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_PatchUi()
        self.ui.setupUi(self)
    
        self.filter = MousePressEventFilter()
        self.installEventFilter(self.filter)

class MousePressEventFilter(QObject):
    def eventFilter(self, object:QObject, event:QEvent)->None:
        
        if event.type() == QEvent.Type.MouseButtonPress:

            p = event.position()
            (x,y)=p.x(),p.y()
    
            geom = object.property('geometry')
            (w,h) = np.array([geom.width(),geom.height()])/4
            xv,yv = np.meshgrid([1,3],[1,3])
            ps = np.dstack((xv.flatten(),yv.flatten())) 
            dist = np.sqrt(np.sum(np.power([x,y]-ps * [w,h],2) ,axis=2))

            

        return super(MousePressEventFilter, self).eventFilter(object, event)




if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()  
    window.show()





    sys.exit(app.exec())
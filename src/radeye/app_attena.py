import sys

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtNetwork import QTcpSocket,QAbstractSocket
from PySide6.QtCore import QFile, QIODevice, QThread, Signal, Slot, QObject
from PySide6.QtGui import QIcon,QPixmap
from attena_ui import Ui_Form
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()  
    window.show()





    sys.exit(app.exec())
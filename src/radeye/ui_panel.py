# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'paneldFjOTR.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QButtonGroup, QFrame, QLabel,
    QListView, QMainWindow, QMenuBar, QProgressBar,
    QPushButton, QSizePolicy, QStatusBar, QTabWidget,
    QTextEdit, QWidget)

from pyqtgraph import PlotWidget
# import trafficlight

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 626)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 801, 561))
        self.tabWidget.setLayoutDirection(Qt.LeftToRight)
        self.RxControl = QWidget()
        self.RxControl.setObjectName(u"RxControl")
        self.listView = QListView(self.RxControl)
        self.listView.setObjectName(u"listView")
        self.listView.setGeometry(QRect(0, 0, 131, 551))
        self.frame = QFrame(self.RxControl)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(130, 0, 671, 531))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.tabWidget.addTab(self.RxControl, "")
        self.RxPanel = QWidget()
        self.RxPanel.setObjectName(u"RxPanel")
        self.connectButton = QPushButton(self.RxPanel)
        self.connectButton.setObjectName(u"connectButton")
        self.connectButton.setGeometry(QRect(70, 120, 80, 23))
        self.addressText = QTextEdit(self.RxPanel)
        self.addressText.setObjectName(u"addressText")
        self.addressText.setGeometry(QRect(70, 60, 151, 21))
        self.portText = QTextEdit(self.RxPanel)
        self.portText.setObjectName(u"portText")
        self.portText.setGeometry(QRect(70, 90, 151, 21))
        self.addressLabel = QLabel(self.RxPanel)
        self.addressLabel.setObjectName(u"addressLabel")
        self.addressLabel.setGeometry(QRect(0, 60, 71, 16))
        self.portLabel = QLabel(self.RxPanel)
        self.portLabel.setObjectName(u"portLabel")
        self.portLabel.setGeometry(QRect(0, 90, 61, 16))
        self.processView = PlotWidget(self.RxPanel)
        self.processView.setObjectName(u"processView")
        self.processView.setGeometry(QRect(240, 0, 561, 261))
        self.dataView = PlotWidget(self.RxPanel)
        self.dataView.setObjectName(u"dataView")
        self.dataView.setGeometry(QRect(240, 260, 561, 271))
        self.singleButton = QPushButton(self.RxPanel)
        self.buttonGroup = QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.singleButton)
        self.singleButton.setObjectName(u"singleButton")
        self.singleButton.setGeometry(QRect(120, 160, 80, 22))
        self.singleButton.setCheckable(True)
        self.runButton = QPushButton(self.RxPanel)
        self.buttonGroup.addButton(self.runButton)
        self.runButton.setObjectName(u"runButton")
        self.runButton.setGeometry(QRect(20, 160, 80, 22))
        self.runButton.setCheckable(True)
        self.runButton.setFlat(False)
        self.stopButton = QPushButton(self.RxPanel)
        self.buttonGroup.addButton(self.stopButton)
        self.stopButton.setObjectName(u"stopButton")
        self.stopButton.setGeometry(QRect(70, 200, 80, 22))
        self.stopButton.setCheckable(True)
        self.stopButton.setChecked(True)
        self.applyButton = QPushButton(self.RxPanel)
        self.applyButton.setObjectName(u"applyButton")
        self.applyButton.setGeometry(QRect(80, 370, 80, 22))
        self.applyButton.setCheckable(False)
        self.applyButton.setChecked(False)
        self.trafficlight = QLabel(self.RxPanel)
        self.trafficlight.setObjectName(u"trafficlight")
        self.trafficlight.setGeometry(QRect(0, 0, 31, 51))
        self.trafficlight.setScaledContents(True)
        self.sizeLabel = QLabel(self.RxPanel)
        self.sizeLabel.setObjectName(u"sizeLabel")
        self.sizeLabel.setGeometry(QRect(0, 300, 61, 16))
        self.sampleRateLabel = QLabel(self.RxPanel)
        self.sampleRateLabel.setObjectName(u"sampleRateLabel")
        self.sampleRateLabel.setGeometry(QRect(0, 340, 71, 16))
        self.sizeText = QTextEdit(self.RxPanel)
        self.sizeText.setObjectName(u"sizeText")
        self.sizeText.setGeometry(QRect(80, 300, 151, 21))
        self.sampleRateText = QTextEdit(self.RxPanel)
        self.sampleRateText.setObjectName(u"sampleRateText")
        self.sampleRateText.setGeometry(QRect(80, 340, 151, 21))
        self.tabWidget.addTab(self.RxPanel, "")
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(680, 560, 118, 23))
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(False)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.RxControl), QCoreApplication.translate("MainWindow", u"Rx Control", None))
        self.connectButton.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.addressText.setPlaceholderText(QCoreApplication.translate("MainWindow", u"192.168.1.10", None))
        self.portText.setPlaceholderText(QCoreApplication.translate("MainWindow", u"7", None))
        self.addressLabel.setText(QCoreApplication.translate("MainWindow", u"IP Address:", None))
        self.portLabel.setText(QCoreApplication.translate("MainWindow", u"Port:", None))
        self.singleButton.setText(QCoreApplication.translate("MainWindow", u"SINGLE", None))
        self.runButton.setText(QCoreApplication.translate("MainWindow", u"RUN", None))
        self.stopButton.setText(QCoreApplication.translate("MainWindow", u"STOP", None))
        self.trafficlight.setText("")
        self.sizeLabel.setText(QCoreApplication.translate("MainWindow", u"Size:", None))
        self.sampleRateLabel.setText(QCoreApplication.translate("MainWindow", u"SampleRate:", None))
        self.sizeText.setPlaceholderText(QCoreApplication.translate("MainWindow", u"5000", None))
        self.sampleRateText.setPlaceholderText(QCoreApplication.translate("MainWindow", u"250", None))
        self.applyButton.setText(QCoreApplication.translate("MainWindow", u"APPLY", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.RxPanel), QCoreApplication.translate("MainWindow", u"Display", None))
    # retranslateUi


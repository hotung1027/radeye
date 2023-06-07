# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'panel.ui'
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTabWidget, QTextEdit, QVBoxLayout,
    QWidget)

from pyqtgraph import PlotWidget
import radeye.trafficlight_rc
import radeye.attena_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(612, 548)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.centralWidget.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy1)
        self.gridLayout_6 = QGridLayout(self.centralWidget)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.tabWidget = QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setLayoutDirection(Qt.LeftToRight)
        self.RxPanel = QWidget()
        self.RxPanel.setObjectName(u"RxPanel")
        self.gridLayout_3 = QGridLayout(self.RxPanel)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.frame_2 = QFrame(self.RxPanel)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy2)
        self.frame_2.setMinimumSize(QSize(250, 325))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.trafficlight = QLabel(self.frame_2)
        self.trafficlight.setObjectName(u"trafficlight")
        self.trafficlight.setGeometry(QRect(0, 0, 31, 51))
        self.trafficlight.setPixmap(QPixmap(u":/resources/icons/trafficlight/redlight.png"))
        self.trafficlight.setScaledContents(True)
        self.addressLabel = QLabel(self.frame_2)
        self.addressLabel.setObjectName(u"addressLabel")
        self.addressLabel.setGeometry(QRect(10, 50, 71, 16))
        self.addressText = QTextEdit(self.frame_2)
        self.addressText.setObjectName(u"addressText")
        self.addressText.setGeometry(QRect(80, 50, 151, 21))
        self.portLabel = QLabel(self.frame_2)
        self.portLabel.setObjectName(u"portLabel")
        self.portLabel.setGeometry(QRect(10, 70, 61, 16))
        self.portText = QTextEdit(self.frame_2)
        self.portText.setObjectName(u"portText")
        self.portText.setGeometry(QRect(80, 70, 151, 21))
        self.connectButton = QPushButton(self.frame_2)
        self.connectButton.setObjectName(u"connectButton")
        self.connectButton.setGeometry(QRect(80, 100, 80, 23))
        self.runButton = QPushButton(self.frame_2)
        self.buttonGroup = QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.runButton)
        self.runButton.setObjectName(u"runButton")
        self.runButton.setGeometry(QRect(20, 130, 80, 22))
        self.runButton.setCheckable(True)
        self.runButton.setFlat(False)
        self.singleButton = QPushButton(self.frame_2)
        self.buttonGroup.addButton(self.singleButton)
        self.singleButton.setObjectName(u"singleButton")
        self.singleButton.setGeometry(QRect(110, 130, 80, 22))
        self.singleButton.setCheckable(True)
        self.stopButton = QPushButton(self.frame_2)
        self.buttonGroup.addButton(self.stopButton)
        self.stopButton.setObjectName(u"stopButton")
        self.stopButton.setGeometry(QRect(70, 160, 80, 22))
        self.stopButton.setCheckable(True)
        self.stopButton.setChecked(True)
        self.sizeLabel = QLabel(self.frame_2)
        self.sizeLabel.setObjectName(u"sizeLabel")
        self.sizeLabel.setGeometry(QRect(10, 210, 61, 16))
        self.sizeText = QTextEdit(self.frame_2)
        self.sizeText.setObjectName(u"sizeText")
        self.sizeText.setGeometry(QRect(90, 210, 151, 21))
        self.sampleRateLabel = QLabel(self.frame_2)
        self.sampleRateLabel.setObjectName(u"sampleRateLabel")
        self.sampleRateLabel.setGeometry(QRect(10, 250, 81, 16))
        self.sampleRateText = QTextEdit(self.frame_2)
        self.sampleRateText.setObjectName(u"sampleRateText")
        self.sampleRateText.setGeometry(QRect(90, 250, 151, 21))
        self.applyButton = QPushButton(self.frame_2)
        self.applyButton.setObjectName(u"applyButton")
        self.applyButton.setGeometry(QRect(70, 280, 80, 22))
        self.applyButton.setCheckable(False)
        self.applyButton.setChecked(False)

        self.horizontalLayout_4.addWidget(self.frame_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.dataView = PlotWidget(self.RxPanel)
        self.dataView.setObjectName(u"dataView")

        self.verticalLayout.addWidget(self.dataView)

        self.processView = PlotWidget(self.RxPanel)
        self.processView.setObjectName(u"processView")

        self.verticalLayout.addWidget(self.processView)


        self.horizontalLayout_4.addLayout(self.verticalLayout)


        self.gridLayout_3.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)

        self.tabWidget.addTab(self.RxPanel, "")
        self.RxControl = QWidget()
        self.RxControl.setObjectName(u"RxControl")
        self.horizontalLayout_2 = QHBoxLayout(self.RxControl)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame = QFrame(self.RxControl)
        self.frame.setObjectName(u"frame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy3)
        self.frame.setMinimumSize(QSize(300, 100))
        self.frame.setMaximumSize(QSize(166655, 166655))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.rowsLineEdit = QLineEdit(self.frame)
        self.rowsLineEdit.setObjectName(u"rowsLineEdit")
        self.rowsLineEdit.setGeometry(QRect(60, 40, 81, 22))
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 57, 14))
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(160, 20, 57, 14))
        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 40, 57, 14))
        self.label_6 = QLabel(self.frame)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(160, 40, 57, 14))
        self.columnsLineEdit = QLineEdit(self.frame)
        self.columnsLineEdit.setObjectName(u"columnsLineEdit")
        self.columnsLineEdit.setGeometry(QRect(220, 40, 81, 22))
        self.thetaComboBox = QComboBox(self.frame)
        self.thetaComboBox.setObjectName(u"thetaComboBox")
        self.thetaComboBox.setGeometry(QRect(60, 10, 81, 21))
        self.phiComboBox = QComboBox(self.frame)
        self.phiComboBox.setObjectName(u"phiComboBox")
        self.phiComboBox.setGeometry(QRect(220, 10, 81, 21))

        self.verticalLayout_2.addWidget(self.frame)

        self.frame_3 = QFrame(self.RxControl)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_3)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_2.addWidget(self.frame_3)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.frame_4 = QFrame(self.RxControl)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout.addWidget(self.frame_4)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.tabWidget.addTab(self.RxControl, "")
        self.Control = QWidget()
        self.Control.setObjectName(u"Control")
        self.horizontalLayout_3 = QHBoxLayout(self.Control)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.frame_5 = QFrame(self.Control)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)

        self.gridLayout_4.addWidget(self.frame_5, 0, 0, 1, 1)


        self.horizontalLayout_3.addLayout(self.gridLayout_4)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.frame_6 = QFrame(self.Control)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)

        self.gridLayout_5.addWidget(self.frame_6, 0, 0, 1, 1)


        self.horizontalLayout_3.addLayout(self.gridLayout_5)

        self.tabWidget.addTab(self.Control, "")

        self.gridLayout_6.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralWidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 612, 19))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.trafficlight.setText("")
        self.addressLabel.setText(QCoreApplication.translate("MainWindow", u"IP Address:", None))
        self.addressText.setPlaceholderText(QCoreApplication.translate("MainWindow", u"192.168.1.10", None))
        self.portLabel.setText(QCoreApplication.translate("MainWindow", u"Port:", None))
        self.portText.setPlaceholderText(QCoreApplication.translate("MainWindow", u"7", None))
        self.connectButton.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.runButton.setText(QCoreApplication.translate("MainWindow", u"RUN", None))
        self.singleButton.setText(QCoreApplication.translate("MainWindow", u"SINGLE", None))
        self.stopButton.setText(QCoreApplication.translate("MainWindow", u"STOP", None))
        self.sizeLabel.setText(QCoreApplication.translate("MainWindow", u"Size:", None))
        self.sizeText.setPlaceholderText(QCoreApplication.translate("MainWindow", u"5000", None))
        self.sampleRateLabel.setText(QCoreApplication.translate("MainWindow", u"SampleRate:", None))
        self.sampleRateText.setPlaceholderText(QCoreApplication.translate("MainWindow", u"250", None))
        self.applyButton.setText(QCoreApplication.translate("MainWindow", u"APPLY", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.RxPanel), QCoreApplication.translate("MainWindow", u"Display", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"theta", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"phi", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"rows", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"columns", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.RxControl), QCoreApplication.translate("MainWindow", u"Rx Control", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Control), QCoreApplication.translate("MainWindow", u"Control", None))
    # retranslateUi


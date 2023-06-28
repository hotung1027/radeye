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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QComboBox, QDoubleSpinBox,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QRadioButton, QSizePolicy, QSlider,
    QSpacerItem, QSpinBox, QStatusBar, QTabWidget,
    QVBoxLayout, QWidget)

from pyqtgraph import PlotWidget
import radeye.trafficlight_rc
import radeye.attena_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1087, 640)
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
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy2)
        self.frame_2.setMinimumSize(QSize(250, 325))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.frame_7 = QFrame(self.frame_2)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(60, 0))
        self.frame_7.setMaximumSize(QSize(1677215, 16777215))
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_7)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.trafficlight = QLabel(self.frame_7)
        self.trafficlight.setObjectName(u"trafficlight")
        self.trafficlight.setMinimumSize(QSize(35, 55))
        self.trafficlight.setMaximumSize(QSize(35, 55))
        self.trafficlight.setPixmap(QPixmap(u":/resources/icons/trafficlight/redlight.png"))
        self.trafficlight.setScaledContents(True)

        self.verticalLayout_4.addWidget(self.trafficlight)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)


        self.horizontalLayout_7.addWidget(self.frame_7)

        self.groupBox = QGroupBox(self.frame_2)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy3)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.addressLabel = QLabel(self.groupBox)
        self.addressLabel.setObjectName(u"addressLabel")

        self.horizontalLayout_5.addWidget(self.addressLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.addressText = QLineEdit(self.groupBox)
        self.addressText.setObjectName(u"addressText")

        self.horizontalLayout_5.addWidget(self.addressText)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.portLabel = QLabel(self.groupBox)
        self.portLabel.setObjectName(u"portLabel")

        self.horizontalLayout_6.addWidget(self.portLabel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)

        self.portText = QLineEdit(self.groupBox)
        self.portText.setObjectName(u"portText")

        self.horizontalLayout_6.addWidget(self.portText)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_3)

        self.connectButton = QPushButton(self.groupBox)
        self.connectButton.setObjectName(u"connectButton")

        self.horizontalLayout_8.addWidget(self.connectButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)


        self.horizontalLayout_7.addWidget(self.groupBox)


        self.verticalLayout_7.addLayout(self.horizontalLayout_7)

        self.groupBox_2 = QGroupBox(self.frame_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy3.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy3)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.runButton = QPushButton(self.groupBox_2)
        self.buttonGroup = QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.runButton)
        self.runButton.setObjectName(u"runButton")
        self.runButton.setMinimumSize(QSize(80, 0))
        self.runButton.setCheckable(True)
        self.runButton.setFlat(False)

        self.horizontalLayout_9.addWidget(self.runButton)

        self.singleButton = QPushButton(self.groupBox_2)
        self.buttonGroup.addButton(self.singleButton)
        self.singleButton.setObjectName(u"singleButton")
        self.singleButton.setMinimumSize(QSize(80, 0))
        self.singleButton.setCheckable(True)

        self.horizontalLayout_9.addWidget(self.singleButton)


        self.verticalLayout_5.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_5)

        self.stopButton = QPushButton(self.groupBox_2)
        self.buttonGroup.addButton(self.stopButton)
        self.stopButton.setObjectName(u"stopButton")
        self.stopButton.setMinimumSize(QSize(80, 0))
        self.stopButton.setCheckable(True)
        self.stopButton.setChecked(True)

        self.horizontalLayout_10.addWidget(self.stopButton)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_6)


        self.verticalLayout_5.addLayout(self.horizontalLayout_10)


        self.verticalLayout_7.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.frame_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy3.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy3)
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.sizeLabel = QLabel(self.groupBox_3)
        self.sizeLabel.setObjectName(u"sizeLabel")

        self.horizontalLayout_11.addWidget(self.sizeLabel)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_7)

        self.sizeText = QLineEdit(self.groupBox_3)
        self.sizeText.setObjectName(u"sizeText")

        self.horizontalLayout_11.addWidget(self.sizeText)


        self.verticalLayout_6.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.sampleRateLabel = QLabel(self.groupBox_3)
        self.sampleRateLabel.setObjectName(u"sampleRateLabel")

        self.horizontalLayout_12.addWidget(self.sampleRateLabel)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_8)

        self.sampleRateText = QLineEdit(self.groupBox_3)
        self.sampleRateText.setObjectName(u"sampleRateText")

        self.horizontalLayout_12.addWidget(self.sampleRateText)


        self.verticalLayout_6.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.groupBox_3)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.horizontalSpacer_24 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_24)

        self.bandWidthText = QLineEdit(self.groupBox_3)
        self.bandWidthText.setObjectName(u"bandWidthText")

        self.horizontalLayout_2.addWidget(self.bandWidthText)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.label_2 = QLabel(self.groupBox_3)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_30.addWidget(self.label_2)

        self.horizontalSpacer_25 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_30.addItem(self.horizontalSpacer_25)

        self.pulseWidthText = QLineEdit(self.groupBox_3)
        self.pulseWidthText.setObjectName(u"pulseWidthText")

        self.horizontalLayout_30.addWidget(self.pulseWidthText)


        self.verticalLayout_6.addLayout(self.horizontalLayout_30)


        self.verticalLayout_7.addWidget(self.groupBox_3)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_2)


        self.horizontalLayout_4.addWidget(self.frame_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.processView = PlotWidget(self.RxPanel)
        self.processView.setObjectName(u"processView")

        self.verticalLayout.addWidget(self.processView)

        self.dataView = PlotWidget(self.RxPanel)
        self.dataView.setObjectName(u"dataView")

        self.verticalLayout.addWidget(self.dataView)


        self.horizontalLayout_4.addLayout(self.verticalLayout)

        self.horizontalLayout_4.setStretch(1, 1)

        self.gridLayout_3.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)

        self.tabWidget.addTab(self.RxPanel, "")
        self.PhaseArray = QWidget()
        self.PhaseArray.setObjectName(u"PhaseArray")
        self.phaseArrayLayout = QHBoxLayout(self.PhaseArray)
        self.phaseArrayLayout.setObjectName(u"phaseArrayLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame = QFrame(self.PhaseArray)
        self.frame.setObjectName(u"frame")
        sizePolicy2.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy2)
        self.frame.setMinimumSize(QSize(300, 100))
        self.frame.setMaximumSize(QSize(166655, 166655))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_28 = QHBoxLayout(self.frame)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.gb_arrayconfig = QGroupBox(self.frame)
        self.gb_arrayconfig.setObjectName(u"gb_arrayconfig")
        sizePolicy3.setHeightForWidth(self.gb_arrayconfig.sizePolicy().hasHeightForWidth())
        self.gb_arrayconfig.setSizePolicy(sizePolicy3)
        self.gb_arrayconfig.setSizeIncrement(QSize(0, 0))
        self.arrayConfigLayout = QVBoxLayout(self.gb_arrayconfig)
        self.arrayConfigLayout.setObjectName(u"arrayConfigLayout")
        self.gb_horizontal = QGroupBox(self.gb_arrayconfig)
        self.gb_horizontal.setObjectName(u"gb_horizontal")
        sizePolicy3.setHeightForWidth(self.gb_horizontal.sizePolicy().hasHeightForWidth())
        self.gb_horizontal.setSizePolicy(sizePolicy3)
        self.gb_horizontal.setFlat(False)
        self.verticalLayout_10 = QVBoxLayout(self.gb_horizontal)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_sizex = QLabel(self.gb_horizontal)
        self.label_sizex.setObjectName(u"label_sizex")

        self.horizontalLayout_13.addWidget(self.label_sizex)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_9)

        self.sb_sizex = QSpinBox(self.gb_horizontal)
        self.sb_sizex.setObjectName(u"sb_sizex")
        self.sb_sizex.setMinimumSize(QSize(0, 20))
        self.sb_sizex.setMinimum(1)
        self.sb_sizex.setMaximum(1024)
        self.sb_sizex.setValue(64)

        self.horizontalLayout_13.addWidget(self.sb_sizex)


        self.verticalLayout_10.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_spacingx = QLabel(self.gb_horizontal)
        self.label_spacingx.setObjectName(u"label_spacingx")

        self.horizontalLayout_14.addWidget(self.label_spacingx)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_10)

        self.dsb_spacingx = QDoubleSpinBox(self.gb_horizontal)
        self.dsb_spacingx.setObjectName(u"dsb_spacingx")
        self.dsb_spacingx.setMinimumSize(QSize(0, 20))
        self.dsb_spacingx.setDecimals(3)
        self.dsb_spacingx.setMinimum(0.001000000000000)
        self.dsb_spacingx.setMaximum(10.000000000000000)
        self.dsb_spacingx.setSingleStep(0.001000000000000)

        self.horizontalLayout_14.addWidget(self.dsb_spacingx)


        self.verticalLayout_10.addLayout(self.horizontalLayout_14)

        self.line_5 = QFrame(self.gb_horizontal)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_10.addWidget(self.line_5)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_windowx = QLabel(self.gb_horizontal)
        self.label_windowx.setObjectName(u"label_windowx")

        self.horizontalLayout_15.addWidget(self.label_windowx)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_11)

        self.cb_windowx = QComboBox(self.gb_horizontal)
        self.cb_windowx.setObjectName(u"cb_windowx")

        self.horizontalLayout_15.addWidget(self.cb_windowx)


        self.verticalLayout_10.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_sidelobex = QLabel(self.gb_horizontal)
        self.label_sidelobex.setObjectName(u"label_sidelobex")

        self.horizontalLayout_20.addWidget(self.label_sidelobex)

        self.horizontalSpacer_12 = QSpacerItem(40, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_12)

        self.sb_sidelobex = QSpinBox(self.gb_horizontal)
        self.sb_sidelobex.setObjectName(u"sb_sidelobex")
        self.sb_sidelobex.setMinimumSize(QSize(0, 20))
        self.sb_sidelobex.setMinimum(10)
        self.sb_sidelobex.setMaximum(100)
        self.sb_sidelobex.setValue(60)

        self.horizontalLayout_20.addWidget(self.sb_sidelobex)


        self.verticalLayout_10.addLayout(self.horizontalLayout_20)

        self.hs_sidelobex = QSlider(self.gb_horizontal)
        self.hs_sidelobex.setObjectName(u"hs_sidelobex")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.hs_sidelobex.sizePolicy().hasHeightForWidth())
        self.hs_sidelobex.setSizePolicy(sizePolicy4)
        self.hs_sidelobex.setMinimum(10)
        self.hs_sidelobex.setMaximum(100)
        self.hs_sidelobex.setValue(60)
        self.hs_sidelobex.setOrientation(Qt.Horizontal)
        self.hs_sidelobex.setTickPosition(QSlider.TicksAbove)

        self.verticalLayout_10.addWidget(self.hs_sidelobex)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.label_adjsidelobex = QLabel(self.gb_horizontal)
        self.label_adjsidelobex.setObjectName(u"label_adjsidelobex")

        self.horizontalLayout_21.addWidget(self.label_adjsidelobex)

        self.horizontalSpacer_13 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_13)

        self.sb_adjsidelobex = QSpinBox(self.gb_horizontal)
        self.sb_adjsidelobex.setObjectName(u"sb_adjsidelobex")
        self.sb_adjsidelobex.setMinimumSize(QSize(0, 20))
        self.sb_adjsidelobex.setMinimum(2)
        self.sb_adjsidelobex.setMaximum(100)
        self.sb_adjsidelobex.setValue(20)

        self.horizontalLayout_21.addWidget(self.sb_adjsidelobex)


        self.verticalLayout_10.addLayout(self.horizontalLayout_21)

        self.hs_adjsidelobex = QSlider(self.gb_horizontal)
        self.hs_adjsidelobex.setObjectName(u"hs_adjsidelobex")
        sizePolicy4.setHeightForWidth(self.hs_adjsidelobex.sizePolicy().hasHeightForWidth())
        self.hs_adjsidelobex.setSizePolicy(sizePolicy4)
        self.hs_adjsidelobex.setMinimum(2)
        self.hs_adjsidelobex.setMaximum(100)
        self.hs_adjsidelobex.setValue(20)
        self.hs_adjsidelobex.setOrientation(Qt.Horizontal)
        self.hs_adjsidelobex.setTickPosition(QSlider.TicksAbove)

        self.verticalLayout_10.addWidget(self.hs_adjsidelobex)


        self.arrayConfigLayout.addWidget(self.gb_horizontal)

        self.gb_vertical = QGroupBox(self.gb_arrayconfig)
        self.gb_vertical.setObjectName(u"gb_vertical")
        sizePolicy3.setHeightForWidth(self.gb_vertical.sizePolicy().hasHeightForWidth())
        self.gb_vertical.setSizePolicy(sizePolicy3)
        self.gb_vertical.setFlat(False)
        self.verticalLayout_11 = QVBoxLayout(self.gb_vertical)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_sizey = QLabel(self.gb_vertical)
        self.label_sizey.setObjectName(u"label_sizey")

        self.horizontalLayout_16.addWidget(self.label_sizey)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_14)

        self.sb_sizey = QSpinBox(self.gb_vertical)
        self.sb_sizey.setObjectName(u"sb_sizey")
        self.sb_sizey.setMinimumSize(QSize(0, 20))
        self.sb_sizey.setMinimum(1)
        self.sb_sizey.setMaximum(1024)
        self.sb_sizey.setValue(64)

        self.horizontalLayout_16.addWidget(self.sb_sizey)


        self.verticalLayout_11.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_spacingy = QLabel(self.gb_vertical)
        self.label_spacingy.setObjectName(u"label_spacingy")

        self.horizontalLayout_17.addWidget(self.label_spacingy)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_15)

        self.dsb_spacingy = QDoubleSpinBox(self.gb_vertical)
        self.dsb_spacingy.setObjectName(u"dsb_spacingy")
        self.dsb_spacingy.setMinimumSize(QSize(0, 20))
        self.dsb_spacingy.setDecimals(3)
        self.dsb_spacingy.setMinimum(0.001000000000000)
        self.dsb_spacingy.setMaximum(10.000000000000000)
        self.dsb_spacingy.setSingleStep(0.001000000000000)
        self.dsb_spacingy.setValue(0.001000000000000)

        self.horizontalLayout_17.addWidget(self.dsb_spacingy)


        self.verticalLayout_11.addLayout(self.horizontalLayout_17)

        self.line_6 = QFrame(self.gb_vertical)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_11.addWidget(self.line_6)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_windowy = QLabel(self.gb_vertical)
        self.label_windowy.setObjectName(u"label_windowy")

        self.horizontalLayout_19.addWidget(self.label_windowy)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_16)

        self.cb_windowy = QComboBox(self.gb_vertical)
        self.cb_windowy.setObjectName(u"cb_windowy")

        self.horizontalLayout_19.addWidget(self.cb_windowy)


        self.verticalLayout_11.addLayout(self.horizontalLayout_19)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.label_sidelobey = QLabel(self.gb_vertical)
        self.label_sidelobey.setObjectName(u"label_sidelobey")

        self.horizontalLayout_22.addWidget(self.label_sidelobey)

        self.horizontalSpacer_17 = QSpacerItem(40, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_22.addItem(self.horizontalSpacer_17)

        self.sb_sidelobey = QSpinBox(self.gb_vertical)
        self.sb_sidelobey.setObjectName(u"sb_sidelobey")
        self.sb_sidelobey.setMinimumSize(QSize(0, 20))
        self.sb_sidelobey.setMinimum(10)
        self.sb_sidelobey.setMaximum(100)
        self.sb_sidelobey.setValue(60)

        self.horizontalLayout_22.addWidget(self.sb_sidelobey)


        self.verticalLayout_11.addLayout(self.horizontalLayout_22)

        self.hs_sidelobey = QSlider(self.gb_vertical)
        self.hs_sidelobey.setObjectName(u"hs_sidelobey")
        sizePolicy4.setHeightForWidth(self.hs_sidelobey.sizePolicy().hasHeightForWidth())
        self.hs_sidelobey.setSizePolicy(sizePolicy4)
        self.hs_sidelobey.setMinimum(10)
        self.hs_sidelobey.setMaximum(100)
        self.hs_sidelobey.setValue(60)
        self.hs_sidelobey.setOrientation(Qt.Horizontal)
        self.hs_sidelobey.setTickPosition(QSlider.TicksAbove)

        self.verticalLayout_11.addWidget(self.hs_sidelobey)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.label_adjsidelobey = QLabel(self.gb_vertical)
        self.label_adjsidelobey.setObjectName(u"label_adjsidelobey")

        self.horizontalLayout_23.addWidget(self.label_adjsidelobey)

        self.horizontalSpacer_18 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_18)

        self.sb_adjsidelobey = QSpinBox(self.gb_vertical)
        self.sb_adjsidelobey.setObjectName(u"sb_adjsidelobey")
        self.sb_adjsidelobey.setMinimumSize(QSize(0, 20))
        self.sb_adjsidelobey.setMinimum(2)
        self.sb_adjsidelobey.setMaximum(100)
        self.sb_adjsidelobey.setValue(20)

        self.horizontalLayout_23.addWidget(self.sb_adjsidelobey)


        self.verticalLayout_11.addLayout(self.horizontalLayout_23)

        self.hs_adjsidelobey = QSlider(self.gb_vertical)
        self.hs_adjsidelobey.setObjectName(u"hs_adjsidelobey")
        sizePolicy4.setHeightForWidth(self.hs_adjsidelobey.sizePolicy().hasHeightForWidth())
        self.hs_adjsidelobey.setSizePolicy(sizePolicy4)
        self.hs_adjsidelobey.setMinimum(2)
        self.hs_adjsidelobey.setMaximum(100)
        self.hs_adjsidelobey.setValue(20)
        self.hs_adjsidelobey.setOrientation(Qt.Horizontal)
        self.hs_adjsidelobey.setTickPosition(QSlider.TicksAbove)

        self.verticalLayout_11.addWidget(self.hs_adjsidelobey)


        self.arrayConfigLayout.addWidget(self.gb_vertical)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.arrayConfigLayout.addItem(self.verticalSpacer_3)


        self.verticalLayout_8.addWidget(self.gb_arrayconfig)


        self.horizontalLayout_28.addLayout(self.verticalLayout_8)

        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.gb_plotconfig = QGroupBox(self.frame)
        self.gb_plotconfig.setObjectName(u"gb_plotconfig")
        sizePolicy3.setHeightForWidth(self.gb_plotconfig.sizePolicy().hasHeightForWidth())
        self.gb_plotconfig.setSizePolicy(sizePolicy3)
        self.gb_plotconfig.setSizeIncrement(QSize(0, 0))
        self.plotConfigLayout = QVBoxLayout(self.gb_plotconfig)
        self.plotConfigLayout.setObjectName(u"plotConfigLayout")
        self.gb_steering = QGroupBox(self.gb_plotconfig)
        self.gb_steering.setObjectName(u"gb_steering")
        sizePolicy3.setHeightForWidth(self.gb_steering.sizePolicy().hasHeightForWidth())
        self.gb_steering.setSizePolicy(sizePolicy3)
        self.gb_steering.setFlat(False)
        self.verticalLayout_14 = QVBoxLayout(self.gb_steering)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_angleaz = QLabel(self.gb_steering)
        self.label_angleaz.setObjectName(u"label_angleaz")

        self.horizontalLayout_18.addWidget(self.label_angleaz)

        self.horizontalSpacer_19 = QSpacerItem(50, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_19)

        self.dsb_angleaz = QDoubleSpinBox(self.gb_steering)
        self.dsb_angleaz.setObjectName(u"dsb_angleaz")
        self.dsb_angleaz.setMinimumSize(QSize(0, 20))
        self.dsb_angleaz.setMinimum(-90.000000000000000)
        self.dsb_angleaz.setMaximum(90.000000000000000)

        self.horizontalLayout_18.addWidget(self.dsb_angleaz)


        self.verticalLayout_14.addLayout(self.horizontalLayout_18)

        self.hs_angleaz = QSlider(self.gb_steering)
        self.hs_angleaz.setObjectName(u"hs_angleaz")
        sizePolicy4.setHeightForWidth(self.hs_angleaz.sizePolicy().hasHeightForWidth())
        self.hs_angleaz.setSizePolicy(sizePolicy4)
        self.hs_angleaz.setMinimum(-900)
        self.hs_angleaz.setMaximum(900)
        self.hs_angleaz.setSingleStep(10)
        self.hs_angleaz.setOrientation(Qt.Horizontal)
        self.hs_angleaz.setTickPosition(QSlider.TicksAbove)
        self.hs_angleaz.setTickInterval(100)

        self.verticalLayout_14.addWidget(self.hs_angleaz)

        self.line_2 = QFrame(self.gb_steering)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_14.addWidget(self.line_2)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.label_angleel = QLabel(self.gb_steering)
        self.label_angleel.setObjectName(u"label_angleel")

        self.horizontalLayout_24.addWidget(self.label_angleel)

        self.horizontalSpacer_20 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_24.addItem(self.horizontalSpacer_20)

        self.dsb_angleel = QDoubleSpinBox(self.gb_steering)
        self.dsb_angleel.setObjectName(u"dsb_angleel")
        self.dsb_angleel.setMinimumSize(QSize(0, 20))
        self.dsb_angleel.setMinimum(-90.000000000000000)
        self.dsb_angleel.setMaximum(90.000000000000000)

        self.horizontalLayout_24.addWidget(self.dsb_angleel)


        self.verticalLayout_14.addLayout(self.horizontalLayout_24)

        self.hs_angleel = QSlider(self.gb_steering)
        self.hs_angleel.setObjectName(u"hs_angleel")
        sizePolicy4.setHeightForWidth(self.hs_angleel.sizePolicy().hasHeightForWidth())
        self.hs_angleel.setSizePolicy(sizePolicy4)
        self.hs_angleel.setMinimum(-900)
        self.hs_angleel.setMaximum(900)
        self.hs_angleel.setSingleStep(10)
        self.hs_angleel.setOrientation(Qt.Horizontal)
        self.hs_angleel.setTickPosition(QSlider.TicksAbove)
        self.hs_angleel.setTickInterval(100)

        self.verticalLayout_14.addWidget(self.hs_angleel)


        self.plotConfigLayout.addWidget(self.gb_steering)

        self.polarGroupBox = QGroupBox(self.gb_plotconfig)
        self.polarGroupBox.setObjectName(u"polarGroupBox")
        self.gridLayout_2 = QGridLayout(self.polarGroupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.polardirection = QComboBox(self.polarGroupBox)
        self.polardirection.setObjectName(u"polardirection")

        self.gridLayout_2.addWidget(self.polardirection, 0, 0, 1, 1)


        self.plotConfigLayout.addWidget(self.polarGroupBox)

        self.gb_plot = QGroupBox(self.gb_plotconfig)
        self.gb_plot.setObjectName(u"gb_plot")
        sizePolicy3.setHeightForWidth(self.gb_plot.sizePolicy().hasHeightForWidth())
        self.gb_plot.setSizePolicy(sizePolicy3)
        self.gb_plot.setFlat(False)
        self.verticalLayout_15 = QVBoxLayout(self.gb_plot)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.cb_plottype = QComboBox(self.gb_plot)
        self.cb_plottype.setObjectName(u"cb_plottype")
        sizePolicy4.setHeightForWidth(self.cb_plottype.sizePolicy().hasHeightForWidth())
        self.cb_plottype.setSizePolicy(sizePolicy4)

        self.verticalLayout_15.addWidget(self.cb_plottype)

        self.line = QFrame(self.gb_plot)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_15.addWidget(self.line)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.rb_azimuth = QRadioButton(self.gb_plot)
        self.rb_azimuth.setObjectName(u"rb_azimuth")
        self.rb_azimuth.setChecked(False)

        self.horizontalLayout_25.addWidget(self.rb_azimuth)

        self.horizontalSpacer_21 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_21)

        self.rbsb_azimuth = QDoubleSpinBox(self.gb_plot)
        self.rbsb_azimuth.setObjectName(u"rbsb_azimuth")
        self.rbsb_azimuth.setMinimumSize(QSize(0, 20))
        self.rbsb_azimuth.setMinimum(-90.000000000000000)
        self.rbsb_azimuth.setMaximum(90.000000000000000)

        self.horizontalLayout_25.addWidget(self.rbsb_azimuth)


        self.verticalLayout_15.addLayout(self.horizontalLayout_25)

        self.rbhs_azimuth = QSlider(self.gb_plot)
        self.rbhs_azimuth.setObjectName(u"rbhs_azimuth")
        self.rbhs_azimuth.setMinimum(-900)
        self.rbhs_azimuth.setMaximum(900)
        self.rbhs_azimuth.setSingleStep(10)
        self.rbhs_azimuth.setOrientation(Qt.Horizontal)
        self.rbhs_azimuth.setTickPosition(QSlider.TicksAbove)
        self.rbhs_azimuth.setTickInterval(100)

        self.verticalLayout_15.addWidget(self.rbhs_azimuth)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.rb_elevation = QRadioButton(self.gb_plot)
        self.rb_elevation.setObjectName(u"rb_elevation")
        self.rb_elevation.setChecked(True)

        self.horizontalLayout_26.addWidget(self.rb_elevation)

        self.horizontalSpacer_22 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_26.addItem(self.horizontalSpacer_22)

        self.rbsb_elevation = QDoubleSpinBox(self.gb_plot)
        self.rbsb_elevation.setObjectName(u"rbsb_elevation")
        self.rbsb_elevation.setEnabled(True)
        self.rbsb_elevation.setMinimumSize(QSize(0, 20))
        self.rbsb_elevation.setMinimum(-90.000000000000000)
        self.rbsb_elevation.setMaximum(90.000000000000000)

        self.horizontalLayout_26.addWidget(self.rbsb_elevation)


        self.verticalLayout_15.addLayout(self.horizontalLayout_26)

        self.rbhs_elevation = QSlider(self.gb_plot)
        self.rbhs_elevation.setObjectName(u"rbhs_elevation")
        self.rbhs_elevation.setEnabled(True)
        self.rbhs_elevation.setMinimum(-900)
        self.rbhs_elevation.setMaximum(900)
        self.rbhs_elevation.setSingleStep(10)
        self.rbhs_elevation.setOrientation(Qt.Horizontal)
        self.rbhs_elevation.setTickPosition(QSlider.TicksAbove)
        self.rbhs_elevation.setTickInterval(100)

        self.verticalLayout_15.addWidget(self.rbhs_elevation)

        self.line_polar = QFrame(self.gb_plot)
        self.line_polar.setObjectName(u"line_polar")
        self.line_polar.setFrameShape(QFrame.HLine)
        self.line_polar.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_15.addWidget(self.line_polar)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.label_polarMinAmp = QLabel(self.gb_plot)
        self.label_polarMinAmp.setObjectName(u"label_polarMinAmp")
        self.label_polarMinAmp.setFrameShape(QFrame.NoFrame)

        self.horizontalLayout_27.addWidget(self.label_polarMinAmp)

        self.horizontalSpacer_23 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_27.addItem(self.horizontalSpacer_23)

        self.spinBox_polarMinAmp = QSpinBox(self.gb_plot)
        self.spinBox_polarMinAmp.setObjectName(u"spinBox_polarMinAmp")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.spinBox_polarMinAmp.sizePolicy().hasHeightForWidth())
        self.spinBox_polarMinAmp.setSizePolicy(sizePolicy5)
        self.spinBox_polarMinAmp.setMinimumSize(QSize(0, 20))
        self.spinBox_polarMinAmp.setMinimum(-120)
        self.spinBox_polarMinAmp.setMaximum(-10)
        self.spinBox_polarMinAmp.setValue(-60)

        self.horizontalLayout_27.addWidget(self.spinBox_polarMinAmp)


        self.verticalLayout_15.addLayout(self.horizontalLayout_27)

        self.horizontalSlider_polarMinAmp = QSlider(self.gb_plot)
        self.horizontalSlider_polarMinAmp.setObjectName(u"horizontalSlider_polarMinAmp")
        self.horizontalSlider_polarMinAmp.setMinimum(-120)
        self.horizontalSlider_polarMinAmp.setMaximum(-10)
        self.horizontalSlider_polarMinAmp.setValue(-60)
        self.horizontalSlider_polarMinAmp.setOrientation(Qt.Horizontal)
        self.horizontalSlider_polarMinAmp.setTickPosition(QSlider.TicksAbove)

        self.verticalLayout_15.addWidget(self.horizontalSlider_polarMinAmp)


        self.plotConfigLayout.addWidget(self.gb_plot)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.plotConfigLayout.addItem(self.verticalSpacer_4)


        self.verticalLayout_12.addWidget(self.gb_plotconfig)


        self.horizontalLayout_28.addLayout(self.verticalLayout_12)


        self.verticalLayout_2.addWidget(self.frame)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.frame_4 = QFrame(self.PhaseArray)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.groupBox_4 = QGroupBox(self.frame_4)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.visualizeLayout = QVBoxLayout(self.groupBox_4)
        self.visualizeLayout.setObjectName(u"visualizeLayout")
        self.layout_canvas = QVBoxLayout()
        self.layout_canvas.setObjectName(u"layout_canvas")

        self.visualizeLayout.addLayout(self.layout_canvas)


        self.gridLayout.addWidget(self.groupBox_4, 0, 0, 1, 1)


        self.horizontalLayout.addWidget(self.frame_4)

        self.horizontalLayout.setStretch(1, 1)

        self.phaseArrayLayout.addLayout(self.horizontalLayout)

        self.tabWidget.addTab(self.PhaseArray, "")
        self.BeamformingConfig = QWidget()
        self.BeamformingConfig.setObjectName(u"BeamformingConfig")
        self.horizontalLayout_3 = QHBoxLayout(self.BeamformingConfig)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.channelGroupBox = QGroupBox(self.BeamformingConfig)
        self.channelGroupBox.setObjectName(u"channelGroupBox")
        self.channelConfGrid = QGridLayout(self.channelGroupBox)
        self.channelConfGrid.setObjectName(u"channelConfGrid")
        self.groupBox_5 = QGroupBox(self.channelGroupBox)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.comPortSelect = QComboBox(self.groupBox_5)
        self.comPortSelect.setObjectName(u"comPortSelect")

        self.verticalLayout_9.addWidget(self.comPortSelect)

        self.findComPortButton = QPushButton(self.groupBox_5)
        self.findComPortButton.setObjectName(u"findComPortButton")

        self.verticalLayout_9.addWidget(self.findComPortButton)

        self.led = QPushButton(self.groupBox_5)
        self.led.setObjectName(u"led")

        self.verticalLayout_9.addWidget(self.led)


        self.channelConfGrid.addWidget(self.groupBox_5, 0, 0, 1, 1)

        self.groupBox_6 = QGroupBox(self.channelGroupBox)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.channelGrid = QGridLayout(self.groupBox_6)
        self.channelGrid.setObjectName(u"channelGrid")

        self.channelConfGrid.addWidget(self.groupBox_6, 1, 0, 1, 1)

        self.channelConfGrid.setRowStretch(1, 1)

        self.horizontalLayout_3.addWidget(self.channelGroupBox)

        self.panelGroupBox = QGroupBox(self.BeamformingConfig)
        self.panelGroupBox.setObjectName(u"panelGroupBox")
        self.panelGrid = QGridLayout(self.panelGroupBox)
        self.panelGrid.setObjectName(u"panelGrid")

        self.horizontalLayout_3.addWidget(self.panelGroupBox)

        self.horizontalLayout_3.setStretch(1, 1)
        self.tabWidget.addTab(self.BeamformingConfig, "")

        self.gridLayout_6.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralWidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1087, 22))
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
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Connection", None))
        self.addressLabel.setText(QCoreApplication.translate("MainWindow", u"IP Address:", None))
        self.addressText.setText(QCoreApplication.translate("MainWindow", u"192.168.1.10", None))
        self.portLabel.setText(QCoreApplication.translate("MainWindow", u"Port:", None))
        self.portText.setText(QCoreApplication.translate("MainWindow", u"7", None))
        self.connectButton.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Control", None))
        self.runButton.setText(QCoreApplication.translate("MainWindow", u"RUN", None))
        self.singleButton.setText(QCoreApplication.translate("MainWindow", u"SINGLE", None))
        self.stopButton.setText(QCoreApplication.translate("MainWindow", u"STOP", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Data Accuqsistion Config", None))
        self.sizeLabel.setText(QCoreApplication.translate("MainWindow", u"Size:", None))
        self.sizeText.setText(QCoreApplication.translate("MainWindow", u"5000", None))
        self.sampleRateLabel.setText(QCoreApplication.translate("MainWindow", u"SampleRate:", None))
        self.sampleRateText.setText(QCoreApplication.translate("MainWindow", u"250M", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"BandWidth:", None))
        self.bandWidthText.setText(QCoreApplication.translate("MainWindow", u"250M", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"PulseWidth:", None))
        self.pulseWidthText.setText(QCoreApplication.translate("MainWindow", u"20u", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.RxPanel), QCoreApplication.translate("MainWindow", u"Display", None))
        self.gb_arrayconfig.setTitle(QCoreApplication.translate("MainWindow", u"Array Config", None))
        self.gb_horizontal.setTitle(QCoreApplication.translate("MainWindow", u"Horizontal - x", None))
        self.label_sizex.setText(QCoreApplication.translate("MainWindow", u"Size:", None))
        self.label_spacingx.setText(QCoreApplication.translate("MainWindow", u"Spacing (\u03bb):", None))
        self.label_windowx.setText(QCoreApplication.translate("MainWindow", u"Window:", None))
        self.label_sidelobex.setText(QCoreApplication.translate("MainWindow", u"Side lobe (dB):", None))
        self.label_adjsidelobex.setText(QCoreApplication.translate("MainWindow", u"Adjacent sidelobes:", None))
        self.gb_vertical.setTitle(QCoreApplication.translate("MainWindow", u"Vertical - y", None))
        self.label_sizey.setText(QCoreApplication.translate("MainWindow", u"Size:", None))
        self.label_spacingy.setText(QCoreApplication.translate("MainWindow", u"Spacing (\u03bb):", None))
        self.label_windowy.setText(QCoreApplication.translate("MainWindow", u"Window:", None))
        self.label_sidelobey.setText(QCoreApplication.translate("MainWindow", u"Side lobe (dB):", None))
        self.label_adjsidelobey.setText(QCoreApplication.translate("MainWindow", u"Adjacent sidelobes:", None))
        self.gb_plotconfig.setTitle(QCoreApplication.translate("MainWindow", u"Beam Config", None))
        self.gb_steering.setTitle(QCoreApplication.translate("MainWindow", u"Steering", None))
        self.label_angleaz.setText(QCoreApplication.translate("MainWindow", u"Azimuth (\u00b0):", None))
        self.label_angleel.setText(QCoreApplication.translate("MainWindow", u"Elevation (\u00b0):", None))
        self.polarGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Polarization", None))
        self.gb_plot.setTitle(QCoreApplication.translate("MainWindow", u"Plot", None))
        self.rb_azimuth.setText(QCoreApplication.translate("MainWindow", u"Azimuth plane (\u00b0):", None))
        self.rb_elevation.setText(QCoreApplication.translate("MainWindow", u"Elevation plane (\u00b0):", None))
        self.label_polarMinAmp.setText(QCoreApplication.translate("MainWindow", u"Min amplitude (dB): ", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Visualize", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.PhaseArray), QCoreApplication.translate("MainWindow", u"PhaseArray", None))
        self.channelGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Channel Config", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Comm Port", None))
        self.findComPortButton.setText(QCoreApplication.translate("MainWindow", u"find port", None))
        self.led.setText(QCoreApplication.translate("MainWindow", u"led", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"ChannelPanel", None))
        self.panelGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"PhaseArrayPanel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.BeamformingConfig), QCoreApplication.translate("MainWindow", u"BeamformingConfig", None))
    # retranslateUi


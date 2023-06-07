# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'attena.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QLabel,
    QSizePolicy, QWidget)

class Ui_AttenaUi(QWidget):
    def setupUi(self, AttenaUi):
        if not AttenaUi.objectName():
            AttenaUi.setObjectName(u"AttenaUi")
        AttenaUi.resize(120, 143)
        AttenaUi.setMinimumSize(QSize(120, 143))
        self.phaseLabel = QLabel(AttenaUi)
        self.phaseLabel.setObjectName(u"phaseLabel")
        self.phaseLabel.setGeometry(QRect(0, 20, 57, 14))
        self.offsetLabel = QLabel(AttenaUi)
        self.offsetLabel.setObjectName(u"offsetLabel")
        self.offsetLabel.setGeometry(QRect(0, 50, 57, 14))
        self.gainLabel = QLabel(AttenaUi)
        self.gainLabel.setObjectName(u"gainLabel")
        self.gainLabel.setGeometry(QRect(0, 80, 57, 14))
        self.attenCheckBox = QCheckBox(AttenaUi)
        self.attenCheckBox.setObjectName(u"attenCheckBox")
        self.attenCheckBox.setGeometry(QRect(0, 100, 85, 20))
        self.txrxCheckBox = QCheckBox(AttenaUi)
        self.txrxCheckBox.setObjectName(u"txrxCheckBox")
        self.txrxCheckBox.setGeometry(QRect(60, 100, 85, 20))
        self.channelLabel = QLabel(AttenaUi)
        self.channelLabel.setObjectName(u"channelLabel")
        self.channelLabel.setGeometry(QRect(40, 0, 31, 16))
        self.phaseComboBox = QComboBox(AttenaUi)
        self.phaseComboBox.setObjectName(u"phaseComboBox")
        self.phaseComboBox.setGeometry(QRect(40, 20, 79, 22))
        self.phaseComboBox.setEditable(True)
        self.offsetComboBox = QComboBox(AttenaUi)
        self.offsetComboBox.setObjectName(u"offsetComboBox")
        self.offsetComboBox.setGeometry(QRect(40, 50, 79, 22))
        self.offsetComboBox.setEditable(True)
        self.gainComboBox = QComboBox(AttenaUi)
        self.gainComboBox.setObjectName(u"gainComboBox")
        self.gainComboBox.setGeometry(QRect(40, 80, 79, 22))
        self.gainComboBox.setEditable(True)
        self.gainInfo = QLabel(AttenaUi)
        self.gainInfo.setObjectName(u"gainInfo")
        self.gainInfo.setGeometry(QRect(0, 120, 57, 14))
        self.phaseInfo = QLabel(AttenaUi)
        self.phaseInfo.setObjectName(u"phaseInfo")
        self.phaseInfo.setGeometry(QRect(60, 120, 57, 14))

        self.retranslateUi(AttenaUi)

        QMetaObject.connectSlotsByName(AttenaUi)
    # setupUi

    def retranslateUi(self, AttenaUi):
        AttenaUi.setWindowTitle(QCoreApplication.translate("AttenaUi", u"Channel", None))
        self.phaseLabel.setText(QCoreApplication.translate("AttenaUi", u"Phase", None))
        self.offsetLabel.setText(QCoreApplication.translate("AttenaUi", u"Offset", None))
        self.gainLabel.setText(QCoreApplication.translate("AttenaUi", u"Gain", None))
        self.attenCheckBox.setText(QCoreApplication.translate("AttenaUi", u"Atten", None))
        self.txrxCheckBox.setText(QCoreApplication.translate("AttenaUi", u"RX", None))
        self.channelLabel.setText(QCoreApplication.translate("AttenaUi", u"Ch1", None))
        self.gainInfo.setText(QCoreApplication.translate("AttenaUi", u"Gain", None))
        self.phaseInfo.setText(QCoreApplication.translate("AttenaUi", u"phase", None))
    # retranslateUi


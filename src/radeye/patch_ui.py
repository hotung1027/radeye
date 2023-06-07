# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'patch.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QSizePolicy,
    QWidget)
import radeye.attena_rc

class Ui_PatchUi(QWidget):
    def setupUi(self, PatchUi):
        if not PatchUi.objectName():
            PatchUi.setObjectName(u"PatchUi")
        PatchUi.resize(553, 403)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PatchUi.sizePolicy().hasHeightForWidth())
        PatchUi.setSizePolicy(sizePolicy)
        PatchUi.setMouseTracking(True)
        PatchUi.setAutoFillBackground(True)
        PatchUi.setStyleSheet(u"QFrame{\n"
"border-image: url(:/resources/indicator/Preview - Bottom.png);\n"
"}\n"
"")
        self.gridLayout_2 = QGridLayout(PatchUi)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(PatchUi)
        self.frame.setObjectName(u"frame")
        self.frame.setAutoFillBackground(False)
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Plain)

        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(PatchUi)

        QMetaObject.connectSlotsByName(PatchUi)
    # setupUi

    def retranslateUi(self, PatchUi):
        PatchUi.setWindowTitle(QCoreApplication.translate("PatchUi", u"Patch", None))
    # retranslateUi


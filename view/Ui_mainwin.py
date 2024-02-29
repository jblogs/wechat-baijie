# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwin.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QStatusBar, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_theMainWindow(object):
    def setupUi(self, theMainWindow):
        if not theMainWindow.objectName():
            theMainWindow.setObjectName(u"theMainWindow")
        theMainWindow.resize(464, 390)
        icon = QIcon()
        icon.addFile(u"../resource/teamwork.ico", QSize(), QIcon.Normal, QIcon.Off)
        theMainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(theMainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 10, 441, 356))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.verticalLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.pushButton_webc = QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_webc.setObjectName(u"pushButton_webc")

        self.horizontalLayout_2.addWidget(self.pushButton_webc)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.line = QFrame(self.verticalLayoutWidget_2)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.label = QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.lineEdit_fcsv = QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_fcsv.setObjectName(u"lineEdit_fcsv")

        self.verticalLayout_2.addWidget(self.lineEdit_fcsv)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit_tag = QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_tag.setObjectName(u"lineEdit_tag")
        self.lineEdit_tag.setEnabled(False)

        self.horizontalLayout.addWidget(self.lineEdit_tag)

        self.checkBox_usetag = QCheckBox(self.verticalLayoutWidget_2)
        self.checkBox_usetag.setObjectName(u"checkBox_usetag")

        self.horizontalLayout.addWidget(self.checkBox_usetag)

        self.pushButton_fetchfs = QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_fetchfs.setObjectName(u"pushButton_fetchfs")

        self.horizontalLayout.addWidget(self.pushButton_fetchfs)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.line_2 = QFrame(self.verticalLayoutWidget_2)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineEdit_tgtcsv = QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_tgtcsv.setObjectName(u"lineEdit_tgtcsv")

        self.gridLayout.addWidget(self.lineEdit_tgtcsv, 0, 0, 1, 1)

        self.pushButton_seltgtcsv = QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_seltgtcsv.setObjectName(u"pushButton_seltgtcsv")

        self.gridLayout.addWidget(self.pushButton_seltgtcsv, 0, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.label_2 = QLabel(self.verticalLayoutWidget_2)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.textEdit_msg = QTextEdit(self.verticalLayoutWidget_2)
        self.textEdit_msg.setObjectName(u"textEdit_msg")

        self.verticalLayout_2.addWidget(self.textEdit_msg)

        self.pushButton_wlog = QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_wlog.setObjectName(u"pushButton_wlog")

        self.verticalLayout_2.addWidget(self.pushButton_wlog)

        self.pushButton_sendout = QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_sendout.setObjectName(u"pushButton_sendout")

        self.verticalLayout_2.addWidget(self.pushButton_sendout)

        self.line_3 = QFrame(self.verticalLayoutWidget_2)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_3)

        self.pushButton_stop = QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_stop.setObjectName(u"pushButton_stop")

        self.verticalLayout_2.addWidget(self.pushButton_stop)

        theMainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(theMainWindow)
        self.statusbar.setObjectName(u"statusbar")
        theMainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(theMainWindow)

        QMetaObject.connectSlotsByName(theMainWindow)
    # setupUi

    def retranslateUi(self, theMainWindow):
        theMainWindow.setWindowTitle(QCoreApplication.translate("theMainWindow", u"\u5fae\u4fe1\u62dc\u8282\u5229\u5668\u3010jblogs@github\u3011", None))
        self.label_3.setText(QCoreApplication.translate("theMainWindow", u"\u8bf7\u5148\u6253\u5f00Windows\u7248\u5fae\u4fe1\uff0c\u786e\u4fdd\u5df2\u767b\u5f55...", None))
        self.pushButton_webc.setText(QCoreApplication.translate("theMainWindow", u"\u68c0\u67e5\u5fae\u4fe1\u7a0b\u5e8f\u72b6\u6001", None))
        self.label.setText(QCoreApplication.translate("theMainWindow", u"\u8f93\u5165\u7528\u6765\u5b58\u653e\u6293\u53d6\u8054\u7cfb\u4eba\u7684\u6587\u4ef6\u540d\uff1a", None))
        self.lineEdit_fcsv.setPlaceholderText(QCoreApplication.translate("theMainWindow", u"friends[%Y%m%d-%H%M%S].csv", None))
        self.lineEdit_tag.setPlaceholderText(QCoreApplication.translate("theMainWindow", u"\u65e0\u6807\u7b7e", None))
        self.checkBox_usetag.setText(QCoreApplication.translate("theMainWindow", u"\u6807\u7b7e\u8fc7\u6ee4", None))
        self.pushButton_fetchfs.setText(QCoreApplication.translate("theMainWindow", u"\u4ece\u5fae\u4fe1\u6293\u53d6\u8054\u7cfb\u4eba", None))
        self.lineEdit_tgtcsv.setPlaceholderText(QCoreApplication.translate("theMainWindow", u"friends.csv", None))
        self.pushButton_seltgtcsv.setText(QCoreApplication.translate("theMainWindow", u"\u9009\u53d6\u53d1\u9001\u8ba1\u5212\u6587\u4ef6", None))
        self.label_2.setText(QCoreApplication.translate("theMainWindow", u"\u8f93\u5165\u95ee\u5019\u6d88\u606f\uff0c\u5982\u6709\u201c {\u79f0\u8c13}\u3001{\u656c\u8bed} \u201d\u5c06\u4f1a\u88abcsv\u4e2d\u7684\u914d\u7f6e\u66ff\u4ee3\uff1a", None))
        self.textEdit_msg.setPlaceholderText("")
        self.pushButton_wlog.setText(QCoreApplication.translate("theMainWindow", u"\u53ea\u70b9\u4e0d\u53d1\uff0c\u64cd\u4f5c\u5199\u5165\u65e5\u5fd7", None))
        self.pushButton_sendout.setText(QCoreApplication.translate("theMainWindow", u"\u6b63\u5f0f\u53d1\u9001", None))
        self.pushButton_stop.setText(QCoreApplication.translate("theMainWindow", u"\u505c\u6b62\u81ea\u52a8\u64cd\u4f5c", None))
    # retranslateUi


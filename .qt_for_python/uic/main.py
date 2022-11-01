# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGroupBox, QHBoxLayout,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPushButton, QRadioButton, QSizePolicy, QStatusBar,
    QTextBrowser, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(937, 692)
        self.action = QAction(MainWindow)
        self.action.setObjectName(u"action")
        self.action_2 = QAction(MainWindow)
        self.action_2.setObjectName(u"action_2")
        self.action_3 = QAction(MainWindow)
        self.action_3.setObjectName(u"action_3")
        self.action_4 = QAction(MainWindow)
        self.action_4.setObjectName(u"action_4")
        self.action_5 = QAction(MainWindow)
        self.action_5.setObjectName(u"action_5")
        self.action_6 = QAction(MainWindow)
        self.action_6.setObjectName(u"action_6")
        self.action_7 = QAction(MainWindow)
        self.action_7.setObjectName(u"action_7")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(200, 30, 561, 71))
        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(250, 190, 631, 441))
        font = QFont()
        font.setFamilies([u"Agency FB"])
        font.setPointSize(10)
        self.groupBox_4.setFont(font)
        self.txt_arm = QTextBrowser(self.groupBox_4)
        self.txt_arm.setObjectName(u"txt_arm")
        self.txt_arm.setGeometry(QRect(340, 40, 271, 341))
        self.label_2 = QLabel(self.groupBox_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(110, 400, 81, 16))
        self.label_3 = QLabel(self.groupBox_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(420, 400, 111, 16))
        self.line = QFrame(self.groupBox_4)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(310, 10, 20, 431))
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.label_image = QLabel(self.groupBox_4)
        self.label_image.setObjectName(u"label_image")
        self.label_image.setGeometry(QRect(30, 40, 271, 341))
        self.label_image.setPixmap(QPixmap(u"UIImage/White.png"))
        self.btn_display = QPushButton(self.groupBox_4)
        self.btn_display.setObjectName(u"btn_display")
        self.btn_display.setGeometry(QRect(30, 400, 75, 23))
        self.btn_armrun = QPushButton(self.groupBox_4)
        self.btn_armrun.setObjectName(u"btn_armrun")
        self.btn_armrun.setGeometry(QRect(530, 400, 75, 23))
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(50, 190, 182, 441))
        self.verticalLayout_4 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.groupBox = QGroupBox(self.layoutWidget)
        self.groupBox.setObjectName(u"groupBox")
        font1 = QFont()
        font1.setFamilies([u"Agency FB"])
        font1.setPointSize(10)
        font1.setBold(False)
        self.groupBox.setFont(font1)
        self.groupBox.setFlat(False)
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.btn_arm = QPushButton(self.groupBox)
        self.btn_arm.setObjectName(u"btn_arm")

        self.horizontalLayout.addWidget(self.btn_arm)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btn_network = QPushButton(self.groupBox)
        self.btn_network.setObjectName(u"btn_network")

        self.horizontalLayout_2.addWidget(self.btn_network)

        self.brn_users = QPushButton(self.groupBox)
        self.brn_users.setObjectName(u"brn_users")

        self.horizontalLayout_2.addWidget(self.brn_users)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)


        self.verticalLayout_4.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.layoutWidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFont(font)
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btn_plasma = QRadioButton(self.groupBox_2)
        self.btn_plasma.setObjectName(u"btn_plasma")

        self.verticalLayout.addWidget(self.btn_plasma)

        self.btn_RBCs = QRadioButton(self.groupBox_2)
        self.btn_RBCs.setObjectName(u"btn_RBCs")

        self.verticalLayout.addWidget(self.btn_RBCs)

        self.btn_Buffy = QRadioButton(self.groupBox_2)
        self.btn_Buffy.setObjectName(u"btn_Buffy")

        self.verticalLayout.addWidget(self.btn_Buffy)


        self.horizontalLayout_4.addLayout(self.verticalLayout)


        self.verticalLayout_4.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.layoutWidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setFont(font)
        self.horizontalLayout_5 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.btn_run = QPushButton(self.groupBox_3)
        self.btn_run.setObjectName(u"btn_run")

        self.verticalLayout_3.addWidget(self.btn_run)

        self.btn_stop = QPushButton(self.groupBox_3)
        self.btn_stop.setObjectName(u"btn_stop")

        self.verticalLayout_3.addWidget(self.btn_stop)

        self.btn_exit = QPushButton(self.groupBox_3)
        self.btn_exit.setObjectName(u"btn_exit")

        self.verticalLayout_3.addWidget(self.btn_exit)


        self.horizontalLayout_5.addLayout(self.verticalLayout_3)


        self.verticalLayout_4.addWidget(self.groupBox_3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 937, 22))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_2)
        self.menu.addAction(self.action_3)
        self.menu.addAction(self.action_4)
        self.menu_2.addAction(self.action_5)
        self.menu_2.addAction(self.action_6)
        self.menu_2.addAction(self.action_7)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u7cfb\u7edf", None))
        self.action.setText(QCoreApplication.translate("MainWindow", u"\u76f8\u673a\u8bbe\u7f6e", None))
        self.action_2.setText(QCoreApplication.translate("MainWindow", u"\u673a\u68b0\u81c2\u8bbe\u7f6e", None))
        self.action_3.setText(QCoreApplication.translate("MainWindow", u"\u7f51\u7edc\u8bbe\u7f6e", None))
        self.action_4.setText(QCoreApplication.translate("MainWindow", u"\u7528\u6237\u7ba1\u7406", None))
        self.action_5.setText(QCoreApplication.translate("MainWindow", u"\u542f\u52a8", None))
        self.action_6.setText(QCoreApplication.translate("MainWindow", u"\u505c\u6b62", None))
        self.action_7.setText(QCoreApplication.translate("MainWindow", u"\u9000\u51fa", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:26pt; font-weight:600;\">\u7cfb\u7edf</span></p></body></html>", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"\u4e3b\u754c\u9762", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u5206\u5272\u6548\u679c\u56fe</p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u673a\u68b0\u81c2\u8fd0\u884c\u8fc7\u7a0b</p></body></html>", None))
        self.label_image.setText("")
        self.btn_display.setText(QCoreApplication.translate("MainWindow", u"\u5c55\u793a", None))
        self.btn_armrun.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u884c", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u7cfb\u7edf\u8bbe\u7f6e", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u76f8\u673a\u8bbe\u7f6e", None))
        self.btn_arm.setText(QCoreApplication.translate("MainWindow", u"\u673a\u68b0\u81c2\u8bbe\u7f6e", None))
        self.btn_network.setText(QCoreApplication.translate("MainWindow", u"\u7f51\u7edc\u8bbe\u7f6e", None))
        self.brn_users.setText(QCoreApplication.translate("MainWindow", u"\u7528\u6237\u7ba1\u7406", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u79fb\u6db2\u7c7b\u578b", None))
        self.btn_plasma.setText(QCoreApplication.translate("MainWindow", u"\u8840\u6d46\u5206\u5272", None))
        self.btn_RBCs.setText(QCoreApplication.translate("MainWindow", u"\u7ea2\u7ec6\u80de\u5206\u5272", None))
        self.btn_Buffy.setText(QCoreApplication.translate("MainWindow", u"\u767d\u7ec6\u80de\u548c\u8840\u5c0f\u677f\u5206\u5272", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\u7cfb\u7edf\u64cd\u4f5c", None))
        self.btn_run.setText(QCoreApplication.translate("MainWindow", u"\u542f\u52a8", None))
        self.btn_stop.setText(QCoreApplication.translate("MainWindow", u"\u505c\u6b62", None))
        self.btn_exit.setText(QCoreApplication.translate("MainWindow", u"\u9000\u51fa", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\u64cd\u4f5c", None))
    # retranslateUi


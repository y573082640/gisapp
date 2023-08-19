# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_login.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(837, 494)
        MainWindow.setStyleSheet("QPushButton:pressed{padding-top:5px;padding-left:5px;}\n"
"\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 50, 301, 351))
        self.label.setStyleSheet("border-image: url(:/image/images/电子地图.png);\n"
"background-color: rgb(168, 168, 168);\n"
"border-top-left-radius:30px;\n"
"border-bottom-left-radius:30px;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(360, 50, 441, 351))
        self.label_2.setStyleSheet("background-color: rgb(239, 239, 239);\n"
"border-top-right-radius:30px;\n"
"border-bottom-right-radius:30px")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(380, 100, 391, 281))
        self.tabWidget.setStyleSheet("/*border:none;\n"
"background-color: rgb(248, 233, 213);*/\n"
"QTabWidget{color: rgb(0, 0, 0);background-color: rgb(248, 233, 213);}\n"
"\n"
"\n"
"QTabBar::tab:unselected\n"
"{\n"
"    color:rgb(18, 18, 18);\n"
"    /*background:transparent;*/\n"
"    width:60px;\n"
"    \n"
"    font-family:\"微软雅黑\";\n"
"    font-size:14px;\n"
"    border-bottom:2px solid rgb(220, 220, 220);\n"
"\n"
"}\n"
"\n"
"QTabBar::tab:selected\n"
"{\n"
"    color:rgb(255, 170, 0);\n"
"    width:60px;\n"
"    /*background:transparent;*/\n"
"    \n"
"    font-family:\"微软雅黑\";\n"
"    font-size:20px;\n"
"    border-bottom:4px solid rgb(188, 125, 0);\n"
"\n"
"}\n"
"QTabBar::tab{min-width:80px}")
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_2.setGeometry(QtCore.QRect(40, 40, 311, 41))
        self.lineEdit_2.setStyleSheet("border:none;\n"
"border-bottom:2px solid rgb(0, 0, 0);\n"
"border-radius:8px;\n"
"\n"
"")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_3.setGeometry(QtCore.QRect(40, 100, 311, 41))
        self.lineEdit_3.setStyleSheet("border:none;\n"
"border-bottom:2px solid rgb(0, 0, 0);\n"
"border-radius:8px;\n"
"\n"
"")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(40, 170, 311, 41))
        self.pushButton.setStyleSheet("#pushButton{\n"
"    background-color: rgb(0, 0, 0);\n"
"    color: rgb(255, 255, 255);\n"
"    font: 10pt \"黑体\";\n"
"    border:3px solid rgb(255, 255, 255);\n"
"    border-radius:7px;\n"
"}\n"
"#pushBotton:hover{\n"
"    \n"
"    background-color: rgb(255, 255, 255);\n"
"    \n"
"    color: rgb(0,0,0);\n"
"}\n"
"#pushBotton:pressed{\n"
"    padding-top:5px;\n"
"    padding-left:5px;\n"
"\n"
"}\n"
"")
        self.pushButton.setObjectName("pushButton")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_4.setGeometry(QtCore.QRect(40, 80, 311, 41))
        self.lineEdit_4.setStyleSheet("border:none;\n"
"border-bottom:2px solid rgb(0, 0, 0);\n"
"border-radius:8px;\n"
"")
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 190, 311, 41))
        self.pushButton_2.setStyleSheet("#pushButton_2{\n"
"    background-color: rgb(0, 0, 0);\n"
"    color: rgb(255, 255, 255);\n"
"    font: 10pt \"黑体\";\n"
"    border:3px solid rgb(255, 255, 255);\n"
"    border-radius:7px;\n"
"}\n"
"#pushBotton_2:hover{\n"
"    \n"
"    background-color: rgb(255, 255, 255);\n"
"    \n"
"    color: rgb(0,0,0);\n"
"}\n"
"#pushBotton_2:pressed{\n"
"    padding-top:5px;\n"
"    padding-left:5px;\n"
"\n"
"}\n"
"")
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_5.setGeometry(QtCore.QRect(40, 30, 311, 41))
        self.lineEdit_5.setStyleSheet("border:none;\n"
"border-bottom:2px solid rgb(0, 0, 0);\n"
"border-radius:8px;\n"
"")
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_6.setGeometry(QtCore.QRect(40, 130, 311, 41))
        self.lineEdit_6.setStyleSheet("border:none;\n"
"border-bottom:2px solid rgb(0, 0, 0);\n"
"border-radius:8px;\n"
"")
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.tabWidget.addTab(self.tab_2, "")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(750, 60, 21, 21))
        self.pushButton_3.setStyleSheet("border-image: url(:/image/images/叉叉.png);")
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 837, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        self.pushButton_3.clicked.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "用户名："))
        self.lineEdit_3.setPlaceholderText(_translate("MainWindow", "密码："))
        self.pushButton.setText(_translate("MainWindow", "登录"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "登录"))
        self.lineEdit_4.setPlaceholderText(_translate("MainWindow", "输入密码："))
        self.pushButton_2.setText(_translate("MainWindow", "注册"))
        self.lineEdit_5.setPlaceholderText(_translate("MainWindow", "创建用户名："))
        self.lineEdit_6.setPlaceholderText(_translate("MainWindow", "确认密码："))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "注册"))
import resourse_rc
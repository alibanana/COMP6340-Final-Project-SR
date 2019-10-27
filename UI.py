# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\Programming\Python Projects\COMP6340 - Final Project (SR)\UI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt, QThread

import VoiceRecognition as vr

class My_Thread(QThread):
    def run(self):
        vr.run()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(497, 179)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(280, 40, 191, 61))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 497, 21))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionAbout_Us = QtWidgets.QAction(MainWindow)
        self.actionAbout_Us.setObjectName("actionAbout_Us")
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionAbout_Us)
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        self.state = 0
        self.pushButton.clicked.connect(self.check_state)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Start / Stop"))
        self.menuHelp.setTitle(_translate("MainWindow", "Menu"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))
        self.actionAbout_Us.setText(_translate("MainWindow", "About Us"))

    def check_state(self):
        print(self.state)
        if self.state == 1:
            self.buttonstop()
        else:
            self.buttonclick()

    def buttonclick(self):
        self.thread = My_Thread()
        self.thread.start()
        self.state = 1

    def buttonstop(self):
        self.thread.quit()
        self.state = 0

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

import os
import sys
import keyboard
import speech_recognition as sr
import VoiceRecognition as vr
import win10toast
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import QThread

notification = win10toast.ToastNotifier()
r = sr.Recognizer()

def get_audio():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=2)
        notification.show_toast("SR", "Start talking:", threaded=True, duration=3)
        audio = r.listen(source)
        # audio = r.record(source, duration=4)
        try:
            text = r.recognize_google(audio, language="EN-US")
            # print("You Said: {}".format(text))
        except:
            return
    return text.lower()

# PyQT5 UI
class My_Thread(QThread):
    def __init__(self):
        super(My_Thread, self).__init__()
    def run(self):
        while True:
            keyboard.wait(hotkey="k + l")
            saidtext = get_audio()
            if saidtext == None:
                notification.show_toast("Error","Sorry could not recognize your voice", threaded=True, duration=3 )
            else:
                print("What you said: ", saidtext)
                vr.split_command(saidtext)

class command_thread(QThread):
    text = ''
    def __init__(self, text):
        super(command_thread, self).__init__()
        self.text = text
    def run(self):
        vr.split_command(self.text)
        self.exit()


class Ui_MainWindow(object):
    # global text
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(472, 179)
        # MainWindow.setWindowIcon()
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(270, 80, 191, 51))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 20, 251, 111))
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 0, 91, 16))
        self.label.setObjectName("label")
        self.runButton = QtWidgets.QPushButton(self.centralwidget)
        self.runButton.setGeometry(QtCore.QRect(270, 20, 191, 51))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.runButton.setFont(font)
        self.runButton.setObjectName("runButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 472, 21))
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
        self.runButton.clicked.connect(self.command)
        self.actionHelp.triggered.connect(self.help_clicked)
        self.actionAbout_Us.triggered.connect(self.about_us_clicked)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Voice Recognition"))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.label.setText(_translate("MainWindow", "Type a command"))
        self.runButton.setText(_translate("MainWindow", "Run Command"))
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
        self.pushButton.setText("Stop")
        self.state = 1

    def buttonstop(self):
        self.thread.terminate()
        self.pushButton.setText("Start")
        self.state = 0

    def command(self):
        self.text = self.textEdit.toPlainText()
        self.thread2 = command_thread(self.text)
        self.thread2.start()
        self.textEdit.setText("")

    def about_us_clicked(self):
        os.system('start https://voicerecognition.godaddysites.com/tentang-kami')

    def help_clicked(self):
        os.system('start https://voicerecognition.godaddysites.com/help')

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

if __name__ == '__main__':
    sys.exit(app.exec_())
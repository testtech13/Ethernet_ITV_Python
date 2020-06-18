
from PyQt5 import QtCore, QtGui, QtWidgets
import pyeip

hostname1 = "192.168.1.20"  #IP address of ITV 1
hostname2 = "192.168.1.21"  #IP address of ITV 2
hostname3 = "192.168.1.22"  #IP address of ITV 3
EIP_1 = pyeip.EtherNetIP(hostname1) 
EIP_2 = pyeip.EtherNetIP(hostname2) 
EIP_3 = pyeip.EtherNetIP(hostname3)
C_A = 1 #default network status is disconnected
C_B = 1 #default network status is disconnected
C_C = 1 #default network status is disconnected
high = 4095     # max/min count values
low = 0
value = low     # initial value state

# PyQt Designer generated code, DO NOT CHANGE!
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(720, 480)
        MainWindow.setMinimumSize(QtCore.QSize(720, 480))
        MainWindow.setMaximumSize(QtCore.QSize(720, 480))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_exit = QtWidgets.QPushButton(self.centralwidget)
        self.btn_exit.setGeometry(QtCore.QRect(610, 10, 101, 71))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.btn_exit.setFont(font)
        self.btn_exit.setObjectName("btn_exit")
        self.btn_OFF = QtWidgets.QPushButton(self.centralwidget)
        self.btn_OFF.setGeometry(QtCore.QRect(400, 250, 281, 161))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.btn_OFF.setFont(font)
        self.btn_OFF.setObjectName("btn_OFF")
        self.btn_ON = QtWidgets.QPushButton(self.centralwidget)
        self.btn_ON.setGeometry(QtCore.QRect(40, 250, 271, 161))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.btn_ON.setFont(font)
        self.btn_ON.setAutoFillBackground(False)
        self.btn_ON.setObjectName("btn_ON")
        self.label_ITV_B = QtWidgets.QCheckBox(self.centralwidget)
        self.label_ITV_B.setGeometry(QtCore.QRect(20, 90, 581, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(40)
        font.setKerning(True)
        self.label_ITV_B.setFont(font)
        self.label_ITV_B.setChecked(False)
        self.label_ITV_B.setObjectName("label_ITV_B")
        self.label_ITV_A = QtWidgets.QCheckBox(self.centralwidget)
        self.label_ITV_A.setGeometry(QtCore.QRect(20, 10, 571, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(40)
        font.setKerning(True)
        self.label_ITV_A.setFont(font)
        self.label_ITV_A.setChecked(False)
        self.label_ITV_A.setObjectName("label_ITV_A")
        self.label_ITV_C = QtWidgets.QCheckBox(self.centralwidget)
        self.label_ITV_C.setGeometry(QtCore.QRect(20, 170, 581, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(40)
        font.setKerning(True)
        self.label_ITV_C.setFont(font)
        self.label_ITV_C.setChecked(False)
        self.label_ITV_C.setObjectName("label_ITV_C")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 720, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # end PyQt generated code

        # Creating button functionalities, only updates when clicked
        self.btn_ON.clicked.connect(lambda:self.button_response(self.btn_ON))
        self.btn_OFF.clicked.connect(lambda:self.button_response(self.btn_OFF))
        self.btn_exit.clicked.connect(lambda:self.button_response(self.btn_exit))

        # 
        self.label_ITV_A.stateChanged.connect(lambda state, x=1:self.check_connection(self.label_ITV_A,x))
        self.label_ITV_B.stateChanged.connect(lambda state, x=2:self.check_connection(self.label_ITV_B,x))
        self.label_ITV_C.stateChanged.connect(lambda state, x=3:self.check_connection(self.label_ITV_C,x))

        # Update functionality:
        self.my_timer = QtCore.QTimer()
        self.my_timer.timeout.connect(self.update_status)   #call the update_status function every one second
        self.my_timer.start(1000) #sets update interval

    # Additional PyQt generated code (same rules)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_exit.setText(_translate("MainWindow", "Quit"))
        self.btn_OFF.setText(_translate("MainWindow", "LOW"))
        self.btn_ON.setText(_translate("MainWindow", "HIGH"))
        self.label_ITV_B.setText(_translate("MainWindow", " ITV 2 (psi): "))
        self.label_ITV_A.setText(_translate("MainWindow", " ITV 1 (psi): "))
        self.label_ITV_C.setText(_translate("MainWindow", " ITV 3 (psi): "))
        # end PyQt generated code

    def button_response(self,b):
        if b.text() == "Quit":      # quit case executes before checking/setting other inputs 
            print("quitting...")
            sys.exit(app.exec_())
        if b.text() == "HIGH":      # sets value corresponding to button being pushed
            value = 4095
            print(str(value))
        if b.text() == "LOW":
            value = 0
            print(str(value))
        if C_A != 1:    # writes new input value to connected ITV
            print("Attempting to write")
            SetPoint = value
            x = SetPoint.to_bytes(2, "little") #change to bytes
            data = pyeip.struct.pack("BB", x[0], x[1])
            if C_A != 1:
                print("Write to 1")
                r = C_A.setAttrSingle(0x64, 0x64, 0x03, data) #write to ITV
                if r[0] == 0:
                    print("Wrote!")
                else:
                    print("Failed to write")
        if C_B != 1:
            print("Attempting to write")
            SetPoint = value
            x = SetPoint.to_bytes(2, "little") #change to bytes
            data = pyeip.struct.pack("BB", x[0], x[1])
            if C_B != 1:
                print("Write to 2")
                r = C_B.setAttrSingle(0x64, 0x64, 0x03, data) #write to ITV
                if r[0] == 0:
                    print("Wrote!")
                else:
                    print("Failed to write")
        if C_C != 1:
            print("Attempting to write")
            SetPoint = value
            x = SetPoint.to_bytes(2, "little") #change to bytes
            data = pyeip.struct.pack("BB", x[0], x[1])
            if C_C != 1:
                print("Write to 3")
                r = C_C.setAttrSingle(0x64, 0x64, 0x03, data) #write to ITV
                if r[0] == 0:
                    print("Wrote!")
                else:
                    print("Failed to write")

    # Connection is only attempted when checkbox is filled. If previous attempt fails,
    # need to uncheck and recheck box to attempt another connection
    def check_connection(self,c,ITV):
        if c.isChecked() == True:       # executes @ checkbox state change, only executes if checked
            if ITV == 1:                # ITV variable selects which ITV should be connected
                print("Attempting to connect...")
                try:    #attempt to connect ITV1
                    global EIP_1, C_A
                    EIP_1= pyeip.EtherNetIP(hostname1)
                    C_A = EIP_1.explicit_conn(hostname1)
                except Exception:   # general catch-all error handler, triggers if no connection detected
                    C_A = 1     # set C_A back to disconnected state
                    
            elif ITV == 2:  # checks whatever ITV is specified by variable ITV (passed in from checkbox)
                print("Attempting to connect...")
                try:
                    global EIP_2, C_B
                    EIP_2= pyeip.EtherNetIP(hostname2)
                    C_B = EIP_2.explicit_conn(hostname2)
                except Exception:
                    #self.label_ITV_B.setText("ITV 2 (psi): " + str(pressure))
                    C_B = 1
            elif ITV == 3:
                print("Attempting to connect...")
                try:
                    global EIP_3, C_C
                    EIP_3= pyeip.EtherNetIP(hostname3)
                    C_C = EIP_3.explicit_conn(hostname3)
                except Exception:
                    C_C = 1
        else:       # no connection found, set C_% to non-connected state
            print("Not Connected")
            if ITV == 1:
                C_A = 1
            elif ITV == 2:
                C_B = 1
            elif ITV == 3:
                C_C = 1
    
    # update_status is called every time interval (line 100)
    # attempts to read count values from all connected ITVs and converts into PSI
    # Outputs to label associated with text box
    def update_status(self):
        if C_A != 1:    #if connection exists read and display values
            r = C_A.getAttrSingle(0x96, 0x96, 0x03)
            print(r[1])
            if 0 == r[0]:
                print(int.from_bytes(r[1],"little"))
                if(r[1][-2:] == b'\x00\x00'):
                    pressure = int.from_bytes(r[1],"little") #in counts
                    pressure = pressure / 31.37 #convert to psi
                    pressure = round(pressure, 1)
                    print(pressure)
                    self.label_ITV_A.setText("ITV 1 (psi): " + str(pressure))
            else:
                self.label_ITV_A.setText("ITV 1 (psi): Error Detected")
        else:
            print("C_A Disconnected")                    
        if C_B != 1:
            r = C_B.getAttrSingle(0x96, 0x96, 0x03)
            print(r[1])
            if 0 == r[0]:
                print(int.from_bytes(r[1],"little"))
                if(r[1][-2:] == b'\x00\x00'):
                    pressure = int.from_bytes(r[1],"little") #in counts
                    pressure = pressure / 31.37 #convert to psi
                    pressure = round(pressure, 1)
                    print(pressure)
                    self.label_ITV_B.setText("ITV 2 (psi): " + str(pressure))
            else:
                self.label_ITV_B.setText("ITV 2 (psi): Error Detected")
        else:
            print("C_B Disconnected")            
        if C_C != 1:
            r = C_C.getAttrSingle(0x96, 0x96, 0x03)
            print(r[1])
            if 0 == r[0]:
                print(int.from_bytes(r[1],"little"))
                if(r[1][-2:] == b'\x00\x00'):
                    pressure = int.from_bytes(r[1],"little") #in counts
                    pressure = pressure / 31.37 #convert to psi
                    pressure = round(pressure, 1)
                    print(pressure)
                    self.label_ITV_C.setText("ITV 3 (psi): " + str(pressure))
            else:   #Connected, error with the ITV
                self.label_ITV_C.setText("ITV 3 (psi): Error Detected")
        else:       #Disconnected
            print("C_C Disconnected")



# calls main function as specified by the class Ui_MainWindow
# This code is PyQt generated, do not attempt to edit
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())



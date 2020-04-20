# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Mainwindown.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1049, 501)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1049, 501))
        MainWindow.setMaximumSize(QtCore.QSize(1049, 501))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Icon/Icon-Mainwindown.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_videocam = QtWidgets.QLabel(self.centralwidget)
        self.label_videocam.setGeometry(QtCore.QRect(0, 0, 640, 480))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_videocam.sizePolicy().hasHeightForWidth())
        self.label_videocam.setSizePolicy(sizePolicy)
        self.label_videocam.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label_videocam.setText("")
        self.label_videocam.setAlignment(QtCore.Qt.AlignCenter)
        self.label_videocam.setObjectName("label_videocam")
        self.label_Mainresult = QtWidgets.QLabel(self.centralwidget)
        self.label_Mainresult.setGeometry(QtCore.QRect(640, 0, 411, 161))
        self.label_Mainresult.setAutoFillBackground(False)
        self.label_Mainresult.setStyleSheet("\n"
"color: blue;\n"
"font: 90pt \"Times New Roman\";")
        self.label_Mainresult.setTextFormat(QtCore.Qt.RichText)
        self.label_Mainresult.setScaledContents(False)
        self.label_Mainresult.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Mainresult.setWordWrap(True)
        self.label_Mainresult.setObjectName("label_Mainresult")
        self.label_quantity = QtWidgets.QLabel(self.centralwidget)
        self.label_quantity.setGeometry(QtCore.QRect(660, 160, 121, 71))
        self.label_quantity.setStyleSheet("font: 20pt \"Romantic\";\n"
"")
        self.label_quantity.setAlignment(QtCore.Qt.AlignCenter)
        self.label_quantity.setObjectName("label_quantity")
        self.label_result_Quantity = QtWidgets.QLabel(self.centralwidget)
        self.label_result_Quantity.setGeometry(QtCore.QRect(790, 160, 201, 71))
        self.label_result_Quantity.setStyleSheet("font: 24pt \"Times New Roman\";\n"
"color: blue;")
        self.label_result_Quantity.setAlignment(QtCore.Qt.AlignCenter)
        self.label_result_Quantity.setObjectName("label_result_Quantity")
        self.pushButton_cameraON = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_cameraON.setGeometry(QtCore.QRect(690, 340, 131, 41))
        self.pushButton_cameraON.setStyleSheet("         QPushButton {\n"
"            background-color: white;\n"
"            color: back;\n"
"           border: 1px solid #00B674;\n"
"           border-radius:6px;\n"
"        }\n"
"        QPushButton::hover {\n"
"         background-color:#9FE4CB;\n"
"        }\n"
"\n"
"        QPushButton::pressed {\n"
"          background-color: white;\n"
"        }")
        self.pushButton_cameraON.setAutoDefault(True)
        self.pushButton_cameraON.setFlat(False)
        self.pushButton_cameraON.setObjectName("pushButton_cameraON")
        self.pushButton_cameraOFF = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_cameraOFF.setGeometry(QtCore.QRect(880, 340, 121, 41))
        self.pushButton_cameraOFF.setStyleSheet("         QPushButton {\n"
"            background-color: white;\n"
"            color: back;\n"
"           border: 1px solid #00B674;\n"
"           border-radius:6px;\n"
"        }\n"
"        QPushButton::hover {\n"
"         background-color:#9FE4CB;\n"
"        }\n"
"\n"
"        QPushButton::pressed {\n"
"          background-color: white;\n"
"        }")
        self.pushButton_cameraOFF.setObjectName("pushButton_cameraOFF")
        self.pushButton_Clear = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Clear.setGeometry(QtCore.QRect(690, 410, 131, 41))
        self.pushButton_Clear.setStyleSheet("         QPushButton {\n"
"            background-color: white;\n"
"            color: back;\n"
"           border: 1px solid #00B674;\n"
"           border-radius:6px;\n"
"        }\n"
"        QPushButton::hover {\n"
"         background-color:#9FE4CB;\n"
"        }\n"
"\n"
"        QPushButton::pressed {\n"
"          background-color: white;\n"
"        }")
        self.pushButton_Clear.setObjectName("pushButton_Clear")
        self.pushButton_connectArduino = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_connectArduino.setGeometry(QtCore.QRect(880, 410, 121, 41))
        self.pushButton_connectArduino.setStyleSheet("         QPushButton {\n"
"            background-color: white;\n"
"            color: back;\n"
"           border: 1px solid #00B674;\n"
"           border-radius:6px;\n"
"        }\n"
"        QPushButton::hover {\n"
"         background-color:#9FE4CB;\n"
"        }\n"
"\n"
"        QPushButton::pressed {\n"
"          background-color: white;\n"
"        }")
        self.pushButton_connectArduino.setCheckable(True)
        self.pushButton_connectArduino.setChecked(False)
        self.pushButton_connectArduino.setObjectName("pushButton_connectArduino")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(640, 220, 411, 20))
        self.line.setStyleSheet("")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(640, 150, 411, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(640, 290, 411, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.label_OK = QtWidgets.QLabel(self.centralwidget)
        self.label_OK.setGeometry(QtCore.QRect(720, 230, 131, 71))
        self.label_OK.setStyleSheet("font: 24pt \"Times New Roman\";\n"
"color: blue;")
        self.label_OK.setAlignment(QtCore.Qt.AlignCenter)
        self.label_OK.setObjectName("label_OK")
        self.label_quantity_OK = QtWidgets.QLabel(self.centralwidget)
        self.label_quantity_OK.setGeometry(QtCore.QRect(660, 230, 71, 71))
        self.label_quantity_OK.setStyleSheet("font: 20pt \"Romantic\";")
        self.label_quantity_OK.setAlignment(QtCore.Qt.AlignCenter)
        self.label_quantity_OK.setObjectName("label_quantity_OK")
        self.label_quantity_NG = QtWidgets.QLabel(self.centralwidget)
        self.label_quantity_NG.setGeometry(QtCore.QRect(860, 230, 61, 71))
        self.label_quantity_NG.setStyleSheet("font: 20pt \"Romantic\";")
        self.label_quantity_NG.setAlignment(QtCore.Qt.AlignCenter)
        self.label_quantity_NG.setObjectName("label_quantity_NG")
        self.label_NG = QtWidgets.QLabel(self.centralwidget)
        self.label_NG.setGeometry(QtCore.QRect(920, 230, 131, 71))
        self.label_NG.setStyleSheet("font: 24pt \"Times New Roman\";\n"
"color: rgb(255, 0, 0);")
        self.label_NG.setAlignment(QtCore.Qt.AlignCenter)
        self.label_NG.setObjectName("label_NG")
        self.label_videocam.raise_()
        self.label_Mainresult.raise_()
        self.label_quantity.raise_()
        self.label_result_Quantity.raise_()
        self.pushButton_cameraON.raise_()
        self.pushButton_cameraOFF.raise_()
        self.pushButton_Clear.raise_()
        self.pushButton_connectArduino.raise_()
        self.line.raise_()
        self.line_2.raise_()
        self.label_OK.raise_()
        self.label_quantity_OK.raise_()
        self.label_quantity_NG.raise_()
        self.label_NG.raise_()
        self.line_3.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1049, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setAutoFillBackground(False)
        self.menuFile.setObjectName("menuFile")
        self.menuSetting = QtWidgets.QMenu(self.menubar)
        self.menuSetting.setObjectName("menuSetting")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.actionParameter = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Icon/Icon-Setting.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionParameter.setIcon(icon1)
        self.actionParameter.setVisible(True)
        self.actionParameter.setPriority(QtWidgets.QAction.NormalPriority)
        self.actionParameter.setObjectName("actionParameter")
        self.actionSave = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Icon/save.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon2)
        self.actionSave.setObjectName("actionSave")
        self.actionExits = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Icon/exits.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExits.setIcon(icon3)
        self.actionExits.setObjectName("actionExits")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("Icon/About.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon4)
        self.actionAbout.setObjectName("actionAbout")
        self.actionDocumment = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("Icon/document.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDocumment.setIcon(icon5)
        self.actionDocumment.setObjectName("actionDocumment")
        self.actionArduino_Uno = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("Icon/Ard.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionArduino_Uno.setIcon(icon6)
        self.actionArduino_Uno.setObjectName("actionArduino_Uno")
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExits)
        self.menuSetting.addAction(self.actionParameter)
        self.menuSetting.addAction(self.actionArduino_Uno)
        self.menuAbout.addAction(self.actionAbout)
        self.menuAbout.addAction(self.actionDocumment)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSetting.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CamArd"))
        self.label_Mainresult.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">None<br/></p></body></html>"))
        self.label_quantity.setText(_translate("MainWindow", "Quantity"))
        self.label_result_Quantity.setText(_translate("MainWindow", "0"))
        self.pushButton_cameraON.setText(_translate("MainWindow", "Camera ON"))
        self.pushButton_cameraOFF.setText(_translate("MainWindow", "Camera OFF"))
        self.pushButton_Clear.setText(_translate("MainWindow", "Clear All"))
        self.pushButton_connectArduino.setText(_translate("MainWindow", "Serial ON"))
        self.label_OK.setText(_translate("MainWindow", "0"))
        self.label_quantity_OK.setText(_translate("MainWindow", "OK"))
        self.label_quantity_NG.setText(_translate("MainWindow", "NG"))
        self.label_NG.setText(_translate("MainWindow", "0"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSetting.setTitle(_translate("MainWindow", "Setting"))
        self.menuAbout.setTitle(_translate("MainWindow", "Help"))
        self.actionParameter.setText(_translate("MainWindow", "Parameter"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionExits.setText(_translate("MainWindow", "Exits"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionDocumment.setText(_translate("MainWindow", "Documment"))
        self.actionArduino_Uno.setText(_translate("MainWindow", "Arduino Uno"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Intro(object):
    def setupUi(self, Intro):
        Intro.setObjectName("Intro")
        Intro.resize(564, 247)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Icon/Icon-Mainwindown.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Intro.setWindowIcon(icon)
        Intro.setStyleSheet("background-color: #1B84B3")
        self.label = QtWidgets.QLabel(Intro)
        self.label.setGeometry(QtCore.QRect(0, 0, 571, 181))
        self.label.setMinimumSize(QtCore.QSize(571, 181))
        self.label.setMaximumSize(QtCore.QSize(571, 181))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("Icon/logo.png"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Intro)
        self.label_2.setGeometry(QtCore.QRect(40, 200, 511, 31))
        self.label_2.setStyleSheet("font: 11pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);")
        self.label_2.setScaledContents(False)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Intro)
        self.label_3.setGeometry(QtCore.QRect(40, 170, 341, 31))
        self.label_3.setStyleSheet("font: 11pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Intro)
        QtCore.QMetaObject.connectSlotsByName(Intro)

    def retranslateUi(self, Intro):
        _translate = QtCore.QCoreApplication.translate
        Intro.setWindowTitle(_translate("Intro", "About"))
        self.label_2.setText(_translate("Intro", "Contact by Phone: 0706116574    Gmail: thaingoctam11cdt2@gmail.com"))
        self.label_3.setText(_translate("Intro", "Copyright ©  by Tam-Vinh Team.                                   "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Intro = QtWidgets.QDialog()
    ui = Ui_Intro()
    ui.setupUi(Intro)
    Intro.show()
    sys.exit(app.exec_())


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'About-custom.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import webbrowser


class Ui_Intro(object):
    def setupUi(self, Intro):
        Intro.setObjectName("Intro")
        Intro.resize(516, 285)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../project cam/Icon/Icon-Mainwindown.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Intro.setWindowIcon(icon)
        Intro.setStyleSheet("background-color: #3C3F41;")
        self.label = QtWidgets.QLabel(Intro)
        self.label.setGeometry(QtCore.QRect(-18, -10, 571, 181))
        self.label.setMinimumSize(QtCore.QSize(571, 181))
        self.label.setMaximumSize(QtCore.QSize(571, 181))
        self.label.setStyleSheet("font: 8pt \"Segoe UI\";\n"
                                 "background-color: #3C3F41;")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/newPrefix/logo.png"))
        self.label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Intro)
        self.label_2.setGeometry(QtCore.QRect(50, 184, 511, 31))
        self.label_2.setMinimumSize(QtCore.QSize(511, 31))
        self.label_2.setStyleSheet("font: 10pt \"Segoe UI\";\n"
                                   "color:white;")
        self.label_2.setScaledContents(False)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Intro)
        self.label_3.setGeometry(QtCore.QRect(52, 158, 341, 31))
        self.label_3.setStyleSheet("font: 10pt \"Segoe UI\";\n"
                                   "color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Intro)
        self.label_4.setGeometry(QtCore.QRect(50, 210, 511, 31))
        self.label_4.setStyleSheet("font: 10pt \"Segoe UI\";\n"
                                   "color:white;")
        self.label_4.setScaledContents(False)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Intro)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(50, 242, 179, 42))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_RemoveRect_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_RemoveRect_2.sizePolicy().hasHeightForWidth())
        self.pushButton_RemoveRect_2.setSizePolicy(sizePolicy)
        self.pushButton_RemoveRect_2.setStyleSheet("        QPushButton{ \n"
                                                   "            border: 0px;\n"
                                                   "            border-radius:17px;\n"
                                                   "}\n"
                                                   "        QPushButton::hover {\n"
                                                   "          border-left:5px solid transparent;\n"
                                                   "        }\n"
                                                   "\n"
                                                   "        QPushButton::pressed {\n"
                                                   "          border-top:4px solid transparent;\n"
                                                   "        }\n"
                                                   "\n"
                                                   "         QToolTip {\n"
                                                   "          color: white;\n"
                                                   "          background-color: rgb(62, 67, 76);\n"
                                                   "          border: 0px;\n"
                                                   "          }")
        self.pushButton_RemoveRect_2.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/newPrefix/facebook (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_RemoveRect_2.setIcon(icon1)
        self.pushButton_RemoveRect_2.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_RemoveRect_2.setAutoDefault(False)
        self.pushButton_RemoveRect_2.setFlat(True)
        self.pushButton_RemoveRect_2.setObjectName("pushButton_RemoveRect_2")
        self.horizontalLayout.addWidget(self.pushButton_RemoveRect_2)
        self.pushButton_RemoveRect_3 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_RemoveRect_3.sizePolicy().hasHeightForWidth())
        self.pushButton_RemoveRect_3.setSizePolicy(sizePolicy)
        self.pushButton_RemoveRect_3.setStyleSheet("        QPushButton{ \n"
                                                   "            border: 0px;\n"
                                                   "            border-radius:17px;\n"
                                                   "}\n"
                                                   "        QPushButton::hover {\n"
                                                   "          border-left:3px solid transparent;\n"
                                                   "        }\n"
                                                   "\n"
                                                   "        QPushButton::pressed {\n"
                                                   "          border-top:4px solid transparent;\n"
                                                   "        }\n"
                                                   "\n"
                                                   "         QToolTip {\n"
                                                   "          color: white;\n"
                                                   "          background-color: rgb(62, 67, 76);\n"
                                                   "          border: 0px;\n"
                                                   "          }")
        self.pushButton_RemoveRect_3.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/newPrefix/zalo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_RemoveRect_3.setIcon(icon2)
        self.pushButton_RemoveRect_3.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_RemoveRect_3.setAutoDefault(False)
        self.pushButton_RemoveRect_3.setFlat(True)
        self.pushButton_RemoveRect_3.setObjectName("pushButton_RemoveRect_3")
        self.horizontalLayout.addWidget(self.pushButton_RemoveRect_3)
        self.pushButton_RemoveRect_4 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_RemoveRect_4.sizePolicy().hasHeightForWidth())
        self.pushButton_RemoveRect_4.setSizePolicy(sizePolicy)
        self.pushButton_RemoveRect_4.setStyleSheet("        QPushButton{ \n"
                                                   "            border: 0px;\n"
                                                   "            border-radius:17px;\n"
                                                   "}\n"
                                                   "        QPushButton::hover {\n"
                                                   "          border-left:5px solid transparent;\n"
                                                   "        }\n"
                                                   "\n"
                                                   "        QPushButton::pressed {\n"
                                                   "          border-top:4px solid transparent;\n"
                                                   "        }\n"
                                                   "\n"
                                                   "         QToolTip {\n"
                                                   "          color: white;\n"
                                                   "          background-color: rgb(62, 67, 76);\n"
                                                   "          border: 0px;\n"
                                                   "          }")
        self.pushButton_RemoveRect_4.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/newPrefix/youtube.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_RemoveRect_4.setIcon(icon3)
        self.pushButton_RemoveRect_4.setIconSize(QtCore.QSize(28, 28))
        self.pushButton_RemoveRect_4.setAutoDefault(False)
        self.pushButton_RemoveRect_4.setFlat(True)
        self.pushButton_RemoveRect_4.setObjectName("pushButton_RemoveRect_4")
        self.horizontalLayout.addWidget(self.pushButton_RemoveRect_4)

        self.retranslateUi(Intro)
        self.pushButton_RemoveRect_2.clicked.connect(lambda: webbrowser.open(
            'https://www.facebook.com/groups/832920733581709/?multi_permalinks=1540354952838280%2C1539603826246726%2C1539597576247351%2C1539588449581597%2C1538615946345514&notif_id=1599388650027497&notif_t=group_activity&ref=notif'))
        self.pushButton_RemoveRect_3.clicked.connect(lambda: webbrowser.open('http://zaloapp.com/qr/p/1kym0bvqxv2ha'))
        self.pushButton_RemoveRect_4.clicked.connect(lambda: webbrowser.open('https://www.youtube.com/channel/UCu7HyH2BPCPgsdDRK-wu7lQ?view_as=subscriber'))
        QtCore.QMetaObject.connectSlotsByName(Intro)



    def retranslateUi(self, Intro):
        _translate = QtCore.QCoreApplication.translate
        Intro.setWindowTitle(_translate("Intro", "About"))
        self.label_2.setText(_translate("Intro", "Contact by Phone: 0706116574   -  033430628"))
        self.label_3.setText(_translate("Intro", "Copyright ©  by TVTeam.                                   "))
        self.label_4.setText(_translate("Intro", "Gmail: thaingoctam11cdt2@gmail.com - Nguyenvinhstv@gmail.com"))
        self.pushButton_RemoveRect_2.setToolTip(_translate("Intro", "FaceBook"))
        self.pushButton_RemoveRect_3.setToolTip(_translate("Intro", "Zalo"))
        self.pushButton_RemoveRect_4.setToolTip(_translate("Intro", "Youtube"))


# import SVG

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Intro = QtWidgets.QDialog()
    ui = Ui_Intro()
    ui.setupUi(Intro)
    Intro.show()
    sys.exit(app.exec_())

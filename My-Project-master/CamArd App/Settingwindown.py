# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Settingwindown.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Setting(object):
    def setupUi(self, Setting):
        Setting.setObjectName("Setting")
        Setting.resize(1049, 520)
        Setting.setMinimumSize(QtCore.QSize(1049, 520))
        Setting.setMaximumSize(QtCore.QSize(1049, 520))
        Setting.setFocusPolicy(QtCore.Qt.TabFocus)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Icon/Icon-Setting.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Setting.setWindowIcon(icon)
        Setting.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label_maxvalue_RGB_2 = QtWidgets.QLabel(Setting)
        self.label_maxvalue_RGB_2.setGeometry(QtCore.QRect(680, 20, 61, 21))
        self.label_maxvalue_RGB_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_maxvalue_RGB_2.setObjectName("label_maxvalue_RGB_2")
        self.doubleSpinBox_Maxvalue_RGB_01 = QtWidgets.QDoubleSpinBox(Setting)
        self.doubleSpinBox_Maxvalue_RGB_01.setEnabled(False)
        self.doubleSpinBox_Maxvalue_RGB_01.setGeometry(QtCore.QRect(740, 20, 91, 22))
        self.doubleSpinBox_Maxvalue_RGB_01.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.doubleSpinBox_Maxvalue_RGB_01.setStyleSheet("border-color: rgb(255, 0, 0);")
        self.doubleSpinBox_Maxvalue_RGB_01.setDecimals(4)
        self.doubleSpinBox_Maxvalue_RGB_01.setMaximum(10000.0)
        self.doubleSpinBox_Maxvalue_RGB_01.setSingleStep(1.0)
        self.doubleSpinBox_Maxvalue_RGB_01.setProperty("value", 10000.0)
        self.doubleSpinBox_Maxvalue_RGB_01.setObjectName("doubleSpinBox_Maxvalue_RGB_01")
        self.doubleSpinBox_Minvalue_RGB_01 = QtWidgets.QDoubleSpinBox(Setting)
        self.doubleSpinBox_Minvalue_RGB_01.setEnabled(False)
        self.doubleSpinBox_Minvalue_RGB_01.setGeometry(QtCore.QRect(911, 20, 91, 22))
        self.doubleSpinBox_Minvalue_RGB_01.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.doubleSpinBox_Minvalue_RGB_01.setDecimals(4)
        self.doubleSpinBox_Minvalue_RGB_01.setMaximum(9999.9999)
        self.doubleSpinBox_Minvalue_RGB_01.setSingleStep(1.0)
        self.doubleSpinBox_Minvalue_RGB_01.setObjectName("doubleSpinBox_Minvalue_RGB_01")
        self.label_minvalue_RGB_01 = QtWidgets.QLabel(Setting)
        self.label_minvalue_RGB_01.setGeometry(QtCore.QRect(850, 20, 61, 21))
        self.label_minvalue_RGB_01.setAlignment(QtCore.Qt.AlignCenter)
        self.label_minvalue_RGB_01.setObjectName("label_minvalue_RGB_01")
        self.horizontalSlider_LH = QtWidgets.QSlider(Setting)
        self.horizontalSlider_LH.setEnabled(False)
        self.horizontalSlider_LH.setGeometry(QtCore.QRect(680, 70, 331, 31))
        self.horizontalSlider_LH.setStyleSheet("\n"
"QSlider::groove:horizontal {\n"
"    border: 1px solid red;\n"
"    height:5px; /* the groove expands to the size of the slider by default. by giving it a height, it has a fixed size */\n"
"    margin: 0.3px 0;\n"
"\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background: white ;\n"
"    border: 4px solid #00B674;\n"
"    width:8px;\n"
"    margin: -6px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */\n"
"    border-radius:8px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal  {\n"
"    background:#9FE4CB;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"    background:#00B674;\n"
"}")
        self.horizontalSlider_LH.setMaximum(255)
        self.horizontalSlider_LH.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_LH.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSlider_LH.setTickInterval(10)
        self.horizontalSlider_LH.setObjectName("horizontalSlider_LH")
        self.label_value_slider_LH = QtWidgets.QLabel(Setting)
        self.label_value_slider_LH.setGeometry(QtCore.QRect(1016, 70, 31, 21))
        self.label_value_slider_LH.setAlignment(QtCore.Qt.AlignCenter)
        self.label_value_slider_LH.setObjectName("label_value_slider_LH")
        self.line = QtWidgets.QFrame(Setting)
        self.line.setGeometry(QtCore.QRect(650, 370, 401, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.pushButton_testSample_Area = QtWidgets.QPushButton(Setting)
        self.pushButton_testSample_Area.setGeometry(QtCore.QRect(860, 410, 81, 31))
        self.pushButton_testSample_Area.setStyleSheet("         QPushButton {\n"
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
        self.pushButton_testSample_Area.setObjectName("pushButton_testSample_Area")
        self.pushButton_Saveallparameter = QtWidgets.QPushButton(Setting)
        self.pushButton_Saveallparameter.setGeometry(QtCore.QRect(660, 470, 81, 31))
        self.pushButton_Saveallparameter.setStyleSheet("         QPushButton {\n"
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
        self.pushButton_Saveallparameter.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_Saveallparameter.setFlat(False)
        self.pushButton_Saveallparameter.setObjectName("pushButton_Saveallparameter")
        self.label_Result_test = QtWidgets.QLabel(Setting)
        self.label_Result_test.setGeometry(QtCore.QRect(320, 480, 321, 41))
        self.label_Result_test.setStyleSheet("color: blue;\n"
"font: 75 18pt \"Romantic\";")
        self.label_Result_test.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Result_test.setObjectName("label_Result_test")
        self.pushButton_DrawRect = QtWidgets.QPushButton(Setting)
        self.pushButton_DrawRect.setGeometry(QtCore.QRect(660, 410, 81, 31))
        self.pushButton_DrawRect.setStyleSheet("         QPushButton {\n"
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
        self.pushButton_DrawRect.setCheckable(True)
        self.pushButton_DrawRect.setChecked(False)
        self.pushButton_DrawRect.setAutoDefault(False)
        self.pushButton_DrawRect.setDefault(False)
        self.pushButton_DrawRect.setFlat(False)
        self.pushButton_DrawRect.setObjectName("pushButton_DrawRect")
        self.pushButton_RemoveRect = QtWidgets.QPushButton(Setting)
        self.pushButton_RemoveRect.setGeometry(QtCore.QRect(760, 410, 81, 31))
        self.pushButton_RemoveRect.setStyleSheet("         QPushButton {\n"
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
        self.pushButton_RemoveRect.setObjectName("pushButton_RemoveRect")
        self.label_ImageSetting = QtWidgets.QLabel(Setting)
        self.label_ImageSetting.setGeometry(QtCore.QRect(0, 0, 640, 480))
        self.label_ImageSetting.setObjectName("label_ImageSetting")
        self.pushButton_OpenImage = QtWidgets.QPushButton(Setting)
        self.pushButton_OpenImage.setGeometry(QtCore.QRect(760, 470, 81, 31))
        self.pushButton_OpenImage.setStyleSheet("         QPushButton {\n"
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
        self.pushButton_OpenImage.setObjectName("pushButton_OpenImage")
        self.label_value_slider_LS = QtWidgets.QLabel(Setting)
        self.label_value_slider_LS.setGeometry(QtCore.QRect(1016, 120, 31, 21))
        self.label_value_slider_LS.setAlignment(QtCore.Qt.AlignCenter)
        self.label_value_slider_LS.setObjectName("label_value_slider_LS")
        self.horizontalSlider_LS = QtWidgets.QSlider(Setting)
        self.horizontalSlider_LS.setEnabled(False)
        self.horizontalSlider_LS.setGeometry(QtCore.QRect(680, 120, 331, 31))
        self.horizontalSlider_LS.setStyleSheet("\n"
"QSlider::groove:horizontal {\n"
"    border: 1px solid red;\n"
"    height:5px; /* the groove expands to the size of the slider by default. by giving it a height, it has a fixed size */\n"
"    margin: 0.3px 0;\n"
"\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background: white ;\n"
"    border: 4px solid #00B674;\n"
"    width:8px;\n"
"    margin: -6px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */\n"
"    border-radius:8px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal  {\n"
"    background:#9FE4CB;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"    background:#00B674;\n"
"}")
        self.horizontalSlider_LS.setMaximum(255)
        self.horizontalSlider_LS.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_LS.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSlider_LS.setTickInterval(20)
        self.horizontalSlider_LS.setObjectName("horizontalSlider_LS")
        self.label_value_slider_LV = QtWidgets.QLabel(Setting)
        self.label_value_slider_LV.setGeometry(QtCore.QRect(1016, 170, 31, 21))
        self.label_value_slider_LV.setAlignment(QtCore.Qt.AlignCenter)
        self.label_value_slider_LV.setObjectName("label_value_slider_LV")
        self.horizontalSlider_LV = QtWidgets.QSlider(Setting)
        self.horizontalSlider_LV.setEnabled(False)
        self.horizontalSlider_LV.setGeometry(QtCore.QRect(680, 170, 331, 31))
        self.horizontalSlider_LV.setStyleSheet("\n"
"QSlider::groove:horizontal {\n"
"    border: 1px solid red;\n"
"    height:5px; /* the groove expands to the size of the slider by default. by giving it a height, it has a fixed size */\n"
"    margin: 0.3px 0;\n"
"\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background: white ;\n"
"    border: 4px solid #00B674;\n"
"    width:8px;\n"
"    margin: -6px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */\n"
"    border-radius:8px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal  {\n"
"    background:#9FE4CB;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"    background:#00B674;\n"
"}")
        self.horizontalSlider_LV.setMaximum(255)
        self.horizontalSlider_LV.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_LV.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSlider_LV.setTickInterval(20)
        self.horizontalSlider_LV.setObjectName("horizontalSlider_LV")
        self.label_R = QtWidgets.QLabel(Setting)
        self.label_R.setGeometry(QtCore.QRect(640, 70, 41, 21))
        self.label_R.setAlignment(QtCore.Qt.AlignCenter)
        self.label_R.setObjectName("label_R")
        self.label_G = QtWidgets.QLabel(Setting)
        self.label_G.setGeometry(QtCore.QRect(640, 120, 41, 21))
        self.label_G.setAlignment(QtCore.Qt.AlignCenter)
        self.label_G.setObjectName("label_G")
        self.label_B = QtWidgets.QLabel(Setting)
        self.label_B.setGeometry(QtCore.QRect(640, 170, 41, 21))
        self.label_B.setAlignment(QtCore.Qt.AlignCenter)
        self.label_B.setObjectName("label_B")
        self.pushButton_SaveImage = QtWidgets.QPushButton(Setting)
        self.pushButton_SaveImage.setGeometry(QtCore.QRect(860, 470, 81, 31))
        self.pushButton_SaveImage.setStyleSheet("         QPushButton {\n"
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
        self.pushButton_SaveImage.setObjectName("pushButton_SaveImage")
        self.label_Result_Area = QtWidgets.QLabel(Setting)
        self.label_Result_Area.setGeometry(QtCore.QRect(0, 480, 321, 41))
        self.label_Result_Area.setStyleSheet("color: Blue;\n"
"font:  18pt \"Romantic\";")
        self.label_Result_Area.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Result_Area.setObjectName("label_Result_Area")
        self.horizontalSlider_UH = QtWidgets.QSlider(Setting)
        self.horizontalSlider_UH.setEnabled(False)
        self.horizontalSlider_UH.setGeometry(QtCore.QRect(680, 220, 331, 31))
        self.horizontalSlider_UH.setStyleSheet("\n"
"QSlider::groove:horizontal {\n"
"    border: 1px solid red;\n"
"    height:5px; /* the groove expands to the size of the slider by default. by giving it a height, it has a fixed size */\n"
"    margin: 0.3px 0;\n"
"\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background: white ;\n"
"    border: 4px solid #00B674;\n"
"    width:8px;\n"
"    margin: -6px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */\n"
"    border-radius:8px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal  {\n"
"    background:#9FE4CB;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"    background:#00B674;\n"
"}")
        self.horizontalSlider_UH.setMaximum(255)
        self.horizontalSlider_UH.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_UH.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSlider_UH.setTickInterval(20)
        self.horizontalSlider_UH.setObjectName("horizontalSlider_UH")
        self.label_B_2 = QtWidgets.QLabel(Setting)
        self.label_B_2.setGeometry(QtCore.QRect(640, 220, 41, 21))
        self.label_B_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_B_2.setObjectName("label_B_2")
        self.label_value_slider_UH = QtWidgets.QLabel(Setting)
        self.label_value_slider_UH.setGeometry(QtCore.QRect(1010, 220, 41, 21))
        self.label_value_slider_UH.setAlignment(QtCore.Qt.AlignCenter)
        self.label_value_slider_UH.setObjectName("label_value_slider_UH")
        self.horizontalSlider_US = QtWidgets.QSlider(Setting)
        self.horizontalSlider_US.setEnabled(False)
        self.horizontalSlider_US.setGeometry(QtCore.QRect(680, 270, 331, 31))
        self.horizontalSlider_US.setStyleSheet("\n"
"QSlider::groove:horizontal {\n"
"    border: 1px solid red;\n"
"    height:5px; /* the groove expands to the size of the slider by default. by giving it a height, it has a fixed size */\n"
"    margin: 0.3px 0;\n"
"\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background: white ;\n"
"    border: 4px solid #00B674;\n"
"    width:8px;\n"
"    margin: -6px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */\n"
"    border-radius:8px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal  {\n"
"    background:#9FE4CB;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"    background:#00B674;\n"
"}")
        self.horizontalSlider_US.setMaximum(255)
        self.horizontalSlider_US.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_US.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSlider_US.setTickInterval(20)
        self.horizontalSlider_US.setObjectName("horizontalSlider_US")
        self.label_B_3 = QtWidgets.QLabel(Setting)
        self.label_B_3.setGeometry(QtCore.QRect(640, 270, 41, 21))
        self.label_B_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_B_3.setObjectName("label_B_3")
        self.label_value_slider_US = QtWidgets.QLabel(Setting)
        self.label_value_slider_US.setGeometry(QtCore.QRect(1010, 270, 41, 21))
        self.label_value_slider_US.setAlignment(QtCore.Qt.AlignCenter)
        self.label_value_slider_US.setObjectName("label_value_slider_US")
        self.label_B_4 = QtWidgets.QLabel(Setting)
        self.label_B_4.setGeometry(QtCore.QRect(640, 320, 41, 21))
        self.label_B_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_B_4.setObjectName("label_B_4")
        self.label_value_slider_UV = QtWidgets.QLabel(Setting)
        self.label_value_slider_UV.setGeometry(QtCore.QRect(1016, 320, 31, 21))
        self.label_value_slider_UV.setAlignment(QtCore.Qt.AlignCenter)
        self.label_value_slider_UV.setObjectName("label_value_slider_UV")
        self.horizontalSlider_UV = QtWidgets.QSlider(Setting)
        self.horizontalSlider_UV.setEnabled(False)
        self.horizontalSlider_UV.setGeometry(QtCore.QRect(680, 320, 331, 31))
        self.horizontalSlider_UV.setStyleSheet("\n"
"QSlider::groove:horizontal {\n"
"    border: 1px solid red;\n"
"    height:5px; /* the groove expands to the size of the slider by default. by giving it a height, it has a fixed size */\n"
"    margin: 0.3px 0;\n"
"\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background: white ;\n"
"    border: 4px solid #00B674;\n"
"    width:8px;\n"
"    margin: -6px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */\n"
"    border-radius:8px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal  {\n"
"    background:#9FE4CB;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"    background:#00B674;\n"
"}")
        self.horizontalSlider_UV.setMaximum(255)
        self.horizontalSlider_UV.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_UV.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSlider_UV.setTickInterval(20)
        self.horizontalSlider_UV.setObjectName("horizontalSlider_UV")
        self.line_3 = QtWidgets.QFrame(Setting)
        self.line_3.setGeometry(QtCore.QRect(310, 480, 20, 61))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.pushButton_Position = QtWidgets.QPushButton(Setting)
        self.pushButton_Position.setGeometry(QtCore.QRect(960, 410, 81, 31))
        self.pushButton_Position.setStyleSheet("         QPushButton {\n"
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
        self.pushButton_Position.setCheckable(True)
        self.pushButton_Position.setChecked(False)
        self.pushButton_Position.setAutoDefault(False)
        self.pushButton_Position.setDefault(False)
        self.pushButton_Position.setFlat(False)
        self.pushButton_Position.setObjectName("pushButton_Position")
        self.pushButton_Distance = QtWidgets.QPushButton(Setting)
        self.pushButton_Distance.setGeometry(QtCore.QRect(960, 470, 81, 31))
        self.pushButton_Distance.setStyleSheet("         QPushButton {\n"
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
        self.pushButton_Distance.setCheckable(True)
        self.pushButton_Distance.setChecked(False)
        self.pushButton_Distance.setAutoDefault(False)
        self.pushButton_Distance.setDefault(False)
        self.pushButton_Distance.setFlat(False)
        self.pushButton_Distance.setObjectName("pushButton_Distance")
        self.label_maxvalue_RGB_2.raise_()
        self.doubleSpinBox_Maxvalue_RGB_01.raise_()
        self.doubleSpinBox_Minvalue_RGB_01.raise_()
        self.label_minvalue_RGB_01.raise_()
        self.horizontalSlider_LH.raise_()
        self.label_value_slider_LH.raise_()
        self.pushButton_testSample_Area.raise_()
        self.pushButton_Saveallparameter.raise_()
        self.label_Result_test.raise_()
        self.pushButton_DrawRect.raise_()
        self.pushButton_RemoveRect.raise_()
        self.pushButton_OpenImage.raise_()
        self.label_value_slider_LS.raise_()
        self.horizontalSlider_LS.raise_()
        self.label_value_slider_LV.raise_()
        self.horizontalSlider_LV.raise_()
        self.pushButton_SaveImage.raise_()
        self.label_Result_Area.raise_()
        self.horizontalSlider_UH.raise_()
        self.label_value_slider_UH.raise_()
        self.horizontalSlider_US.raise_()
        self.label_value_slider_US.raise_()
        self.label_value_slider_UV.raise_()
        self.horizontalSlider_UV.raise_()
        self.line_3.raise_()
        self.label_ImageSetting.raise_()
        self.line.raise_()
        self.label_R.raise_()
        self.label_G.raise_()
        self.label_B.raise_()
        self.label_B_4.raise_()
        self.label_B_2.raise_()
        self.label_B_3.raise_()
        self.pushButton_Position.raise_()
        self.pushButton_Distance.raise_()

        self.retranslateUi(Setting)
        QtCore.QMetaObject.connectSlotsByName(Setting)

    def retranslateUi(self, Setting):
        _translate = QtCore.QCoreApplication.translate
        Setting.setWindowTitle(_translate("Setting", "Setting"))
        self.label_maxvalue_RGB_2.setText(_translate("Setting", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#ff0000;\">Max</span></p></body></html>"))
        self.label_minvalue_RGB_01.setText(_translate("Setting", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;color:red;\">Min </span></p></body></html>"))
        self.label_value_slider_LH.setText(_translate("Setting", "0"))
        self.pushButton_testSample_Area.setText(_translate("Setting", "Test"))
        self.pushButton_Saveallparameter.setText(_translate("Setting", "Save"))
        self.label_Result_test.setText(_translate("Setting", "Result"))
        self.pushButton_DrawRect.setText(_translate("Setting", "Draw Rect"))
        self.pushButton_RemoveRect.setText(_translate("Setting", "Remove Rect"))
        self.label_ImageSetting.setText(_translate("Setting", "<html><head/><body><p><br/></p></body></html>"))
        self.pushButton_OpenImage.setText(_translate("Setting", "Open Image"))
        self.label_value_slider_LS.setText(_translate("Setting", "0"))
        self.label_value_slider_LV.setText(_translate("Setting", "0"))
        self.label_R.setText(_translate("Setting", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:blue;\">L-H</span></p><p><br/></p></body></html>"))
        self.label_G.setText(_translate("Setting", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:blue;\">L-S</span></p></body></html>"))
        self.label_B.setText(_translate("Setting", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:blue;\">L-V</span></p></body></html>"))
        self.pushButton_SaveImage.setText(_translate("Setting", "Delete"))
        self.label_Result_Area.setText(_translate("Setting", "Area"))
        self.label_B_2.setText(_translate("Setting", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:blue;\">L-V</span></p></body></html>"))
        self.label_value_slider_UH.setText(_translate("Setting", "0"))
        self.label_B_3.setText(_translate("Setting", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:blue;\">L-V</span></p></body></html>"))
        self.label_value_slider_US.setText(_translate("Setting", "0"))
        self.label_B_4.setText(_translate("Setting", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:blue;\">L-V</span></p></body></html>"))
        self.label_value_slider_UV.setText(_translate("Setting", "0"))
        self.pushButton_Position.setText(_translate("Setting", "Position"))
        self.pushButton_Distance.setText(_translate("Setting", "Distance"))

# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Module.SettingWindown import *
from Module.UI.Mainwindown_UI import *
from Module.UI.Arduino_UI import *
from Module.UI.About_UI import *
from Module.UI.SVG import *
import cv2
import sys
import serial
import time
import serial.tools.list_ports
import sqlite3
import threading
import os
from toucamera import *
from add_key import *


class Foster_app(QMainWindow):
    SenddatatoArduino_NG = pyqtSignal()
    sizeChanged = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setMinimumSize(QtCore.QSize(800, 600))
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.timer = QtCore.QTimer()
        self.xuat_mang_so = []
        self.xuat_mang_kq = []
        self.data_arduino = []
        self.isCapturing = False
        self.noPort = False
        self.quantity_OK_cam = 0
        self.quantity_NG_cam = 0
        self.quantity_OK_cam1 = 0
        self.quantity_NG_cam1 = 0
        self.quantity_OK_cam2 = 0
        self.quantity_NG_cam2 = 0
        self.quantity_total = 0
        self.workThread = WorkThread()
        self.Inital_dataArd()
        self.readSaveF = SaveAndRead("cam1_setting")
        self.absoluteUrlFile = os.path.dirname(__file__)

        self.ui.actionCamera1.triggered.connect(self.setting_parameter)
        self.ui.actionCamera_2.triggered.connect(self.setting_parameter)
        self.ui.actionArduino_Uno.triggered.connect(self.Arduino_setting)
        self.ui.actionDocumment.triggered.connect(self.openDocument)
        self.ui.actionAbout.triggered.connect(self.Aboutme)
        self.ui.actionSave.triggered.connect(self.saveFileDialog)
        self.ui.actionExits.triggered.connect(self.deleteLater)

        self.ui.pushButton_camera1.clicked.connect(self.changeStatusCam)
        self.ui.pushButton_ClearAll.clicked.connect(self.clearQuantity)
        self.ui.pushButton_ClearAll.clicked.connect(self.xoamang_xuatfile)
        self.ui.pushButton_connectArduino.clicked.connect(self.changeStatusSerial)
        self.ui.pushButton_test.clicked.connect(self.getResult)
        self.ui.pushButton_auto_manual.clicked.connect(self.changeMenuStatus)

        self.workThread.letdoit.connect(self.getResult)
        self.workThread.Error.connect(self.ErrorNoArd)
        self.workThread.sp1.connect(self.fileData1)
        self.workThread.sp2.connect(self.fileData2)
        self.workThread.sp3.connect(self.fileData3)

        self.pix_cam1 = QtGui.QPixmap(os.path.join(root, 'Icon', 'anh_con_hang.jpg'))
        self.pix_cam2 = QtGui.QPixmap(os.path.join(root, 'Icon', 'anh_con_hang.jpg'))
        self.frame1 = cv2.imread(os.path.join(root, 'Icon', 'anh_con_hang.jpg'))
        self.frame2 = cv2.imread(os.path.join(root, 'Icon', 'anh_con_hang.jpg'))
        self.listPort = self.readSaveF.getPort()
        self.Startcam()
        self.StartSerial()
        self.lockmenuBar()
        self.changeStatusFile()
        self.fix = False
        self.updateQlabelNTF = 0

    def changeMenuStatus(self):
        if self.ui.pushButton_auto_manual.isChecked():
            self.lockmenuBar()
        else:
            self.unlockMenuBar()

    def changeStatusCam(self):
        if self.ui.pushButton_camera1.isChecked():
            self.Startcam()
        else:
            self.Stopcam()

    def changeStatusSerial(self):
        if self.ui.pushButton_connectArduino.isChecked():
            self.StartSerial()
        else:
            self.StopSerial()

    def changeStatusFile(self):
        filename = self.readSaveF.getNameConfig()
        if (filename == "X-W0116-058.txt"):
            self.ui.label_File.setText("X-W0116-058")
        elif (filename == "X-12378-014.txt"):
            self.ui.label_File.setText("X-12378-014")
        elif (filename == "X-10635-050R2.txt"):
            self.ui.label_File.setText("X-10635-050R2")
        else:
            self.ui.label_File.setText(filename)

    def lockmenuBar(self):
        self.ui.actionCamera1.setVisible(False)
        self.ui.actionCamera_2.setVisible(False)
        self.ui.pushButton_auto_manual.setText("Auto")

    def unlockMenuBar(self):
        self.ui.actionCamera1.setVisible(True)
        self.ui.actionCamera_2.setVisible(True)
        self.ui.pushButton_auto_manual.setText("Manual")

    def Startcam(self):  # bat dau camera
        self.fix = False
        self.isCapturing = True
        self.fps = 24
        self.changeStatusFile()
        try:
            if self.isCapturing:
                self.cap1 = cv2.VideoCapture(int(self.readSaveF.getPort()[0]), cv2.CAP_DSHOW)
                self.cap2 = cv2.VideoCapture(int(self.readSaveF.getPort()[1]), cv2.CAP_DSHOW)
                self.Starttimer()
        except:
            pass

    def Starttimer(self):  # thoi gian xu ly hien thi camera
        try:
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.Displayframe)
            self.timer.timeout.connect(self.Displayframe2)
            self.timer.start(1000 / self.fps)
        except:
            pass

    def Displayframe(self):
        try:
            ret, self.frame1 = self.cap1.read()  # frame chưa hình ảnh capture từ camera và ret là gia trị Bolean (nếu frame availble thì true)
            self.frame1 = cv2.cvtColor(self.frame1, cv2.COLOR_BGR2RGB)
            self.frame1 = cv2.resize(src=self.frame1, dsize=(1100, 500))
            img = QtGui.QImage(self.frame1, self.frame1.shape[1],
                               self.frame1.shape[0], QtGui.QImage.Format_RGB888)
            self.pix_cam1 = QtGui.QPixmap.fromImage(img)
            self.ui.label_cam1.setPixmap(self.pix_cam1)
            self.ui.pushButton_camera1.setChecked(True)
            self.ui.pushButton_camera1.setText("Cam ON")
        except:
            self.Stopcam()
            self.ErrorNocam()
        finally:
            if self.updateQlabelNTF <= 1:
                self.sizeChanged.emit()
                self.updateQlabelNTF = +1

    def Displayframe2(self):
        try:
            ret, self.frame2 = self.cap2.read()  # frame chưa hình ảnh capture từ camera và ret là gia trị Bolean (nếu frame availble thì true)
            self.frame2 = cv2.cvtColor(self.frame2, cv2.COLOR_BGR2RGB)
            self.frame2 = cv2.resize(src=self.frame2, dsize=(1100, 500))
            img = QtGui.QImage(self.frame2, self.frame2.shape[1],
                               self.frame2.shape[0], QtGui.QImage.Format_RGB888)
            self.pix_cam2 = QtGui.QPixmap.fromImage(img)
            self.ui.label_cam2.setPixmap(self.pix_cam2)
            self.ui.pushButton_camera1.setChecked(True)
            self.ui.pushButton_camera1.setText("Cam ON")
        except:
            self.Stopcam()
            self.ErrorNocam()

    def Stopcam(self):
        if self.isCapturing:
            self.isCapturing = False
            self.timer.stop()
            try:
                self.cap1.release()
                self.cap2.release()
            except:
                self.ui.label_OK_NG_Final.setStyleSheet("color:red;font: 20pt;Times New Roman;")
                self.ui.label_OK_NG_Final.setText("Configuration file failed.")
            self.ui.pushButton_camera1.setChecked(False)
            self.ui.pushButton_camera1.setText("Cam OFF")

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        if self.isCapturing:
            fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                      "All Files (*);;Text Files (*.txt)", options=options)
            if fileName:
                self.frame = cv2.cvtColor(self.frame1, cv2.COLOR_RGB2BGR)
                cv2.imwrite(fileName + ".jpg", self.frame)

    def setting_parameter(self):
        self.Stopcam()
        dialog = Qmainwindown(self)
        if (self.sender().text() == "Camera 1"):
            self.pix = QPixmap(self.pix_cam1).scaled(640, 480, Qt.KeepAspectRatio,
                                                     Qt.SmoothTransformation)
            self.pixmap = self.pix.scaled(640, 480)
            self.imageforprocess = cv2.resize(src=self.frame1, dsize=(640, 480))
            self.Uisetting_cam1_setting = Setting_Windown(dialog, self.pixmap, self.imageforprocess, "cam1_setting")
        elif (self.sender().text() == "Camera 2"):
            self.pix = QPixmap(self.pix_cam2).scaled(640, 480, Qt.KeepAspectRatio,
                                                     Qt.SmoothTransformation)
            self.pixmap = self.pix.scaled(640, 480)
            self.imageforprocess = cv2.resize(src=self.frame2, dsize=(640, 480))
            self.Uisetting_cam2_setting = Setting_Windown(dialog, self.pixmap, self.imageforprocess, "cam2_setting")
        dialog.show()

    def StartSerial(self):
        self.workThread.start()
        self.ui.pushButton_connectArduino.setChecked(True)
        self.ui.pushButton_connectArduino.setText("Serial OFF")

    def StopSerial(self):
        self.workThread.terminate()
        self.ui.pushButton_connectArduino.setChecked(False)
        self.ui.pushButton_connectArduino.setText("Serial ON")

    def deleteLater(self):
        if self.isCapturing:
            self.timer.stop()
            self.cap1.release()
            self.cap2.release()
            cv2.destroyAllWindows()
        self.close()

    def clearQuantity(self):
        self.ui.label_result_QuantityTotal.setText("0")
        self.ui.label_resultOK_Total.setText("0")
        self.ui.label_resultNG_total.setText("0")
        self.ui.label_ResultOK_Cam1.setText("0")
        self.ui.label_ResultNG_cam1.setText("0")
        self.ui.label_ResultOk_cam2.setText("0")
        self.ui.label_ResultNG_cam2.setText("0")
        self.quantity_OK_cam = self.quantity_OK_cam1 = self.quantity_OK_cam2 = 0
        self.quantity_NG_cam = self.quantity_NG_cam1 = self.quantity_NG_cam2 = 0
        self.quantity_total = 0

    @pyqtSlot()
    def xoamang_xuatfile(self):
        f = open(os.path.join(root, 'data', 'xuat_file_cam.txt'), "w", encoding='utf-8')
        # Ghi dữ liệu lên file
        f.write("")
        # Close opened file
        f.close()
        f2 = open(os.path.join(root, 'data', 'xuat_file_cam.txt'), "w", encoding='utf-8')
        # Ghi dữ liệu lên file
        f2.write("")
        # Close opened file
        f2.close()

    def xuat_file_cam(self):
        try:
            for j in range(len(self.xuat_mang_kq)):
                f = open(os.path.join(root, 'data', 'xuat_file_cam.txt'), "a", encoding='utf-8')
                # Ghi dữ liệu lên file
                f.write(str(self.xuat_mang_kq[j]) + " ")
                # Close opened file

                f.close()
            f = open(os.path.join(root, 'data', 'xuat_file_cam.txt'), "a", encoding='utf-8')
            # Ghi dữ liệu lên file
            f.write("\n")
            f.close()
            for j in range(len(self.xuat_mang_so)):
                f1 = open(os.path.join(root, 'data', 'xuat_file_cam.txt'), "a", encoding='utf-8')
                # Ghi dữ liệu lên file
                f1.write("%.2f" % (self.xuat_mang_so[j]) + " ")
                # Close opened file

                f1.close()
            f1 = open(os.path.join(root, 'data', 'xuat_file_cam.txt'), "a", encoding='utf-8')
            # Ghi dữ liệu lên file
            f1.write("\n")
            f1.close()
        except:
            pass

    def closeEvent(self, event):
        self.Save_dataArd()
        close = QtWidgets.QMessageBox.question(self,
                                               "QUIT CAM",
                                               "Are you sure want Exist ?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.Yes:
            self.workThread.terminate()
            event.accept()
        else:
            event.ignore()

    @pyqtSlot()
    def ErrorNoArd(self):
        self.ui.pushButton_connectArduino.setChecked(False)
        msg = QMessageBox()
        msg.setWindowTitle("Arduino UNO not found")
        msg.setText(" Please Connect Arduino UNO to Computer! ")
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Retry)
        x = msg.exec_()

    def ErrorNocam(self):
        self.isCapturing = False
        msg = QMessageBox()
        msg.setWindowTitle("CAMERA not found")
        msg.setText(" Please Connect CAMERA to Computer! ")
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Retry)
        x = msg.exec_()

    def getResult(self):
        try:
            self.xuat_mang_so = []
            self.xuat_mang_kq = []
            self.quantity_total += 1
            dialog1 = QMainWindow(self)
            dialog2 = QMainWindow(self)
            self.imageforprocess1 = cv2.resize(src=self.frame1, dsize=(640, 480))
            self.imageforprocess2 = cv2.resize(src=self.frame2, dsize=(640, 480))
            if self.fix == False:
                self.Uisetting_cam11 = Setting_Windown(dialog1, self.pix_cam1, self.imageforprocess1, "cam1_setting")
                self.Uisetting_cam22 = Setting_Windown(dialog2, self.pix_cam2, self.imageforprocess2, "cam2_setting")
                self.fix = True
            else:
                self.Uisetting_cam11.image = self.pix_cam1
                self.imageforprocess1 = cv2.resize(src=self.frame1, dsize=(640, 480))
                self.Uisetting_cam11.frame = self.imageforprocess1
                self.Uisetting_cam22.image = self.pix_cam2
                self.imageforprocess2 = cv2.resize(src=self.frame2, dsize=(640, 480))
                self.Uisetting_cam22.frame = self.imageforprocess2

            if self.isCapturing:
                result_cam1 = self.Uisetting_cam11.GetResult()
                for i in range(len(result_cam1[0])):
                    self.xuat_mang_so.append(result_cam1[0][i])
                    self.xuat_mang_kq.append(result_cam1[2][i])
                result_cam2 = self.Uisetting_cam22.GetResult()
                for i in range(len(result_cam2[0])):
                    self.xuat_mang_so.append(result_cam2[0][i])
                    self.xuat_mang_kq.append(result_cam2[2][i])
            else:
                return
            self.ui.label_result_QuantityTotal.setText(str(self.quantity_total))
            if result_cam1 == False or result_cam2 == False:
                self.ui.label_OK_NG_Final.setStyleSheet("color:blue;font: 40pt;Times New Roman;")
                self.ui.label_OK_NG_Final.setText("No file")
            if result_cam1 != False:
                if result_cam1[1] == True:
                    self.quantity_OK_cam1 += 1
                    self.ui.label_ResultOK_Cam1.setText(str(self.quantity_OK_cam1))
                    if self.quantity_total % 2 != 0:
                        self.ui.label_ntfCam1.setStyleSheet("color:blue;font: 20pt;Times New Roman;")
                        self.ui.label_ntfCam1.setText("OK")
                    if self.quantity_total % 2 == 0:
                        self.ui.label_ntfCam1.setStyleSheet("color:blue;font: 20pt;Times New Roman;")
                        self.ui.label_ntfCam1.setText("OK.")
                    if len(result_cam1[0]) >= 1:
                        if result_cam1[2][0] == "OK":
                            self.ui.label_cam1_result1.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                            self.ui.label_cam1_result1.setText("%.2f" % (result_cam1[0][0]))
                        else:
                            self.ui.label_cam1_result1.setStyleSheet("color:red;font: 13pt;Times New Roman;")
                            self.ui.label_cam1_result1.setText("%.2f" % (result_cam1[0][0]))
                    if len(result_cam1[0]) < 1:
                        self.ui.label_cam1_result1.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                        self.ui.label_cam1_result1.setText("No Pin1")
                    if len(result_cam1[0]) >= 2:
                        if result_cam1[2][1] == "OK":
                            self.ui.label_cam1_result2.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                            self.ui.label_cam1_result2.setText("%.2f" % (result_cam1[0][1]))
                        else:
                            self.ui.label_cam1_result2.setStyleSheet("color:red;font: 13pt;Times New Roman;")
                            self.ui.label_cam1_result2.setText("%.2f" % (result_cam1[0][1]))
                    if len(result_cam1[0]) < 2:
                        self.ui.label_cam1_result2.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                        self.ui.label_cam1_result2.setText("No Pin2")
                    if len(result_cam1[0]) >= 3:
                        if result_cam1[2][2] == "OK":
                            self.ui.label_cam1_result3.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                            self.ui.label_cam1_result3.setText("%.2f" % (result_cam1[0][2]))
                        else:
                            self.ui.label_cam1_result3.setStyleSheet("color:red;font: 13pt;Times New Roman;")
                            self.ui.label_cam1_result3.setText("%.2f" % (result_cam1[0][2]))
                    if len(result_cam1[0]) < 3:
                        self.ui.label_cam1_result3.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                        self.ui.label_cam1_result3.setText("No Pin3")
                    if len(result_cam1[0]) >= 4:
                        if result_cam1[2][3] == "OK":
                            self.ui.label_cam1_result4.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                            self.ui.label_cam1_result4.setText("%.2f" % (result_cam1[0][3]))
                        else:
                            self.ui.label_cam1_result4.setStyleSheet("color:red;font: 13pt;Times New Roman;")
                            self.ui.label_cam1_result4.setText("%.2f" % (result_cam1[0][3]))
                    if len(result_cam1[0]) < 4:
                        self.ui.label_cam1_result4.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                        self.ui.label_cam1_result4.setText("No Pin4")
                    if len(result_cam1[0]) >= 5:
                        if result_cam1[2][4] == "OK":
                            self.ui.label_cam1_result5.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                            self.ui.label_cam1_result5.setText("%.2f" % (result_cam1[0][4]))
                        else:
                            self.ui.label_cam1_result5.setStyleSheet("color:red;font: 13pt;Times New Roman;")
                            self.ui.label_cam1_result5.setText("%.2f" % (result_cam1[0][4]))
                    if len(result_cam1[0]) < 5:
                        self.ui.label_cam1_result5.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                        self.ui.label_cam1_result5.setText("No Pin5")
                    if len(result_cam1[0]) >= 6:
                        if result_cam1[2][5] == "OK":
                            self.ui.label_cam1_result6.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                            self.ui.label_cam1_result6.setText("%.2f" % (result_cam1[0][5]))
                        else:
                            self.ui.label_cam1_result6.setStyleSheet("color:red;font: 13pt;Times New Roman;")
                            self.ui.label_cam1_result6.setText("%.2f" % (result_cam1[0][5]))
                    if len(result_cam1[0]) < 6:
                        self.ui.label_cam1_result6.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                        self.ui.label_cam1_result6.setText("No Pin6")
                elif result_cam1[1] == False:
                    self.quantity_NG_cam1 += 1
                    self.ui.label_ResultNG_cam1.setText(str(self.quantity_NG_cam1))
                    if self.quantity_total % 2 != 0:
                        self.ui.label_ntfCam1.setStyleSheet("color:red;font: 20pt;Times New Roman;")
                        self.ui.label_ntfCam1.setText("NG")
                    if self.quantity_total % 2 == 0:
                        self.ui.label_ntfCam1.setStyleSheet("color:red;font: 20pt;Times New Roman;")
                        self.ui.label_ntfCam1.setText("NG.")
                    if len(result_cam1[0]) >= 1:
                        if result_cam1[2][0] == "OK":
                            self.ui.label_cam1_result1.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                            self.ui.label_cam1_result1.setText("%.2f" % (result_cam1[0][0]))
                        else:
                            self.ui.label_cam1_result1.setStyleSheet("color:red;font: 13pt;Times New Roman;")
                            self.ui.label_cam1_result1.setText("%.2f" % (result_cam1[0][0]))
                    if len(result_cam1[0]) < 1:
                        self.ui.label_cam1_result1.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                        self.ui.label_cam1_result1.setText("No Pin1")
                    if len(result_cam1[0]) >= 2:
                        if result_cam1[2][1] == "OK":
                            self.ui.label_cam1_result2.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                            self.ui.label_cam1_result2.setText("%.2f" % (result_cam1[0][1]))
                        else:
                            self.ui.label_cam1_result2.setStyleSheet("color:red;font: 13pt;Times New Roman;")
                            self.ui.label_cam1_result2.setText("%.2f" % (result_cam1[0][1]))
                    if len(result_cam1[0]) < 2:
                        self.ui.label_cam1_result2.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                        self.ui.label_cam1_result2.setText("No Pin2")
                    if len(result_cam1[0]) >= 3:
                        if result_cam1[2][2] == "OK":
                            self.ui.label_cam1_result3.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                            self.ui.label_cam1_result3.setText("%.2f" % (result_cam1[0][2]))
                        else:
                            self.ui.label_cam1_result3.setStyleSheet("color:red;font: 13pt;Times New Roman;")
                            self.ui.label_cam1_result3.setText("%.2f" % (result_cam1[0][2]))
                    if len(result_cam1[0]) < 3:
                        self.ui.label_cam1_result3.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                        self.ui.label_cam1_result3.setText("No Pin3")
                    if len(result_cam1[0]) >= 4:
                        if result_cam1[2][3] == "OK":
                            self.ui.label_cam1_result4.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                            self.ui.label_cam1_result4.setText("%.2f" % (result_cam1[0][3]))
                        else:
                            self.ui.label_cam1_result4.setStyleSheet("color:red;font: 13pt;Times New Roman;")
                            self.ui.label_cam1_result4.setText("%.2f" % (result_cam1[0][3]))
                    if len(result_cam1[0]) < 4:
                        self.ui.label_cam1_result4.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                        self.ui.label_cam1_result4.setText("No Pin4")
                    if len(result_cam1[0]) >= 5:
                        if result_cam1[2][4] == "OK":
                            self.ui.label_cam1_result5.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                            self.ui.label_cam1_result5.setText("%.2f" % (result_cam1[0][4]))
                        else:
                            self.ui.label_cam1_result5.setStyleSheet("color:red;font: 13pt;Times New Roman;")
                            self.ui.label_cam1_result5.setText("%.2f" % (result_cam1[0][4]))
                    if len(result_cam1[0]) < 5:
                        self.ui.label_cam1_result5.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                        self.ui.label_cam1_result5.setText("No Pin5")
                    if len(result_cam1[0]) >= 6:
                        if result_cam1[2][5] == "OK":
                            self.ui.label_cam1_result6.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                            self.ui.label_cam1_result6.setText("%.2f" % (result_cam1[0][5]))
                        else:
                            self.ui.label_cam1_result6.setStyleSheet("color:red;font: 13pt;Times New Roman;")
                            self.ui.label_cam1_result6.setText("%.2f" % (result_cam1[0][5]))
                    if len(result_cam1[0]) < 6:
                        self.ui.label_cam1_result6.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                        self.ui.label_cam1_result6.setText("No Pin6")

            if result_cam2 != False:
                if result_cam2[1] == True:
                    self.quantity_OK_cam2 += 1
                    self.ui.label_ResultOk_cam2.setText(str(self.quantity_OK_cam2))
                    if self.quantity_total % 2 != 0:
                        self.ui.label_ntfCam2.setStyleSheet("color:blue;font: 20pt;Times New Roman;")
                        self.ui.label_ntfCam2.setText("OK")
                    if self.quantity_total % 2 == 0:
                        self.ui.label_ntfCam2.setStyleSheet("color:blue;font: 20pt;Times New Roman;")
                        self.ui.label_ntfCam2.setText("OK.")
                    if len(result_cam2[0]) >= 1:
                        if result_cam2[2][0] == "OK":
                            self.ui.label_cam2_result1.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                            self.ui.label_cam2_result1.setText("%.2f" % (result_cam2[0][0]))
                        else:
                            self.ui.label_cam2_result1.setStyleSheet("color:red;font: 13pt;Times New Roman;")
                            self.ui.label_cam2_result1.setText("%.2f" % (result_cam2[0][0]))
                    if len(result_cam2[0]) < 1:
                        self.ui.label_cam2_result1.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                        self.ui.label_cam2_result1.setText("No Pin1")
                    if len(result_cam2[0]) >= 2:
                        if result_cam2[2][1] == "OK":
                            self.ui.label_cam2_result2.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                            self.ui.label_cam2_result2.setText("%.2f" % (result_cam2[0][1]))
                        else:
                            self.ui.label_cam2_result2.setStyleSheet("color:red;font: 13pt;Times New Roman;")
                            self.ui.label_cam2_result2.setText("%.2f" % (result_cam2[0][1]))
                    if len(result_cam2[0]) < 2:
                        self.ui.label_cam2_result2.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                        self.ui.label_cam2_result2.setText("No Pin2")
                    if len(result_cam2[0]) >= 3:
                        if result_cam2[2][2] == "OK":
                            self.ui.label_cam2_result3.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                            self.ui.label_cam2_result3.setText("%.2f" % (result_cam2[0][2]))
                        else:
                            self.ui.label_cam2_result3.setStyleSheet("color:red;font: 13pt;Times New Roman;")
                            self.ui.label_cam2_result3.setText("%.2f" % (result_cam2[0][2]))
                    if len(result_cam2[0]) < 3:
                        self.ui.label_cam2_result3.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                        self.ui.label_cam2_result3.setText("No Pin3")
                    if len(result_cam2[0]) >= 4:
                        if result_cam2[2][3] == "OK":
                            self.ui.label_cam2_result4.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                            self.ui.label_cam2_result4.setText("%.2f" % (result_cam2[0][3]))
                        else:
                            self.ui.label_cam2_result4.setStyleSheet("color:red;font: 13pt;Times New Roman;")
                            self.ui.label_cam2_result4.setText("%.2f" % (result_cam2[0][3]))
                    if len(result_cam2[0]) < 4:
                        self.ui.label_cam2_result4.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                        self.ui.label_cam2_result4.setText("No Pin4")
                    if len(result_cam2[0]) >= 5:
                        if result_cam2[2][4] == "OK":
                            self.ui.label_cam2_result5.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                            self.ui.label_cam2_result5.setText("%.2f" % (result_cam2[0][4]))
                        else:
                            self.ui.label_cam2_result5.setStyleSheet("color:red;font: 13pt;Times New Roman;")
                            self.ui.label_cam2_result5.setText("%.2f" % (result_cam2[0][4]))
                    if len(result_cam2[0]) < 5:
                        self.ui.label_cam2_result5.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                        self.ui.label_cam2_result5.setText("No Pin5")
                    if len(result_cam2[0]) >= 6:
                        if result_cam2[2][5] == "OK":
                            self.ui.label_cam2_result6.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                            self.ui.label_cam2_result6.setText("%.2f" % (result_cam2[0][5]))
                        else:
                            self.ui.label_cam2_result6.setStyleSheet("color:red;font: 13pt;Times New Roman;")
                            self.ui.label_cam2_result6.setText("%.2f" % (result_cam2[0][5]))
                    if len(result_cam2[0]) < 6:
                        self.ui.label_cam2_result6.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                        self.ui.label_cam2_result6.setText("No Pin6")
                elif result_cam2[1] == False:
                    self.quantity_NG_cam2 += 1
                    self.ui.label_ResultNG_cam2.setText(str(self.quantity_NG_cam2))
                    if self.quantity_total % 2 != 0:
                        self.ui.label_ntfCam2.setStyleSheet("color:red;font: 20pt;Times New Roman;")
                        self.ui.label_ntfCam2.setText("NG")
                    if self.quantity_total % 2 == 0:
                        self.ui.label_ntfCam2.setStyleSheet("color:red;font: 20pt;Times New Roman;")
                        self.ui.label_ntfCam2.setText("NG.")
                    if len(result_cam2[0]) >= 1:
                        if result_cam2[2][0] == "OK":
                            self.ui.label_cam2_result1.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                            self.ui.label_cam2_result1.setText("%.2f" % (result_cam2[0][0]))
                        else:
                            self.ui.label_cam2_result1.setStyleSheet("color:red;font: 13pt;Times New Roman;")
                            self.ui.label_cam2_result1.setText("%.2f" % (result_cam2[0][0]))
                    if len(result_cam2[0]) < 1:
                        self.ui.label_cam2_result1.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                        self.ui.label_cam2_result1.setText("No Pin1")
                    if len(result_cam2[0]) >= 2:
                        if result_cam2[2][1] == "OK":
                            self.ui.label_cam2_result2.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                            self.ui.label_cam2_result2.setText("%.2f" % (result_cam2[0][1]))
                        else:
                            self.ui.label_cam2_result2.setStyleSheet("color:red;font: 13pt;Times New Roman;")
                            self.ui.label_cam2_result2.setText("%.2f" % (result_cam2[0][1]))
                    if len(result_cam2[0]) < 2:
                        self.ui.label_cam2_result2.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                        self.ui.label_cam2_result2.setText("No Pin2")
                    if len(result_cam2[0]) >= 3:
                        if result_cam2[2][2] == "OK":
                            self.ui.label_cam2_result3.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                            self.ui.label_cam2_result3.setText("%.2f" % (result_cam2[0][2]))
                        else:
                            self.ui.label_cam2_result3.setStyleSheet("color:red;font: 13pt;Times New Roman;")
                            self.ui.label_cam2_result3.setText("%.2f" % (result_cam2[0][2]))
                    if len(result_cam2[0]) < 3:
                        self.ui.label_cam2_result3.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                        self.ui.label_cam2_result3.setText("No Pin3")
                    if len(result_cam2[0]) >= 4:
                        if result_cam2[2][3] == "OK":
                            self.ui.label_cam2_result4.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                            self.ui.label_cam2_result4.setText("%.2f" % (result_cam2[0][3]))
                        else:
                            self.ui.label_cam2_result4.setStyleSheet("color:red;font: 13pt;Times New Roman;")
                            self.ui.label_cam2_result4.setText("%.2f" % (result_cam2[0][3]))
                    if len(result_cam2[0]) < 4:
                        self.ui.label_cam2_result4.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                        self.ui.label_cam2_result4.setText("No Pin4")
                    if len(result_cam2[0]) >= 5:
                        if result_cam2[2][4] == "OK":
                            self.ui.label_cam2_result5.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                            self.ui.label_cam2_result5.setText("%.2f" % (result_cam2[0][4]))
                        else:
                            self.ui.label_cam2_result5.setStyleSheet("color:red;font: 13pt;Times New Roman;")
                            self.ui.label_cam2_result5.setText("%.2f" % (result_cam2[0][4]))
                    if len(result_cam2[0]) < 5:
                        self.ui.label_cam2_result5.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                        self.ui.label_cam2_result5.setText("No Pin5")
                    if len(result_cam2[0]) >= 6:
                        if result_cam2[2][5] == "OK":
                            self.ui.label_cam2_result6.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                            self.ui.label_cam2_result6.setText("%.2f" % (result_cam2[0][5]))
                        else:
                            self.ui.label_cam2_result6.setStyleSheet("color:red;font: 13pt;Times New Roman;")
                            self.ui.label_cam2_result6.setText("%.2f" % (result_cam2[0][5]))
                    if len(result_cam2[0]) < 6:
                        self.ui.label_cam2_result6.setStyleSheet("color:white;font: 13pt;Times New Roman;")
                        self.ui.label_cam2_result6.setText("No Pin6")
            if result_cam1 != False and result_cam2 != False:
                if result_cam1[1] == True and result_cam2[1] == True:
                    self.workThread.Send_OK("8")
                    self.quantity_OK_cam += 1
                    self.ui.label_resultOK_Total.setText(str(self.quantity_OK_cam))
                    if self.quantity_total % 2 != 0:
                        self.ui.label_OK_NG_Final.setStyleSheet("color:blue;font: 70pt;Times New Roman;")
                        self.ui.label_OK_NG_Final.setText("OK")
                    if self.quantity_total % 2 == 0:
                        self.ui.label_OK_NG_Final.setStyleSheet("color:blue;font: 70pt;Times New Roman;")
                        self.ui.label_OK_NG_Final.setText("OK.")
                else:
                    self.quantity_NG_cam += 1
                    self.ui.label_resultNG_total.setText(str(self.quantity_NG_cam))
                    if self.quantity_total % 2 != 0:
                        self.ui.label_OK_NG_Final.setStyleSheet("color:red;font: 70pt;Times New Roman;")
                        self.ui.label_OK_NG_Final.setText("NG")
                    if self.quantity_total % 2 == 0:
                        self.ui.label_OK_NG_Final.setStyleSheet("color:red;font: 70pt;Times New Roman;")
                        self.ui.label_OK_NG_Final.setText("NG.")
                QtCore.QCoreApplication.processEvents()
            self.xuat_file_cam()
        except:
            self.ui.label_OK_NG_Final.setStyleSheet("color:red;font: 20pt;Times New Roman;")
            self.ui.label_OK_NG_Final.setText("Setting file error")

    def openDocument(self):
        fileH = self.absoluteUrlFile = os.path.dirname(__file__)
        os.system("start EXCEL.EXE " + fileH + "Help.xlsx")

    def fileData1(self):
        url = os.path.join(root, 'data', 'X-W0116-058.txt').replace(".txt", "")
        url = self.readSaveF.formatURl(url)
        self.readSaveF.writeFileConfig(url, None)
        self.ui.label_File.setText("X-W0116-058R1")

    def fileData2(self):
        url = os.path.join(root, 'data', 'X-12378-014.txt').replace(".txt", "")
        url = self.readSaveF.formatURl(url)
        self.readSaveF.writeFileConfig(url, None)
        self.ui.label_File.setText("X-12378-014")

    def fileData3(self):
        url = os.path.join(root, 'data', 'X-10635-050R2.txt').replace(".txt", "")
        url = self.readSaveF.formatURl(url)
        self.readSaveF.writeFileConfig(url, None)
        self.ui.label_File.setText("X-10635-050R2")

    def Arduino_setting(self):
        dialog = QDialog1(self)
        self.UiArd = Ui_Dialog()
        self.UiArd.setupUi(dialog)
        dialog.close_arduino.connect(self.PinoutArd)
        if self.data_arduino[3] == 1:
            self.UiArd.radioButton_6.setChecked(True)
        if self.data_arduino[4] == 1:
            self.UiArd.radioButton_7.setChecked(True)
        if self.data_arduino[5] == 1:
            self.UiArd.radioButton_9.setChecked(True)
        if self.data_arduino[6] == 1:
            self.UiArd.radioButton_10.setChecked(True)
        if self.data_arduino[7] == 1:
            self.UiArd.radioButton_11.setChecked(True)
        if self.data_arduino[8] == 1:
            self.UiArd.radioButton_12.setChecked(True)
        dialog.exec_()

    def PinoutArd(self):
        if self.UiArd.radioButton_6.isChecked():
            self.data_arduino[3] = 1
        else:
            self.data_arduino[3] = 0
        if self.UiArd.radioButton_7.isChecked():
            self.data_arduino[4] = 1
        else:
            self.data_arduino[4] = 0
        if self.UiArd.radioButton_9.isChecked():
            self.data_arduino[5] = 1
        else:
            self.data_arduino[5] = 0
        if self.UiArd.radioButton_10.isChecked():
            self.data_arduino[6] = 1
        else:
            self.data_arduino[6] = 0
        if self.UiArd.radioButton_11.isChecked():
            self.data_arduino[7] = 1
        else:
            self.data_arduino[7] = 0
        if self.UiArd.radioButton_12.isChecked():
            self.data_arduino[8] = 1
        else:
            self.data_arduino[8] = 0

    def Inital_dataArd(self):
        self.conn = sqlite3.connect(os.path.join(root, 'parameter', 'Data_parameter.db'))
        cursor = self.conn.execute("SELECT count(*) as Quatity from Ard")
        for row in cursor:
            quality = row[0]
        if quality != 0:
            cursor = self.conn.execute("SELECT * from Ard")
            for row in cursor:
                for i in range(1, 10):
                    self.data_arduino.append(row[i])
        self.conn.close()

    def Save_dataArd(self):
        conn = sqlite3.connect(os.path.join(root, 'parameter', 'Data_parameter.db'))
        conn.execute("DELETE FROM Ard")
        conn.execute("INSERT INTO  Ard (Pin6,Pin7,Pin9,Pin10,Pin11,Pin12) VALUES (?,?,?,?,?,?);",
                     (self.data_arduino[3],
                      self.data_arduino[4],
                      self.data_arduino[5], self.data_arduino[6], self.data_arduino[7], self.data_arduino[8]))
        conn.commit()
        self.conn.close()

    def Aboutme(self):
        About = QDialog(self)
        self.intro = Ui_Intro()
        self.intro.setupUi(About)
        About.exec()

    def resizeEvent(self, event):
        self.sizeChanged.emit()
        super().resizeEvent(event)


class WorkThread(QThread):
    letdoit = pyqtSignal()
    Error = pyqtSignal()
    sp1 = pyqtSignal()
    sp2 = pyqtSignal()
    sp3 = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.check = False
        self.check1 = False
        self.readFproductCode = SaveAndRead("cam1_setting")

    def run(self):
        try:
            while (1):
                ports = serial.tools.list_ports.comports(include_links=False)
                if len(ports) != 0 and self.check == False:
                    for port in ports:
                        self.ser = serial.Serial(port.device)
                        if self.ser.isOpen():
                            self.ser.close()
                            self.ser = serial.Serial(port.device, 9600, timeout=2)
                            self.check = True
                            self.check1 = True
                data = self.ser.readline().decode("utf-8").strip('\n').strip('\r')
                lastDateModified, dateModified = self.readFproductCode.getDateModified()
                if (lastDateModified != dateModified):
                    self.readFproductCode.writeFileConfig(None, dateModified)
                    self.ProductCode = self.readFproductCode.getFProductCode()
                    if self.ProductCode == "0":
                        self.Send_Pcode("3")
                        self.sp1.emit()
                    if self.ProductCode == "1":
                        self.Send_Pcode("4")
                        self.sp2.emit()
                    if self.ProductCode == "2":
                        self.Send_Pcode("5")
                        self.sp3.emit()
                if data == "SenSor In":
                    self.letdoit.emit()
        except:
            self.Error.emit()
            self.check = False
            if self.check1:
                self.ser.close()

    def Send_NG(self, data_arduino):
        try:
            Sending = bytearray(data_arduino)
            self.ser.write(Sending)
        except:
            self.Error.emit()

    def Send_OK(self, ok):
        try:
            self.ser.write(ok.encode())
        except:
            self.Error.emit()

    def Send_Pcode(self, productcode):
        # try:
        self.ser.write(productcode.encode())
    # except:
    #     self.Error.emit()


class QDialog1(QDialog):
    close_arduino = pyqtSignal()

    @pyqtSlot()
    def closeEvent(self, event):
        self.close_arduino.emit()

class Qmainwindown(QMainWindow):
    close_setting= pyqtSignal()

    @pyqtSlot()
    def closeEvent(self, event):
        print("setting close")
        self.close_setting.emit()

if __name__ == "__main__":
    import sys

    app1 = QApplication(sys.argv)
    ban_quyen().checkdate()
    try:
        ktserial = kt_serial_disk().test_serial()
        lenkey = len(ktserial)
        keyS = keyMenu().readKey()[:lenkey]
    except:
        ktserial = "1"
        keyS = "2"
    if (keyS == ktserial):
        f = Foster_app()
        f.showMaximized()
        sys.exit(app1.exec_())
    else:
        key = key_menu()
        if key.exec_() == QDialog.Accepted:
            f = Foster_app()
            f.showMaximized()
            sys.exit(app1.exec_())

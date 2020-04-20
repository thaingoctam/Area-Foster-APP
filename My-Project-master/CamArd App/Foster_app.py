# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
from PyQt5.QtGui import *
from Settingwindown import *
from Mainwindown import *
from Arduino import*
from DrawRect import *
from about import *
from os.path import expanduser
import cv2
import imutils
import sys
import serial
import threading
import time
import serial.tools.list_ports
import sqlite3
import os
class Foster_app(QMainWindow):
    SenddatatoArduino_NG = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.timer = QtCore.QTimer()
        self.data_arduino=[]
        self.isCapturing = False
        self.noPort=False
        self.quantity_OK = 0
        self.quantity_NG = 0
        self.quantity_total = 0
        self.workThread = WorkThread()
        self.Inital_dataArd()
        self.pix=QtGui.QPixmap("Icon/demo.jpg")
        self.imageforprocess=cv2.imread("Icon/demo.jpg")
        self.ui.actionParameter.triggered.connect(self.setting_parameter)
        self.ui.actionArduino_Uno.triggered.connect(self.Arduino_setting)
        self.ui.actionDocumment.triggered.connect(self.openDocument)
        self.ui.actionAbout.triggered.connect(self.Aboutme)
        self.ui.actionSave.triggered.connect(self.saveFileDialog)
        self.ui.pushButton_cameraON.clicked.connect(self.Startcam)
        self.ui.pushButton_cameraOFF.clicked.connect(self.Stopcam)
        self.ui.pushButton_Clear.clicked.connect(self.clearQuantity)
        self.ui.pushButton_cameraOFF.clicked.connect(self.Stopcam)
        self.ui.actionExits.triggered.connect(self.deleteLater)
        self.ui.pushButton_connectArduino.clicked.connect(self.Serial)
        self.workThread.letdoit.connect(self.getResult)
        self.workThread.Error.connect(self.ErrorNoArd)
        self.pix1 = QtGui.QPixmap("Icon/Nocam.jpg")
        self.ui.label_videocam.setPixmap(self.pix1)
        self.show()

    def Startcam(self):
        if self.isCapturing==False:
           self.isCapturing = True
           self.testcam = True
           self.fps = 24
           self.cap = cv2.VideoCapture(0)
           self.ith_frame = 1
           self.Starttimmer()
           self.show()

    def Starttimmer(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.Displayframe)
        self.timer.start(1000./self.fps)

    def Displayframe(self):
        try:
            ret, self.frame= self.cap.read()
            self.imageforprocess=self.frame
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            img = QtGui.QImage(self.frame, self.frame.shape[1],self.frame.shape[0], QtGui.QImage.Format_RGB888)
            self.pix = QtGui.QPixmap.fromImage(img)
            self.ui.label_videocam.setPixmap(self.pix)
        except:
            self.ErrorNocam()
            self.testcam = False

    def Stopcam(self):
        if self.isCapturing:
           self.isCapturing= False
           self.cap.release()
           self.timer.stop()
           cv2.destroyAllWindows()
           self.ui.label_videocam.setPixmap(self.pix1)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        if self.isCapturing:
            fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
            if fileName:
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
                cv2.imwrite(fileName+".jpg", self.frame)

    def setting_parameter(self):
        dialog = QDialog(self)
        self.Uisetting=Setting_Windown(dialog,self.pix,self.imageforprocess)
        dialog.exec_()

    def Serial(self):
        self.workThread.start()
        if self.ui.pushButton_connectArduino.isChecked():
            self.workThread.startSerial()
            self.ui.pushButton_connectArduino.setStyleSheet("background-color:green;border: 1px solid #00B674;border-radius:6px;")
            self.ui.pushButton_connectArduino.setText("Serial Conected")
        else:
            self.workThread.stopSerial()
            self.ui.pushButton_connectArduino.setStyleSheet("background-color: white;border: 1px solid #00B674;border-radius:6px;")
            self.ui.pushButton_connectArduino.setText("Serial Disconnected")


    def deleteLater(self):
        if self.isCapturing:
            self.timer.stop()
            self.cap.release()
            cv2.destroyAllWindows()
        self.close()

    def clearQuantity(self):
        self.ui.label_result_Quantity.setText("0")
        self.ui.label_OK.setText("0")
        self.ui.label_NG.setText("0")
        self.quantity_OK=0
        self.quantity_NG=0
        self.quantity_total=0

    @pyqtSlot()
    def closeEvent(self, event):
        self.Save_dataArd()
        close = QtWidgets.QMessageBox.question(self,
                                               "QUIT CAM",
                                               "Are you sure want Exist ?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    @pyqtSlot()
    def ErrorNoArd(self):
        self.ui.pushButton_connectArduino.setChecked(False)
        self.ui.pushButton_connectArduino.setStyleSheet("background-color: white;border: 1px solid #00B674;border-radius:6px;")
        self.ui.pushButton_connectArduino.setText("Serial Disconnected")
        msg = QMessageBox()
        msg.setWindowTitle("Arduino UNO not found")
        msg.setText(" Please Connect Arduino UNO to Computer! ")
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Retry)
        x = msg.exec_()

    def ErrorNocam(self):
        if self.testcam:
            self.isCapturing=False
            msg = QMessageBox()
            msg.setWindowTitle("CAMERA not found")
            msg.setText(" Please Connect CAMERA to Computer! ")
            msg.setIcon(QMessageBox.Critical)
            msg.setStandardButtons(QMessageBox.Retry)
            x = msg.exec_()

    def getResult(self):
        self.quantity_total+=1
        dialog = QDialog(self)
        result=False
        self.Uisetting = Setting_Windown(dialog, self.pix, self.imageforprocess)
        if self.isCapturing:
           result=self.Uisetting.GetResult()
        else:
            return
        self.ui.label_result_Quantity.setText(str(self.quantity_total))

        if result:
            self.ui.label_Mainresult.setStyleSheet("color:blue;font: 90pt;Times New Roman;")
            self.ui.label_Mainresult.setText("OK")
            self.quantity_OK+=1
            self.ui.label_OK.setText(str(self.quantity_OK))
        else:
            self.ui.label_Mainresult.setStyleSheet("color:red;font: 90pt;Times New Roman;")
            self.ui.label_Mainresult.setText("NG")
            self.quantity_NG+=1
            self.ui.label_NG.setText(str(self.quantity_NG))
            self.workThread.Send_NG(self.data_arduino)

    def openDocument(self):
        os.system("start EXCEL.EXE Help.xlsx")

    def Arduino_setting(self):
        dialog = QDialog1(self)
        self.UiArd=Ui_Dialog()
        self.UiArd.setupUi(dialog)
        dialog.close_arduino.connect(self.PinoutArd)
        if self.data_arduino[0]==1:
            self.UiArd.radioButton_3.setChecked(True)
        if self.data_arduino[1]==1:
            self.UiArd.radioButton_4.setChecked(True)
        if self.data_arduino[2]==1:
            self.UiArd.radioButton_5.setChecked(True)
        if self.data_arduino[3]==1:
            self.UiArd.radioButton_6.setChecked(True)
        if self.data_arduino[4]==1:
            self.UiArd.radioButton_7.setChecked(True)
        if self.data_arduino[5]==1:
            self.UiArd.radioButton_9.setChecked(True)
        if self.data_arduino[6]==1:
            self.UiArd.radioButton_10.setChecked(True)
        if self.data_arduino[7]==1:
            self.UiArd.radioButton_11.setChecked(True)
        if self.data_arduino[8]==1:
            self.UiArd.radioButton_12.setChecked(True)
        dialog.exec_()
    def PinoutArd(self):
        if self.UiArd.radioButton_3.isChecked():
            self.data_arduino[0]=1
        else:
            self.data_arduino[0]=0
        if self.UiArd.radioButton_4.isChecked():
            self.data_arduino[1]=1
        else:
            self.data_arduino[1]=0
        if self.UiArd.radioButton_5.isChecked():
            self.data_arduino[2]=1
        else:
            self.data_arduino[2]=0
        if self.UiArd.radioButton_6.isChecked():
            self.data_arduino[3]=1
        else:
            self.data_arduino[3]=0
        if self.UiArd.radioButton_7.isChecked():
            self.data_arduino[4]=1
        else:
            self.data_arduino[4]=0
        if self.UiArd.radioButton_9.isChecked():
            self.data_arduino[5]=1
        else:
            self.data_arduino[5]=0
        if self.UiArd.radioButton_10.isChecked():
            self.data_arduino[6]=1
        else:
            self.data_arduino[6]=0
        if self.UiArd.radioButton_11.isChecked():
            self.data_arduino[7]=1
        else:
            self.data_arduino[7]=0
        if self.UiArd.radioButton_12.isChecked():
            self.data_arduino[8] = 1
        else:
            self.data_arduino[8]=0

    def Inital_dataArd(self):
        self.conn = sqlite3.connect('Data_parameter.db')
        cursor = self.conn.execute("SELECT count(*) as Quatity from Ard")
        for row in cursor:
            quality=row[0]
        if quality!=0:
            cursor = self.conn.execute("SELECT * from Ard")
            for row in cursor:
                for i in range(1,10):
                    self.data_arduino.append(row[i])
        self.conn.close()

    def Save_dataArd(self):
        conn = sqlite3.connect('Data_parameter.db')
        conn.execute("DELETE FROM Ard")
        conn.execute("INSERT INTO  Ard (Pin3,Pin4,Pin5,Pin6,Pin7,Pin9,Pin10,Pin11,Pin12) VALUES (?,?,?,?,?,?,?,?,?);",
                     (self.data_arduino[0],self.data_arduino[1],self.data_arduino[2],self.data_arduino[3],self.data_arduino[4],
                      self.data_arduino[5],self.data_arduino[6],self.data_arduino[7],self.data_arduino[8]))
        conn.commit()
        self.conn.close()
    def Aboutme(self):
        About=QDialog(self)
        self.intro=Ui_Intro()
        self.intro.setupUi(About)
        About.exec()

class QDialog1(QDialog):
    close_arduino = pyqtSignal()
    @pyqtSlot()
    def closeEvent(self, event):
        self.close_arduino.emit()

class Setting_Windown(QMainWindow):
    def __init__(self,dialog,image,frame):
        super().__init__()
        self.ui = Ui_Setting()
        self.ui.setupUi(dialog)
        self.itemp=[]
        self.items=[]
        self.frame=frame
        self.image=image
        self.imageoutside=False
        self.centerX=0
        self.centerY=0
        self.tgian=0
        self.conn = sqlite3.connect("Data_parameter.db")
        self.scene = QGraphicsScene()#Lop quan ly 2D
        self.scene.setSceneRect(0, 0, 640, 480)
        self.scene.addPixmap(QPixmap(self.image))
        self.grview = QGraphicsView(self.scene, self.ui.label_ImageSetting)#lop cung cap Widget de hien thi QGraphicsScene
        self.grview.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.valueslide=self.ui.horizontalSlider_LH.value()
        self.initiateRect()
        self.innitalProcessImage()
        self.initiateRectp()
        self.innitalProcessImagep()
        self.ui.pushButton_DrawRect.clicked.connect(self.drawrect)
        self.ui.pushButton_Position.clicked.connect(self.Position)
        self.ui.pushButton_RemoveRect.clicked.connect(self.removerect)
        self.ui.pushButton_Saveallparameter.clicked.connect(self.SaveData)
        self.ui.pushButton_OpenImage.clicked.connect(self.openImage)
        self.ui.pushButton_testSample_Area.clicked.connect(self.GetResult)
        self.ui.pushButton_SaveImage.clicked.connect(self.delete_all)
        self.grview.clickItems.connect(self.showParameter)
        self.grview.moveItems.connect(self.MoveItems)
        self.grview.clickItems.connect(self.setValueZ)
        self.grview.doubleclick.connect(self.Rectchild)
        self.ui.doubleSpinBox_Maxvalue_RGB_01.editingFinished.connect(self.UpdateDataOnList)
        self.ui.doubleSpinBox_Minvalue_RGB_01.editingFinished.connect(self.UpdateDataOnList)
        self.ui.horizontalSlider_LH.valueChanged.connect(self.UpdateDataOnList)
        self.ui.horizontalSlider_LS.valueChanged.connect(self.UpdateDataOnList)
        self.ui.horizontalSlider_LV.valueChanged.connect(self.UpdateDataOnList)
        self.ui.horizontalSlider_UH.valueChanged.connect(self.UpdateDataOnList)
        self.ui.horizontalSlider_US.valueChanged.connect(self.UpdateDataOnList)
        self.ui.horizontalSlider_UV.valueChanged.connect(self.UpdateDataOnList)
        self.scene.entered.connect(self.SaveDataOnList)


    def MoveItems(self,valx,valy):
        for i in range(len(self.items)):
            if self.items[i][0].isSelected():
                self.GetDataFromRect(i)
                self.threadProcessImage(i,self.x,self.y,self.width,self.height)
        for j in range(len(self.itemp)):
            if self.itemp[j][0].isSelected():
                self.GetDataFromRectp(j)
                self.threadProcessImagep(j,self.xp,self.yp,self.widthp,self.heightp)
    @pyqtSlot()            
    def SaveData(self):
        conn = sqlite3.connect('Data_parameter.db')
        conn.execute("DELETE FROM  PARAMETER")
        conn.commit()
        for i in range(len(self.items)):
            self.GetDataFromRect(i)
            conn.execute("INSERT INTO  PARAMETER (Max_value, Min_value, Slide_value_LH, Slide_value_LS, Slide_value_LV, "
                         "Slide_value_UH, Slide_value_US, Slide_value_UV, x0, y0, Width, Height) VALUES (?,?,?,?,?,?,?,?,?,?,?,?);",
                         (self.maxvalue, self.minvalue, self.slidevalue_LH,self.slidevalue_LS,self.slidevalue_LV,
                          self.slidevalue_UH,self.slidevalue_US,self.slidevalue_UV, self.x, self.y, self.width, self.height))
            conn.commit()
        conn.execute("DELETE FROM  Center")
        conn.commit()
        for j in range(len(self.itemp)):
            self.GetDataFromRectp(j)
            self.itemp[0][14] = self.center_xx
            self.itemp[0][15] = self.center_yy
            conn.execute("INSERT INTO  Center (Max_valuep, Min_valuep, Slide_value_LHp, Slide_value_LSp, Slide_value_LVp, "
                         "Slide_value_UHp, Slide_value_USp, Slide_value_UVp, x0p, y0p, Widthp, Heightp,center_x,center_y) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);",
                         (self.maxvaluep, self.minvaluep, self.slidevalue_LHp, self.slidevalue_LSp, self.slidevalue_LVp,
                          self.slidevalue_UHp, self.slidevalue_USp, self.slidevalue_UVp, self.xp, self.yp, self.widthp,
                          self.heightp, self.center_x, self.center_y))
            conn.commit()
        self.conn.close()
        self.tgian=0
    def SaveDataOnList(self):
        for i in range(len(self.items)):
            if self.items[i][0].isSelected():
                self.GetDataFromRect(i)
                self.items[i]=(self.itemRect,self.maxvalue, self.minvalue, self.slidevalue_LH,self.slidevalue_LS,
                               self.slidevalue_LV,self.slidevalue_UH,self.slidevalue_US,self.slidevalue_UV,self.x, self.y, self.width, self.height,self.Pixitem)
                self.threadProcessImage(i,self.x,self.y,self.width,self.height)
        for j in range(len(self.itemp)):
            if self.itemp[j][0].isSelected():
                self.GetDataFromRectp(j)
                self.itemp[j]=[self.itemRectp,self.maxvaluep, self.minvaluep, self.slidevalue_LHp,self.slidevalue_LSp,
                               self.slidevalue_LVp,self.slidevalue_UHp,self.slidevalue_USp,self.slidevalue_UVp,self.xp, self.yp, self.widthp, self.heightp,self.Pixitemp,
                               self.center_x, self.center_y]
                self.threadProcessImagep(j,self.xp,self.yp,self.widthp,self.heightp)


    def GetDataFromRect(self,i):
        self.Pixitem = self.items[i][13]
        self.itemRect = self.items[i][0]
        self.x = self.items[i][0].sceneBoundingRect().left() + 4
        self.y = self.items[i][0].sceneBoundingRect().top() + 4
        self.width = self.items[i][0].sceneBoundingRect().width() - 8
        self.height = self.items[i][0].sceneBoundingRect().height() - 8
        self.maxvalue = self.items[i][1]
        self.minvalue = self.items[i][2]
        self.slidevalue_LH = self.items[i][3]
        self.slidevalue_LS = self.items[i][4]
        self.slidevalue_LV = self.items[i][5]
        self.slidevalue_UH = self.items[i][6]
        self.slidevalue_US = self.items[i][7]
        self.slidevalue_UV = self.items[i][8]

    @pyqtSlot()
    def GetDataFromRectp(self,j):
        self.Pixitemp = self.itemp[j][13]
        self.itemRectp = self.itemp[j][0]
        self.xp = self.itemp[j][0].sceneBoundingRect().left() + 4
        self.yp = self.itemp[j][0].sceneBoundingRect().top() + 4
        self.widthp = self.itemp[j][0].sceneBoundingRect().width() - 8
        self.heightp = self.itemp[j][0].sceneBoundingRect().height() - 8
        self.maxvaluep=self.itemp[j][1]
        self.minvaluep=self.itemp[j][2]
        self.slidevalue_LHp = self.itemp[j][3]
        self.slidevalue_LSp = self.itemp[j][4]
        self.slidevalue_LVp = self.itemp[j][5]
        self.slidevalue_UHp = self.itemp[j][6]
        self.slidevalue_USp = self.itemp[j][7]
        self.slidevalue_UVp = self.itemp[j][8]
        self.center_x = self.itemp[j][14]
        self.center_y = self.itemp[j][15]
    @pyqtSlot()    
    def initiateRect(self):
        self.conn = sqlite3.connect('Data_parameter.db')
        cursor = self.conn.execute("SELECT count(*) as Quatity from PARAMETER")
        for row in cursor:
            quality=row[0]
        if quality!=0:
            cursor = self.conn.execute("SELECT * from PARAMETER")
            for row in cursor:
                self.value = GraphicsRectItem(row[9], row[10], row[11], row[12])
                self.value.setZValue(1)
                self.items.append([self.value,row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9], row[10], row[11], row[12],None])
                self.scene.addItem(self.value)
        self.conn.close()
    def initiateRectp(self):
        self.conn = sqlite3.connect('Data_parameter.db')
        cursor = self.conn.execute("SELECT count(*) as Quatity from Center")
        for row in cursor:
            quality=row[0]
        if quality!=0:
            cursor = self.conn.execute("SELECT * from Center")
            for row in cursor:
                self.value = GraphicsRectItem(row[9], row[10], row[11], row[12])
                self.value.setZValue(1)
                self.itemp.append([self.value,row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9], row[10], row[11], row[12],None,row[13],
                                   row[14]])
                self.scene.addItem(self.value)
        self.conn.close()
    def innitalProcessImage(self):
        for i in range(len(self.items)):
            self.GetDataFromRect(i)
            self.threadProcessImage(i,self.x, self.y, self.width, self.height)
    def innitalProcessImagep(self):
        for j in range(len(self.itemp)):
            self.GetDataFromRectp(j)
            self.threadProcessImagep(j,self.xp, self.yp, self.widthp, self.heightp)
    @pyqtSlot()
    def drawrect(self):
            self.value = GraphicsRectItem(0, 0, 100, 50)
            self.value.setZValue(1)
            self.Pixmapitem=QGraphicsPixmapItem()
            self.Pixmapitem.setZValue(1)
            self.items.append([self.value,0,0,0,0,0,255,255,255,0,0,100,50,self.Pixmapitem])
            self.scene.addItem(self.value)
            
    @pyqtSlot()
    def Position(self):
        if len(self.itemp)==0:
            self.tgian = 1
            self.pst = GraphicsRectItem(0, 0, 30, 30)
            self.pst.setZValue(1)
            self.Pixmapitem=QGraphicsPixmapItem()
            self.Pixmapitem.setZValue(0)
            self.itemp.append([self.pst,0,0,0,0,0,255,255,255,0,0,30,30,self.Pixmapitem, 10, 10])
            self.scene.addItem(self.pst)
        else:
            pass
    @pyqtSlot()
    def removerect(self):
        for i in self.items:
            if i[0].isSelected():
                self.scene.removeItem(i[0])
                self.scene.removeItem(i[13])
                self.items.remove(i)
        for j in self.itemp:
            if j[0].isSelected():
                self.scene.removeItem(j[0])
                self.scene.removeItem(j[13])
                self.itemp.remove(j)
    def delete_all(self):
        for i in self.items:
                self.scene.removeItem(i[0])
                self.scene.removeItem(i[13])
        for j in self.itemp:
                self.scene.removeItem(j[0])
                self.scene.removeItem(j[13])
        self.items.clear()
        self.itemp.clear()
    @pyqtSlot()
    def showParameter(self):
        count=0
        countp = 0
        for i in range(0,len(self.items)):
            if self.items[i][0].isSelected():
                self.ui.doubleSpinBox_Maxvalue_RGB_01.setEnabled(True)
                self.ui.doubleSpinBox_Maxvalue_RGB_01.setValue(self.items[i][1])
                self.ui.doubleSpinBox_Minvalue_RGB_01.setEnabled(True)
                self.ui.doubleSpinBox_Minvalue_RGB_01.setValue(self.items[i][2])
                self.ui.horizontalSlider_LH.setEnabled(True)
                self.ui.horizontalSlider_LH.blockSignals(True)
                self.ui.horizontalSlider_LH.setValue(self.items[i][3])
                self.ui.horizontalSlider_LH.blockSignals(False)
                self.ui.label_value_slider_LH.setText(str(self.items[i][3]))

                self.ui.horizontalSlider_LS.setEnabled(True)
                self.ui.horizontalSlider_LS.blockSignals(True)
                self.ui.horizontalSlider_LS.setValue(self.items[i][4])
                self.ui.horizontalSlider_LS.blockSignals(False)
                self.ui.label_value_slider_LS.setText(str(self.items[i][4]))

                self.ui.horizontalSlider_LV.setEnabled(True)
                self.ui.horizontalSlider_LV.blockSignals(True)
                self.ui.horizontalSlider_LV.setValue(self.items[i][5])
                self.ui.horizontalSlider_LV.blockSignals(False)
                self.ui.label_value_slider_LV.setText(str(self.items[i][5]))

                self.ui.horizontalSlider_UH.setEnabled(True)
                self.ui.horizontalSlider_UH.blockSignals(True)
                self.ui.horizontalSlider_UH.setValue(self.items[i][6])
                self.ui.horizontalSlider_UH.blockSignals(False)
                self.ui.label_value_slider_UH.setText(str(self.items[i][6]))

                self.ui.horizontalSlider_US.setEnabled(True)
                self.ui.horizontalSlider_US.blockSignals(True)
                self.ui.horizontalSlider_US.setValue(self.items[i][7])
                self.ui.horizontalSlider_US.blockSignals(False)
                self.ui.label_value_slider_US.setText(str(self.items[i][7]))

                self.ui.horizontalSlider_UV.setEnabled(True)
                self.ui.horizontalSlider_UV.blockSignals(True)
                self.ui.horizontalSlider_UV.setValue(self.items[i][8])
                self.ui.horizontalSlider_UV.blockSignals(False)
                self.ui.label_value_slider_UV.setText(str(self.items[i][8]))

                self.GetDataFromRect(i)
                self.threadProcessImage(i,self.x,self.y,self.width,self.height)
                count=1
            if count==0 and countp == 0:
                self.lockParameter()
        for j in range(0,len(self.itemp)):
            if self.itemp[j][0].isSelected():
                self.ui.doubleSpinBox_Maxvalue_RGB_01.setEnabled(True)
                self.ui.doubleSpinBox_Maxvalue_RGB_01.setValue(self.itemp[j][1])
                self.ui.doubleSpinBox_Minvalue_RGB_01.setEnabled(True)
                self.ui.doubleSpinBox_Minvalue_RGB_01.setValue(self.itemp[j][2])
                self.ui.horizontalSlider_LH.setEnabled(True)
                self.ui.horizontalSlider_LH.blockSignals(True)
                self.ui.horizontalSlider_LH.setValue(self.itemp[j][3])
                self.ui.horizontalSlider_LH.blockSignals(False)
                self.ui.label_value_slider_LH.setText(str(self.itemp[j][3]))

                self.ui.horizontalSlider_LS.setEnabled(True)
                self.ui.horizontalSlider_LS.blockSignals(True)
                self.ui.horizontalSlider_LS.setValue(self.itemp[j][4])
                self.ui.horizontalSlider_LS.blockSignals(False)
                self.ui.label_value_slider_LS.setText(str(self.itemp[j][4]))

                self.ui.horizontalSlider_LV.setEnabled(True)
                self.ui.horizontalSlider_LV.blockSignals(True)
                self.ui.horizontalSlider_LV.setValue(self.itemp[j][5])
                self.ui.horizontalSlider_LV.blockSignals(False)
                self.ui.label_value_slider_LV.setText(str(self.itemp[j][5]))

                self.ui.horizontalSlider_UH.setEnabled(True)
                self.ui.horizontalSlider_UH.blockSignals(True)
                self.ui.horizontalSlider_UH.setValue(self.itemp[j][6])
                self.ui.horizontalSlider_UH.blockSignals(False)
                self.ui.label_value_slider_UH.setText(str(self.itemp[j][6]))

                self.ui.horizontalSlider_US.setEnabled(True)
                self.ui.horizontalSlider_US.blockSignals(True)
                self.ui.horizontalSlider_US.setValue(self.itemp[j][7])
                self.ui.horizontalSlider_US.blockSignals(False)
                self.ui.label_value_slider_US.setText(str(self.itemp[j][7]))

                self.ui.horizontalSlider_UV.setEnabled(True)
                self.ui.horizontalSlider_UV.blockSignals(True)
                self.ui.horizontalSlider_UV.setValue(self.itemp[j][8])
                self.ui.horizontalSlider_UV.blockSignals(False)
                self.ui.label_value_slider_UV.setText(str(self.itemp[j][8]))

                self.GetDataFromRectp(j)
                self.threadProcessImagep(j,self.xp,self.yp,self.widthp,self.heightp)
                countp=1      
                
            if countp==0 and count == 0:
                self.lockParameter()

    @pyqtSlot()
    def lockParameter(self):
        self.ui.doubleSpinBox_Maxvalue_RGB_01.setEnabled(False)
        self.ui.doubleSpinBox_Minvalue_RGB_01.setEnabled(False)
        self.ui.horizontalSlider_LH.setEnabled(False)
        self.ui.horizontalSlider_LS.setEnabled(False)
        self.ui.horizontalSlider_LV.setEnabled(False)
        self.ui.horizontalSlider_UH.setEnabled(False)
        self.ui.horizontalSlider_US.setEnabled(False)
        self.ui.horizontalSlider_UV.setEnabled(False)

    @pyqtSlot()
    def UpdateDataOnList(self):
      try:
        for i in range(len(self.items)):
            if self.items[i][0].isSelected():
                self.GetDataFromRect(i)
                maxvalue=self.ui.doubleSpinBox_Maxvalue_RGB_01.value()
                minvalue = self.ui.doubleSpinBox_Minvalue_RGB_01.value()
                slidevalue_LH = self.ui.horizontalSlider_LH.value()
                slidevalue_LS = self.ui.horizontalSlider_LS.value()
                slidevalue_LV = self.ui.horizontalSlider_LV.value()
                slidevalue_UH = self.ui.horizontalSlider_UH.value()
                slidevalue_US = self.ui.horizontalSlider_US.value()
                slidevalue_UV = self.ui.horizontalSlider_UV.value()
                self.ui.label_value_slider_LH.setText(str(slidevalue_LH))
                self.ui.label_value_slider_LS.setText(str(slidevalue_LS))
                self.ui.label_value_slider_LV.setText(str(slidevalue_LV))
                self.ui.label_value_slider_UH.setText(str(slidevalue_UH))
                self.ui.label_value_slider_US.setText(str(slidevalue_US))
                self.ui.label_value_slider_UV.setText(str(slidevalue_UV))
                self.items[i]=(self.items[i][0],maxvalue,minvalue,slidevalue_LH,slidevalue_LS,slidevalue_LV,
                               slidevalue_UH,slidevalue_US,slidevalue_UV,self.x, self.y, self.width, self.height,self.Pixitem)
                self.threadProcessImage(i,self.x,self.y,self.width,self.height)
        for j in range(len(self.itemp)):
            if self.itemp[j][0].isSelected():
                self.GetDataFromRectp(j)
                maxvaluep=self.ui.doubleSpinBox_Maxvalue_RGB_01.value()
                minvaluep = self.ui.doubleSpinBox_Minvalue_RGB_01.value()
                slidevalue_LHp = self.ui.horizontalSlider_LH.value()
                slidevalue_LSp = self.ui.horizontalSlider_LS.value()
                slidevalue_LVp = self.ui.horizontalSlider_LV.value()
                slidevalue_UHp = self.ui.horizontalSlider_UH.value()
                slidevalue_USp = self.ui.horizontalSlider_US.value()
                slidevalue_UVp = self.ui.horizontalSlider_UV.value()
                self.ui.label_value_slider_LH.setText(str(slidevalue_LHp))
                self.ui.label_value_slider_LS.setText(str(slidevalue_LSp))
                self.ui.label_value_slider_LV.setText(str(slidevalue_LVp))
                self.ui.label_value_slider_UH.setText(str(slidevalue_UHp))
                self.ui.label_value_slider_US.setText(str(slidevalue_USp))
                self.ui.label_value_slider_UV.setText(str(slidevalue_UVp))
                self.itemp[j]=(self.itemp[j][0],maxvaluep,minvaluep,slidevalue_LHp,slidevalue_LSp,slidevalue_LVp,
                               slidevalue_UHp,slidevalue_USp,slidevalue_UVp,self.xp, self.yp, self.widthp, self.heightp,self.Pixitemp,
                               self.center_x, self.center_y)
                self.threadProcessImagep(j,self.xp,self.yp,self.widthp,self.heightp)
      except:
          pass
    @pyqtSlot()
    def threadProcessImage(self,index,x,y,width,height):
      try:
        #print("index in thread",index)
        if self.imageoutside:
            self.imageforprocess=self.imageopen1
        else:
            self.imageforprocess=self.frame
        if x<0:
            x=0
        if y<0:
            y=0
        if x+width>640:
            x=640-width
        if y+height>480:
            y=480-height
        #print(x,y)
        #gray = cv2.cvtColor(self.imageforprocess, cv2.COLOR_BGR2GRAY)
       # ret, self.processedImage = cv2.threshold(gray[int(y):int(y+height), int(x):int(x+width)], self.ui.horizontalSlider_LH.value(),255, cv2.THRESH_BINARY)
        self.ProcessImage(self.imageforprocess,index,x,y,width,height)
        #self.processedImage = cv2.cvtColor(self.res, cv2.COLOR_BGR2GRAY)
        self.CovertoPixmap(self.res,x,y)
        self.CreateListPixmapIterm(self.pixm, index, x, y)
      except:
        pass
    def threadProcessImagep(self,index,x,y,width,height):
        #print("index in thread",index)
        if self.imageoutside:
            self.imageforprocess=self.imageopen1
        else:
            self.imageforprocess=self.frame
        if x<0:
            x=0
        if y<0:
            y=0
        if x+width>640:
            x=640-width
        if y+height>480:
            y=480-height
        #print(x,y)
        #gray = cv2.cvtColor(self.imageforprocess, cv2.COLOR_BGR2GRAY)
       # ret, self.processedImage = cv2.threshold(gray[int(y):int(y+height), int(x):int(x+width)], self.ui.horizontalSlider_LH.value(),255, cv2.THRESH_BINARY)
        self.ProcessImagep(self.imageforprocess,index,x,y,width,height)
        #self.processedImage = cv2.cvtColor(self.res, cv2.COLOR_BGR2GRAY)
        self.CovertoPixmap(self.resp,x,y)
        self.CreateListPixmapItermp(self.pixm, index, x, y)
        self.center_are()
    @pyqtSlot()    
    def ProcessImage(self,orginalImage,index,x,y,width,height):
      try:
        self.GetDataFromRect(index)
        crop_image = orginalImage[int(y):int(y + height), int(x):int(x + width)]
        HsvColor = cv2.cvtColor(crop_image, cv2.COLOR_BGR2HSV)
        L_b = np.array([self.slidevalue_LH, self.slidevalue_LS,self.slidevalue_LV])
        U_b = np.array([self.slidevalue_UH,self.slidevalue_US,self.slidevalue_UV])
        mask = cv2.inRange(HsvColor, L_b, U_b)
        self.res = cv2.bitwise_and(crop_image, crop_image, mask=mask)
      except:
       pass
    def ProcessImagep(self,orginalImage,index,x,y,width,height):

      try:
        self.GetDataFromRectp(index)
        crop_image = orginalImage[int(y):int(y + height), int(x):int(x + width)]
        print(x,y)
        self.HsvColorp = cv2.cvtColor(crop_image, cv2.COLOR_BGR2HSV)
        L_bp = np.array([self.slidevalue_LHp, self.slidevalue_LSp,self.slidevalue_LVp])
        U_bp = np.array([self.slidevalue_UHp,self.slidevalue_USp,self.slidevalue_UVp])
        self.maskp = cv2.inRange(self.HsvColorp, L_bp, U_bp)
        #self.maskp = cv2.erode(self.maskp, kernal, iterations=1)
        self.resp = cv2.bitwise_and(crop_image, crop_image, mask=self.maskp)
      except:
       pass
    def CovertoPixmap(self,image,x,y):
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:  # rows[0],cols[1],channels[2]
            if (image.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(image, image.shape[1], image.shape[0],image.strides[0], qformat)
        img = img.rgbSwapped()
        self.pixm = QtGui.QPixmap.fromImage(img)

    def CreateListPixmapIterm(self,pix,index,x,y):
                self.scene.removeItem(self.items[index][13])
                self.pixmapiterm = QGraphicsPixmapItem(pix)
                self.pixmapiterm .setPos(x, y)
                self.pixmapiterm .setZValue(0)
                self.scene.addItem(self.pixmapiterm)
                self.GetDataFromRect(index)
                self.items[index] = (self.itemRect, self.maxvalue, self.minvalue, self.slidevalue_LH, self.slidevalue_LS,self.slidevalue_LV,
                                     self.slidevalue_UH, self.slidevalue_US, self.slidevalue_UV,self.x, self.y, self.width, self.height,self.pixmapiterm)

    def CreateListPixmapItermp(self,pix,index,x,y):
                self.scene.removeItem(self.itemp[index][13])
                self.pixmapitermp = QGraphicsPixmapItem(pix)
                self.pixmapitermp .setPos(x, y)
                self.pixmapitermp .setZValue(0)
                self.scene.addItem(self.pixmapitermp)
                self.GetDataFromRectp(index)
                self.itemp[index] = [self.itemRectp, self.maxvaluep, self.minvaluep, self.slidevalue_LHp, self.slidevalue_LSp,self.slidevalue_LVp,
                                     self.slidevalue_UHp, self.slidevalue_USp, self.slidevalue_UVp,self.xp, self.yp, self.widthp, self.heightp,self.pixmapitermp,
                                     self.center_x, self.center_y]

    def openImage(self):
        fileChoosen = QFileDialog.getOpenFileName(self, 'Open Files', 'D:\\', "Image Files (*.jpg *.png)")
        if fileChoosen[0] != '':
            imagepath=fileChoosen[0]
            self.image=QPixmap(imagepath)
            self.scene.addPixmap(self.image)
            self.imageopen1 = cv2.imread(fileChoosen[0])
            self.imageopen = self.image.copy()
            self.imageoutside = True
        else:
            pass

    def GetResult(self):
        self.center_are()
        self.pen = QPen(QColor(Qt.yellow))
        self.center = QGraphicsEllipseItem(self.center_xx, self.center_yy, 5, 5)
        self.center.setZValue(2)
        self.center.setPen(self.pen)
        self.scene.addItem(self.center)
        gettotalResult=0
        totalArea=0
        if len(self.items)==0:
            self.ui.label_Result_test.setText("NG")
            self.ui.label_Result_Area.setText("No Items")
            return False
        for i in range(len(self.items)):
            if self.items[i][0].isSelected():
                cal=self.Calculate_area(i)
                if cal:
                    self.ui.label_Result_test.setText("OK One")
                    self.ui.label_Result_Area.setText(str(self.area))
                    return True
                else:
                    self.ui.label_Result_test.setText("NG One")
                    self.ui.label_Result_Area.setText(str(self.area))
                    return False

        for i in range(len(self.items)):
            cal=self.Calculate_area(i)
            totalArea += self.area
            if cal:
                gettotalResult+=1


        if gettotalResult==len(self.items):
            text= "OK Total: %d / %d" %(gettotalResult,len(self.items))
            self.ui.label_Result_test.setText(text)
            self.ui.label_Result_Area.setText(str(totalArea))
            return True
        else:
            text= "NG Total: %d / %d" %(gettotalResult,len(self.items))
            self.ui.label_Result_test.setText(text)
            self.ui.label_Result_Area.setText(str(totalArea))
            return False


    def Calculate_area(self,count):
        self.area = 0
        if self.imageoutside:
            self.imageforprocess = self.imageopen1
        else:
            self.imageforprocess = self.frame
        self.GetDataFromRect(count)
        self.ProcessImage(self.imageforprocess,count,self.x,self.y,self.width,self.height)
        gray = cv2.cvtColor(self.res, cv2.COLOR_BGR2GRAY)
        contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours)==0 or len(hierarchy)==0:
            self.ui.label_Result_Area.setText("Area is None")
            self.area=0
            return False
        for i in range (len(contours)):
            self.area = cv2.contourArea(contours[i]) / 100 + self.area
        if self.area >= self.minvalue and self.area <= self.maxvalue:
            return True
        else:
            return False

    def center_are(self):
        if self.imageoutside:
            self.imageforprocess = self.imageopen1
        else:
            self.imageforprocess = self.frame
        #self.GetDataFromRectp(countp)
        #self.ProcessImagep(self.imageforprocess,countp,self.xp,self.yp,self.widthp,self.heightp)
        contours, hierarchy = cv2.findContours(self.maskp, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        if len(contours)==0 or len(hierarchy)==0:
            self.ui.label_Result_Area.setText("Area is No have")

            return False

        contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(contour)

        self.cx = int(M['m10'] / M['m00'])
        self.cy = int(M['m01'] / M['m00'])
        self.center_xx = self.cx - 2.5 + self.xp
        self.center_yy = self.cy - 2.5 + self.yp
        self.Do_lech()
    def Do_lech(self):
        #print(self.itemp)
        #print("items",self.items)

        if len(self.itemp)==0 or self.tgian == 1:
            self.center_XL = 0
            self.center_YL = 0
            #print(self.center_XL, self.center_YL)
        else:
            self.center_XL =   self.center_xx - self.itemp[0][14]
            self.center_YL =   self.center_yy - self.itemp[0][15]

            self.itemp[0][14]=self.center_xx
            self.itemp[0][15] = self.center_yy
            #print(self.center_XL,self.center_YL)
            #print(self.itemp[0][14], self.itemp[0][15])

            self.chinh_hinh()
    def chinh_hinh(self):
        for i in range (len(self.items)):
            self.GetDataFromRect(i)
            self.x_lech = self.center_XL
            self.y_lech = self.center_YL
            self.items[i][0].moveBy(self.x_lech,self.y_lech)
            self.threadProcessImage(i,self.x,self.y,self.width,self.height)
    def setValueZ(self):
        for i in self.items:
            if i[0].isSelected():
                i[0].setZValue(2)
            else:
                i[0].setZValue(1)

    def Rectchild(self,Xpoint,Ypoint):
        for i in self.items:
            if i[0].isSelected():
                for j in self.items:
                    a = QRect(j[0].sceneBoundingRect().left() + 4, j[0].sceneBoundingRect().top() + 4,j[0].sceneBoundingRect().width() - 8,j[0].sceneBoundingRect().height() - 8)
                    if a.contains(Xpoint,Ypoint) and  j[0].isSelected()==False:
                        j[0].setZValue(2)
                        j[0].setSelected(True)
                        i[0].setSelected(False)
                        i[0].setZValue(1)

class QGraphicsView(QGraphicsView):
    clickItems = pyqtSignal()
    moveItems = pyqtSignal(int,int)
    doubleclick=pyqtSignal(int,int)
    def __init__(self,*args):
        super().__init__(*args)
    def mousePressEvent(self,event):
        super().mousePressEvent(event)
        self.clickItems.emit()
    def mouseMoveEvent(self,event):
        super().mouseMoveEvent(event)
        valx=event.pos().x()
        valy=event.pos().y()
        self.moveItems.emit(valx,valy)
    def mouseDoubleClickEvent(self,event):
        self.doubleclick.emit(event.pos().x(),event.pos().y())

class WorkThread(QThread):
    letdoit = pyqtSignal()
    Error = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.stopserial=True
        self.check = False
        self.check1=False
    def run(self):
     
        try:
            while(1):
                 ports = serial.tools.list_ports.comports(include_links=False)
                 #print("number",len(ports))
                 if len(ports)!=0 and self.check==False:
                     for port in ports:
                         self.ser = serial.Serial(port.device)
                         if self.ser.isOpen():
                             self.ser.close()
                             self.ser = serial.Serial(port.device, 9600,timeout=2)
                             self.check = True
                             self.check1= True
                 data = self.ser.readline().decode("utf-8").strip('\n').strip('\r')
                 time.sleep(0.3)
                 if data == "SenSor In" and self.stopserial==False:
                        self.letdoit.emit()


        except :

            self.Error.emit()
            self.check=False
            if self.check1:
                self.ser.close()


    def stopSerial(self):
        self.stopserial=True
    def startSerial(self):
        self.stopserial=False

    def Send_NG(self,data_arduino):
        Sending = bytearray(data_arduino)
        self.ser.write(Sending)


if __name__=="__main__":
    app = QApplication(sys.argv)
    w = Foster_app()
    w.show()
    sys.exit(app.exec_())

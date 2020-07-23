# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
from PyQt5.QtGui import *
from Settingwindown1 import *
from Mainwindown1 import *
from Arduino import*
from DrawRect import *
from about import *
import cv2
from scipy.spatial import distance as dist
import sys
import serial
import time
import serial.tools.list_ports
import sqlite3
import os
import math
#from pypylon import pylon
from toucamera import *

class Foster_app(QMainWindow):
    SenddatatoArduino_NG = pyqtSignal()
    def __init__(self,h,w):
        super().__init__()
        self.resize(w,h)
        self.setMinimumSize(QtCore.QSize(800, 600))
        self.sang = 0
        self.toi = 0
        self.h=h
        self.w=w
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self,self.w,self.h)
        self.timer = QtCore.QTimer()
        self.data_arduino=[]
        self.isCapturing = False
        self.noPort=False
        self.quantity_OK = 0
        self.quantity_NG = 0
        self.quantity_total = 0
        self.workThread = WorkThread()
        self.Inital_dataArd()
        self.pix=QtGui.QPixmap("Icon/luc_giac.jpg")
        self.pix = self.pix.scaled(640,480)
        self.frame=cv2.imread("Icon/luc_giac.jpg")
        self.frame = cv2.resize(src=self.frame, dsize=(640, 480))
        self.ui.sang.clicked.connect(self.dosang)
        self.ui.toi.clicked.connect(self.dotoi)
        self.ui.actionParameter.triggered.connect(self.setting_parameter)
        self.ui.actionArduino_Uno.triggered.connect(self.Arduino_setting)
        self.ui.actionDocumment.triggered.connect(self.openDocument)
        self.ui.actionAbout.triggered.connect(self.Aboutme)
        self.ui.actionSave.triggered.connect(self.saveFileDialog)
        self.ui.pushButton_cameraON.clicked.connect(self.start_basler)
        self.ui.pushButton_cameraOFF.clicked.connect(self.Stopcam)
        self.ui.pushButton_Clear.clicked.connect(self.clearQuantity)
        self.ui.pushButton_cameraOFF.clicked.connect(self.Stopcam)
        self.ui.actionExits.triggered.connect(self.deleteLater)
        self.ui.pushButton_connectArduino.clicked.connect(self.Serial)
        self.workThread.letdoit.connect(self.getResult)
        self.workThread.Error.connect(self.ErrorNoArd)
        self.pix1 = QtGui.QPixmap("Icon/Nocam.jpg")
        self.ui.label_videocam.setPixmap(self.pix1)
        self.ui.test.clicked.connect(self.getResult)
        self.show()
    def start_basler(self):
        self.fps = 20
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

        # Grabing Continusely (video) with minimal delay
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        self.converter = pylon.ImageFormatConverter()

        # converting to opencv bgr format
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        self.baslertimmer()
        self.show()

    def baslertimmer(self):
        self.isCapturing = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.Display_basler)
        self.timer.start(1000./self.fps)
    def Display_basler(self):
        grabResult = self.camera.RetrieveResult(10000, pylon.TimeoutHandling_ThrowException)
        image = self.converter.Convert(grabResult)
        img_basler = image.GetArray()
        self.frame = img_basler
        self.imageforprocess = cv2.resize(src=self.frame, dsize=(720, 600))
        img = QtGui.QImage(self.imageforprocess, self.imageforprocess.shape[1],
                           self.imageforprocess.shape[0], QtGui.QImage.Format_RGB888)
        self.pix = QtGui.QPixmap.fromImage(img)
        self.ui.label_videocam.setPixmap(self.pix)
    def dotoi(self):
       self.Stopcam()
       if self.sang>0:
        self.sang = self.sang-50
        self.ui.value_sang.setText(str(self.sang))
       self.Startcam()
    def dosang(self):
      self.Stopcam()
      if self.sang<500:
        self.sang = self.sang + 50
        self.ui.value_sang.setText(str(self.sang))
      self.Startcam()
    def Startcam(self):
        self.fps = 200
        name=['0','0','0','0']
        self.cam=[0, 1,2,3]
        self.cnum = get_Enum()
        self.isCapturing = True
        if self.isCapturing:
          for i in range (0,self.cnum):
              self.cam[i] = ToupCamCamera(cid=i)
              self.cam[i].open(1)
              self.cam[i].set_auto_exposure(False)
              self.cam[i].set_HZ(10)
              self.cam[i].set_Speed(22)
              self.cam[i].set_ExpoAGain(self.sang)#tang do sang
              name[i] = self.cam[i].get_serial()
              self.ith_frame = 1
              self.Starttimmer()
              self.show()

    def Starttimmer(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.Displayframe)
        self.timer.start(1000./self.fps)

    def Displayframe(self):
        for i in range (0,self.cnum):
            self.frame= np.array(self.cam[i].get_pil_image())
            img = QtGui.QImage(self.frame, self.frame.shape[1],
                               self.frame.shape[0], QtGui.QImage.Format_RGB888)
            self.pix = QtGui.QPixmap.fromImage(img)
            self.ui.label_videocam.setPixmap(self.pix)
       
    def Displayframegray(self):
        for i in range (0,self.cnum):
            self.frame= np.array(self.cam[i].get_pil_image())
            img_gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            img = QtGui.QImage(img_gray.data,
                               self.frame.shape[1],
                               self.frame.shape[0],
                               img_gray.strides[0],
                               QtGui.QImage.Format_Grayscale8)
            self.pix = QtGui.QPixmap.fromImage(img)
            self.ui.label_videocam.setPixmap(self.pix)
    def Stopcam(self):
        if self.isCapturing:
            for i in range(0, self.cnum):
                self.cam[i].close()
                self.isCapturing= False
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
        self.Stopcam()
        dialog = QDialog(self)
        self.pix = QPixmap(self.pix).scaled(640, 480, Qt.KeepAspectRatio,
                                           Qt.SmoothTransformation)
        self.pix = self.pix.scaled(640,480)
        self.imageforprocess = cv2.resize(src=self.frame, dsize=(640, 480))
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
        self.imageforprocess = cv2.resize(src=self.frame, dsize=(640, 480))
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
            #self.workThread.Send_OK(self.data_arduino)
        else:
            self.ui.label_Mainresult.setStyleSheet("color:red;font: 90pt;Times New Roman;")
            self.ui.label_Mainresult.setText("NG")
            self.quantity_NG+=1
            self.ui.label_NG.setText(str(self.quantity_NG))
            #self.workThread.Send_NG(self.data_arduino)

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
        self.noi_diem = []
        self.loai_diem = []
        self.dem_chon =0
        self.goc = 0
        self.chon_hcnx = []
        self.chon_hcny = []
        self.itemp=[]
        self.items=[]
        self.loai_diem = []
        self.frame=frame
        self.image=image
        self.imageoutside=False
        self.center_x=0
        self.center_y=0
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
        self.readloaidiem()
        self.readmeasure()
        self.ui.pushButton_DrawRect.clicked.connect(self.drawrect)
        self.ui.pushButton_Position.clicked.connect(self.Position)
        self.ui.pushButton_RemoveRect.clicked.connect(self.removerect)
        self.ui.pushButton_Saveallparameter.clicked.connect(self.SaveData)
        self.ui.pushButton_OpenImage.clicked.connect(self.openImage)
        self.ui.pushButton_testSample_Area.clicked.connect(self.GetResult)
        self.ui.pushButton_SaveImage.clicked.connect(self.delete_all)
        self.grview.moveItems.connect(self.MoveItems)
        self.grview.clickItems.connect(self.showParameter)
        self.grview.clickItems.connect(self.setValueZ)
        self.grview.clickItems.connect(self.Rectchild)
        self.ui.distance_2object.editingFinished.connect(self.UpdateDataOnList)
        self.ui.angle_xoay.editingFinished.connect(self.UpdateDataOnList)
        self.ui.doubleSpinBox_Maxvalue_RGB_01.editingFinished.connect(self.UpdateDataOnList)
        self.ui.doubleSpinBox_Minvalue_RGB_01.editingFinished.connect(self.UpdateDataOnList)
        self.ui.doubleSpinBox_Maxvalue_RGB_2.editingFinished.connect(self.UpdateDataOnList)
        self.ui.doubleSpinBox_Maxvalue_RGB_3.editingFinished.connect(self.UpdateDataOnList)
        self.ui.doubleSpinBox_Maxvalue_RGB_4.editingFinished.connect(self.UpdateDataOnList)
        self.ui.doubleSpinBox_Minvalue_RGB_2.editingFinished.connect(self.UpdateDataOnList)
        self.ui.horizontalSlider_LH.valueChanged.connect(self.UpdateDataOnList)
        self.ui.horizontalSlider_LS.valueChanged.connect(self.UpdateDataOnList)
        self.ui.horizontalSlider_LV.valueChanged.connect(self.UpdateDataOnList)
        self.ui.horizontalSlider_UH.valueChanged.connect(self.UpdateDataOnList)
        self.ui.horizontalSlider_US.valueChanged.connect(self.UpdateDataOnList)
        self.ui.horizontalSlider_UV.valueChanged.connect(self.UpdateDataOnList)
        self.scene.entered.connect(self.SaveDataOnList)
    def MoveItems(self):
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
      try:
        conn = sqlite3.connect('Data_parameter.db')
        conn.execute("DELETE FROM  PARAMETER")
        conn.commit()
        for i in range(len(self.items)):
                     self.GetDataFromRect(i)
                     conn.execute(
                         "INSERT INTO  PARAMETER (Max_value, Min_value, Slide_value_LH, Slide_value_LS, Slide_value_LV, "
                         "Slide_value_UH, Slide_value_US, Slide_value_UV, x0, y0, Width, Height, Num1, Num2, MaxD, MinD, Angle, Num3)"
                         " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",
                         (self.maxvalue, self.minvalue, self.slidevalue_LH, self.slidevalue_LS, self.slidevalue_LV,
                          self.slidevalue_UH, self.slidevalue_US, self.slidevalue_UV, self.x, self.y, self.width,
                          self.height, self.num1, self.num2, self.maxD, self.minD, self.angle, self.num3))
                     conn.commit()
        conn.execute("DELETE FROM  Center")
        conn.commit()
        for j in range(len(self.itemp)):
            self.GetDataFromRectp(j)
            self.itemp[0][14] = self.center_x
            self.itemp[0][15] = self.center_y
            conn.execute("INSERT INTO  Center (Max_valuep, Min_valuep, Slide_value_LHp, Slide_value_LSp, Slide_value_LVp, "
                         "Slide_value_UHp, Slide_value_USp, Slide_value_UVp, x0p, y0p, Widthp, Heightp,center_x,center_y) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);",
                         (self.maxvaluep, self.minvaluep, self.slidevalue_LHp, self.slidevalue_LSp, self.slidevalue_LVp,
                          self.slidevalue_UHp, self.slidevalue_USp, self.slidevalue_UVp, self.xp, self.yp, self.widthp,
                          self.heightp, self.center_x, self.center_y))
            conn.commit()
        conn.execute("DELETE FROM  Measure")
        conn.commit()
        self.Measure()
        conn.execute("INSERT INTO  Measure (Area, Distance, Distancew, trudiem) VALUES (?,?,?,?);",
                         (self.Area, self.Distance, self.Distancew, self.Number))
        conn.commit()

        conn.commit()
        conn.execute("DELETE FROM  Loaidiem")
        conn.commit()
        self.docdiem()
        conn.execute("INSERT INTO  Loaidiem (diem1,diem2,diem3,diem4,diem5,diem6) VALUES (?,?,?,?,?,?);",
                     (self.diem1,self.diem2,self.diem3,self.diem4,self.diem5,self.diem6))
        conn.commit()

        conn.commit()
        conn.execute("DELETE FROM  image")
        conn.commit()
        self.saveimage()
        self.imagepath1=(self.imagepath,)
        conn.execute("INSERT INTO  image (Anh1) VALUES (?);",
                     (self.imagepath1))
        conn.commit()
        self.conn.close()
      except:
        pass
    def SaveDataOnList(self):
        for i in range(len(self.items)):
            if self.items[i][0].isSelected():
                self.GetDataFromRect(i)
                self.items[i]=(self.itemRect,self.maxvalue, self.minvalue, self.slidevalue_LH,self.slidevalue_LS,
                               self.slidevalue_LV,self.slidevalue_UH,self.slidevalue_US,self.slidevalue_UV,self.x,
                               self.y, self.width, self.height,self.Pixitem, self.num1,self.num2, self.maxD, self.minD,self.angle,self.num3)
                self.threadProcessImage(i,self.x,self.y,self.width,self.height)
        for j in range(len(self.itemp)):
            if self.itemp[j][0].isSelected():
                self.GetDataFromRectp(j)
                self.itemp[j]=[self.itemRectp,self.maxvaluep, self.minvaluep, self.slidevalue_LHp,self.slidevalue_LSp,
                               self.slidevalue_LVp,self.slidevalue_UHp,self.slidevalue_USp,self.slidevalue_UVp,self.xp, self.yp, self.widthp, self.heightp,self.Pixitemp,
                               self.center_x, self.center_y]
                self.threadProcessImagep(j,self.xp,self.yp,self.widthp,self.heightp)
    def docdiem(self):
        self.loaidiem()
        if len(self.loai_diem)==6:
           self.diem1 = self.loai_diem[0]
           self.diem2 = self.loai_diem[1]
           self.diem3 = self.loai_diem[2]
           self.diem4 = self.loai_diem[3]
           self.diem5 = self.loai_diem[4]
           self.diem6 = self.loai_diem[5]
        if len(self.loai_diem)==5:
           self.diem1 = self.loai_diem[0]
           self.diem2 = self.loai_diem[1]
           self.diem3 = self.loai_diem[2]
           self.diem4 = self.loai_diem[3]
           self.diem5 = self.loai_diem[4]
           self.diem6 = self.diem5
        if len(self.loai_diem)==4:
           self.diem1 = self.loai_diem[0]
           self.diem2 = self.loai_diem[1]
           self.diem3 = self.loai_diem[2]
           self.diem4 = self.loai_diem[3]
           self.diem5 = self.diem6 = self.diem4
        if len(self.loai_diem)==3:
           self.diem1 = self.loai_diem[0]
           self.diem2 = self.loai_diem[1]
           self.diem3 = self.loai_diem[2]
           self.diem5 = self.diem6 = self.diem4 =self.diem3
        if len(self.loai_diem)==2:
           self.diem1 = self.loai_diem[0]
           self.diem2 = self.loai_diem[1]
           self.diem5 = self.diem6 = self.diem4 = self.diem3 = self.diem2
        if len(self.loai_diem)==1:
           self.diem1 = self.loai_diem[0]
           self.diem5 = self.diem6 = self.diem4 = self.diem2 =self.diem3 = self.diem1
        if len(self.loai_diem)>6:
            self.diem5 = self.diem6 = self.diem4 = self.diem2 = self.diem3 = self.diem1 = 0
    def GetDataFromRect(self,i):
          self.Pixitem = self.items[i][13]
          self.itemRect = self.items[i][0]
          self.x = self.items[i][0].sceneBoundingRect().left() + 4
         # print(self.items[i][0].sceneBoundingRect().left(),self.items[i][0].sceneBoundingRect().top(), self.items[i][0].sceneBoundingRect().center().x())
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
          self.num1 = self.items[i][14]
          self.num2 = self.items[i][15]
          self.maxD = self.items[i][16]
          self.minD = self.items[i][17]
          self.angle = self.items[i][18]
          self.num3 = self.items[i][19]
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
    def Measure(self):
        self.Area = self.ui.radioButton.isChecked()
        self.Distance = self.ui.radioButton_2.isChecked()
        self.Distancew = self.ui.radioButton_3.isChecked()
        self.Number = self.ui.tru_diem.value()
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
                   self.items.append([self.value, row[1], row[2], row[3], row[4], row[5],
                                      row[6], row[7], row[8], row[9], row[10], row[11],
                                      row[12], None, row[13], row[14], row[15], row[16], row[17], row[18]])
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
                self.itemp.append([self.value,row[1],row[2],row[3],row[4],row[5],
                                   row[6],row[7],row[8],row[9], row[10], row[11], row[12],None,row[13],row[14]])
                self.scene.addItem(self.value)
        self.conn.close()
    def readmeasure(self):
        self.conn = sqlite3.connect('Data_parameter.db')
        cursor = self.conn.execute("SELECT count(*) as Quatity from Measure")
        for row in cursor:
            quality=row[0]
        if quality!=0:
            cursor = self.conn.execute("SELECT * from Measure")
            for row in cursor:
                self.Area = bool(row[0])
                self.Distance = bool(row[1])
                self.Distancew = bool(row[2])
                self.Number = row[3]
                self.ui.radioButton.setChecked(self.Area)
                self.ui.radioButton_2.setChecked(self.Distance)
                self.ui.radioButton_3.setChecked(self.Distancew)
                self.ui.tru_diem.setValue(self.Number)
    def readloaidiem(self):
        self.conn = sqlite3.connect('Data_parameter.db')
        cursor = self.conn.execute("SELECT count(*) as Quatity from Loaidiem")
        for row in cursor:
            quality = row[0]
        if quality != 0:
            cursor = self.conn.execute("SELECT * from Loaidiem")
            for row in cursor:
                for i in range(0,len(row)):
                   self.loai_diem.append(row[i])

    def readimage(self):
        self.conn = sqlite3.connect('Data_parameter.db')
        cursor = self.conn.execute("SELECT count(*) as Quatity from Measure")
        for row in cursor:
            quality = row[0]
        if quality != 0:
            cursor = self.conn.execute("SELECT * from image")
            for row in cursor:
                self.imagepath1 = row[0]

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
            self.value.setZValue(2)
            self.Pixmapitem=QGraphicsPixmapItem()
            self.Pixmapitem.setZValue(1)
            self.items.append([self.value, 0, 0, 0, 0, 0, 255, 255, 255, 0, 0, 100, 50, self.Pixmapitem, 0, 0, 0, 0, 0, 0])
            self.scene.addItem(self.value)
    @pyqtSlot()
    def Position(self):
        if len(self.itemp)==0:
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
    def center_rect(self,index):
        cenrec_x = self.items[index][0].sceneBoundingRect().center().x()
        cenrec_y = self.items[index][0].sceneBoundingRect().center().y()
        return cenrec_x,cenrec_y
    def draw_circle_xanh(self,cenx,ceny):
        pen = QPen(QColor(Qt.blue))
        circle = QGraphicsEllipseItem(cenx, ceny, 8, 8)
        circle.setZValue(0)
        circle.setPen(pen)
        circle.moveBy(self.center_x,self.center_y)
        self.scene.addItem(circle)
    def draw_circle(self,cenx,ceny):
        pen = QPen(QColor(Qt.red))
        circle = QGraphicsEllipseItem(cenx, ceny, 5, 5)
        circle.setZValue(0)
        circle.setPen(pen)
        circle.moveBy(self.center_x,self.center_y)
        self.scene.addItem(circle)
    def xoay_rect(self,index):
       if self.angle!=0:
           tam_x = self.center_x
           tam_y = self.center_y
           self.xr1 = self.items[index][0].sceneBoundingRect().left() + 4
           self.yr1 = self.items[index][0].sceneBoundingRect().top() + 4
           self.widthr1 = self.items[index][0].sceneBoundingRect().width() - 8
           self.heightr1 = self.items[index][0].sceneBoundingRect().height() - 8
           self.rect1 = GraphicsRectItem(self.xr1, self.yr1, self.widthr1, self.heightr1)
           self.scene.addItem(self.rect1)
           point = self.xoay_diem(tam_x, tam_y, self.xr1, self.yr1, self.goc)
           self.point_x1 = point[0]
           self.point_y1 = point[1]
           self.rect1 = GraphicsRectItem(0, 0, self.widthr1, self.heightr1)
           self.rect1.moveBy(self.point_x1, self.point_y1)
           self.rect1.setRotation(self.goc)
           self.rect1.moveBy(tam_x, tam_y)
           self.rect1.setZValue(0)
           self.scene.addItem(self.rect1)
       else:
               pass
    def xoay_line(self, point1, point2, point3, point4):
        point_xoay1, point_xoay2 = self.xoay_diem(self.center_x, self.center_y, point1, point2, self.goc)
        point_xoay3, point_xoay4 = self.xoay_diem(self.center_x, self.center_y, point3, point4, self.goc)
        x1 = point_xoay1 + self.center_x
        y1 = point_xoay2 + self.center_y
        x2 = point_xoay3 + self.center_x
        y2 = point_xoay4 + self.center_y
        return x1, y1, x2, y2
    def xoay_diem(self,centerx,centery,xr1,yr1, goc):
        newpx1 = xr1 - centerx
        newpy1 = yr1 - centery
        point_x1 = newpx1 * math.cos(math.radians(goc)) - newpy1 * math.sin(math.radians(goc))
        point_y1 = newpx1 * math.sin(math.radians(goc)) + newpy1 * math.cos(math.radians(goc))
        return point_x1, point_y1
    def loaidiem(self):
        self.Number = int(self.ui.tru_diem.value())
        if self.Number!=0 and self.Number<=360:
            if self.Number not in self.loai_diem:
                self.loai_diem.append(self.Number)
        if self.Number==0:
            self.loai_diem.clear()
    def showParameter(self):
        count=0
        countp = 0
        self.scene.update()
        for i in range(len(self.items)):
            self.ui.tru_diem.setEnabled(True)
            if self.items[i][0].isSelected() and self.ui.radioButton.isChecked():
                self.ui.distance_2object.setEnabled(True)
                self.ui.distance_2object.setValue(self.items[i][19])
                self.ui.angle_xoay.setEnabled(True)
                self.ui.angle_xoay.setValue(self.items[i][18])
                self.ui.doubleSpinBox_Maxvalue_RGB_01.setEnabled(True)
                self.ui.doubleSpinBox_Maxvalue_RGB_01.setValue(self.items[i][1])
                self.ui.doubleSpinBox_Minvalue_RGB_01.setEnabled(True)
                self.ui.doubleSpinBox_Minvalue_RGB_01.setValue(self.items[i][2])
            if self.items[i][0].isSelected() and self.ui.radioButton_2.isChecked():
                self.ui.distance_2object.setEnabled(True)
                self.ui.distance_2object.setValue(self.items[i][19])
                self.ui.angle_xoay.setEnabled(True)
                self.ui.angle_xoay.setValue(self.items[i][18])
                self.ui.doubleSpinBox_Maxvalue_RGB_2.setEnabled(True)
                self.ui.doubleSpinBox_Maxvalue_RGB_2.setValue(self.items[i][14])
                self.ui.doubleSpinBox_Maxvalue_RGB_4.setEnabled(True)
                self.ui.doubleSpinBox_Maxvalue_RGB_4.setValue(self.items[i][16])
                self.ui.doubleSpinBox_Minvalue_RGB_2.setEnabled(True)
                self.ui.doubleSpinBox_Minvalue_RGB_2.setValue(self.items[i][17])
            if self.items[i][0].isSelected() and self.ui.radioButton_3.isChecked():
                self.ui.distance_2object.setEnabled(True)
                self.ui.distance_2object.setValue(self.items[i][19])
                self.ui.angle_xoay.setEnabled(True)
                self.ui.angle_xoay.setValue(self.items[i][18])
                self.ui.doubleSpinBox_Maxvalue_RGB_3.setEnabled(True)
                self.ui.doubleSpinBox_Maxvalue_RGB_3.setValue(self.items[i][15])
                self.ui.doubleSpinBox_Maxvalue_RGB_4.setEnabled(True)
                self.ui.doubleSpinBox_Maxvalue_RGB_4.setValue(self.items[i][16])
                self.ui.doubleSpinBox_Minvalue_RGB_2.setEnabled(True)
                self.ui.doubleSpinBox_Minvalue_RGB_2.setValue(self.items[i][17])
            if self.items[i][0].isSelected():
                count = 1
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
                self.ui.horizontalSlider_US.setValue(255.0)
                self.ui.horizontalSlider_US.blockSignals(False)
                self.ui.label_value_slider_US.setText(str(self.items[i][7]))
                self.ui.horizontalSlider_UV.setEnabled(True)
                self.ui.horizontalSlider_UV.blockSignals(True)
                self.ui.horizontalSlider_UV.setValue(self.items[i][8])
                self.ui.horizontalSlider_UV.blockSignals(False)
                self.ui.label_value_slider_UV.setText(str(self.items[i][8]))

                self.GetDataFromRect(i)
                self.threadProcessImage(i,self.x,self.y,self.width,self.height)
            if count==0 and countp ==0:
                self.lockParameter()
        for j in range(0,len(self.itemp)):
            if self.itemp[j][0].isSelected():
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

            if countp==0 and count==0 :
                self.lockParameter()
    @pyqtSlot()
    def lockParameter(self):
        self.ui.distance_2object.setEnabled(False)
        self.ui.angle_xoay.setEnabled(False)
        self.ui.doubleSpinBox_Maxvalue_RGB_01.setEnabled(False)
        self.ui.doubleSpinBox_Minvalue_RGB_01.setEnabled(False)
        self.ui.doubleSpinBox_Maxvalue_RGB_2.setEnabled(False)
        self.ui.doubleSpinBox_Maxvalue_RGB_3.setEnabled(False)
        self.ui.doubleSpinBox_Maxvalue_RGB_4.setEnabled(False)
        self.ui.doubleSpinBox_Minvalue_RGB_2.setEnabled(False)
        self.ui.horizontalSlider_LH.setEnabled(False)
        self.ui.horizontalSlider_LS.setEnabled(False)
        self.ui.horizontalSlider_LV.setEnabled(False)
        self.ui.horizontalSlider_UH.setEnabled(False)
        self.ui.horizontalSlider_US.setEnabled(False)
        self.ui.horizontalSlider_UV.setEnabled(False)
    @pyqtSlot()
    def UpdateDataOnList(self):
      try:
        #self.Number = self.ui.tru_diem.value()
        for i in range(len(self.items)):
            if self.items[i][0].isSelected():
                self.GetDataFromRect(i)
                self.maxvalue=self.ui.doubleSpinBox_Maxvalue_RGB_01.value()
                self.minvalue = self.ui.doubleSpinBox_Minvalue_RGB_01.value()
                self.slidevalue_LH = self.ui.horizontalSlider_LH.value()
                self.slidevalue_LS = self.ui.horizontalSlider_LS.value()
                self.slidevalue_LV = self.ui.horizontalSlider_LV.value()
                self.slidevalue_UH = self.ui.horizontalSlider_UH.value()
                self.slidevalue_US = self.ui.horizontalSlider_US.value()
                self.slidevalue_UV = self.ui.horizontalSlider_UV.value()
                self.ui.label_value_slider_LH.setText(str(self.slidevalue_LH))
                self.ui.label_value_slider_LS.setText(str(self.slidevalue_LS))
                self.ui.label_value_slider_LV.setText(str(self.slidevalue_LV))
                self.ui.label_value_slider_UH.setText(str(self.slidevalue_UH))
                self.ui.label_value_slider_US.setText(str(self.slidevalue_US))
                self.ui.label_value_slider_UV.setText(str(self.slidevalue_UV))
                self.num1 = self.ui.doubleSpinBox_Maxvalue_RGB_2.value()
                self.num2 = self.ui.doubleSpinBox_Maxvalue_RGB_3.value()
                self.maxD = self.ui.doubleSpinBox_Maxvalue_RGB_4.value()
                self.minD = self.ui.doubleSpinBox_Minvalue_RGB_2.value()
                self.angle = self.ui.angle_xoay.value()
                self.num3 = self.ui.distance_2object.value()
                self.items[i]=(self.items[i][0],self.maxvalue,self.minvalue,self.slidevalue_LH,self.slidevalue_LS,self.slidevalue_LV,
                               self.slidevalue_UH,self.slidevalue_US,self.slidevalue_UV,self.x, self.y, self.width, self.height,self.Pixitem,
                               self.num1, self.num2, self.maxD, self.minD, self.angle, self.num3)
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
                               slidevalue_UHp,slidevalue_USp,slidevalue_UVp,self.xp, self.yp, self.widthp, self.heightp,
                               self.Pixitemp,self.center_x, self.center_y)
                self.threadProcessImagep(j,self.xp,self.yp,self.widthp,self.heightp)
      except:
          pass
    @pyqtSlot()
    def threadProcessImage(self,index,x,y,width,height):
      try:
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
        self.ProcessImage(self.imageforprocess,index,x,y,width,height)
        self.CovertoPixmap(self.res,x,y)
        self.CreateListPixmapIterm(self.pixm, index, x, y)
      except:
        pass
    def threadProcessImagep(self,index,x,y,width,height):
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
        self.ProcessImagep(self.imageforprocess,index,x,y,width,height)
        self.CovertoPixmap(self.resp,x,y)
        self.CreateListPixmapItermp(self.pixm, index, x, y)
        self.chinh_hinh()
    @pyqtSlot()    
    def ProcessImage(self,orginalImage,index,x,y,width,height):
      try:
        if len(self.items) != 0:
           imgx, imgy, im = orginalImage.shape
           center = (self.center_x, self.center_y)
           scale = 1
           self.GetDataFromRect(index)
           M = cv2.getRotationMatrix2D(center, self.goc, scale)
           orginalImage = cv2.warpAffine(orginalImage, M, (imgy, imgx))
           crop_image = orginalImage[int(y):int(y + height), int(x):int(x + width)]
           crop_image = cv2.GaussianBlur(crop_image, (5, 5), 0)
           self.HsvColor = cv2.cvtColor(crop_image, cv2.COLOR_BGR2HSV)
           L_b = np.array([self.slidevalue_LH, self.slidevalue_LS,self.slidevalue_LV])
           U_b = np.array([self.slidevalue_UH,self.slidevalue_US,self.slidevalue_UV])
           self.mask = cv2.inRange(self.HsvColor, L_b, U_b)
           self.res = cv2.bitwise_and(crop_image, crop_image, mask=self.mask)
      except:
       pass
    def ProcessImagep(self,orginalImage,index,x,y,width,height):
      try:
       if len(self.itemp) != 0:
          self.GetDataFromRectp(index)
          crop_image = orginalImage[int(y):int(y + height), int(x):int(x + width)]
          self.HsvColorp = cv2.cvtColor(crop_image, cv2.COLOR_BGR2HSV)
          L_bp = np.array([self.slidevalue_LHp, self.slidevalue_LSp,self.slidevalue_LVp])
          U_bp = np.array([self.slidevalue_UHp,self.slidevalue_USp,self.slidevalue_UVp])
          self.maskp = cv2.inRange(self.HsvColorp, L_bp, U_bp)
          self.resp = cv2.bitwise_and(crop_image, crop_image, mask=self.maskp)
      except:
          pass
    def CovertoPixmap(self,image,x,y):
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if (image.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_BGR888
        img = QImage(image, image.shape[1], image.shape[0],image.strides[0], qformat)
        img = img.rgbSwapped()
        self.pixm = QtGui.QPixmap.fromImage(img)

    def CreateListPixmapIterm(self,pix,index,x,y):
                self.scene.removeItem(self.items[index][13])
                self.pixmapiterm = QGraphicsPixmapItem(pix)
                self.pixmapiterm.setPos(x, y)
                self.pixmapiterm.setZValue(0)
                self.scene.addItem(self.pixmapiterm)
                self.GetDataFromRect(index)
                self.items[index] = (self.itemRect, self.maxvalue, self.minvalue, self.slidevalue_LH,
                                     self.slidevalue_LS,self.slidevalue_LV,self.slidevalue_UH,
                                     self.slidevalue_US, self.slidevalue_UV,self.x, self.y, self.width, self.height,
                                     self.pixmapiterm, self.num1, self.num2, self.maxD, self.minD, self.angle, self.num3)

    def CreateListPixmapItermp(self,pix,index,x,y):
                self.scene.removeItem(self.itemp[index][13])
                self.pixmapitermp = QGraphicsPixmapItem(pix)
                self.pixmapitermp .setPos(x, y)
                self.pixmapitermp .setZValue(0)
                self.scene.addItem(self.pixmapitermp)
                self.GetDataFromRectp(index)
                self.itemp[index] = [self.itemRectp, self.maxvaluep, self.minvaluep, self.slidevalue_LHp,
                                     self.slidevalue_LSp,self.slidevalue_LVp,self.slidevalue_UHp,
                                     self.slidevalue_USp, self.slidevalue_UVp,self.xp, self.yp,
                                     self.widthp, self.heightp,self.pixmapitermp,self.center_x, self.center_y]

    def openImage(self):
        fileChoosen = QFileDialog.getOpenFileName(self, 'Open Files', 'D:\\', "Image Files (*.jpg *.png)")
        if fileChoosen[0] != '':
            self.imagepath=fileChoosen[0]
            #self.image=QPixmap(self.imagepath).scaled(640, 480, Qt.KeepAspectRatio,
                                              #Qt.SmoothTransformation)
            self.image=QPixmap(self.imagepath)
            self.scene.addPixmap(self.image)
            self.imageopen1 = cv2.imread(fileChoosen[0])
            self.imageopen = self.image.copy()
            self.imageoutside = True
        else:
            pass
    def saveimage(self):
       try:
        self.imagepath1 = self.imagepath
       except:
           pass
    def GetResult(self):
      self.noi_diem()
      self.show_center()
      if len(self.items)==0:
        self.ui.label_Result_test.setText("NG")
        self.ui.label_Result_Area.setText("No Items")
        return False
      else:
        if self.ui.radioButton.isChecked() and not self.ui.radioButton_2.isChecked() \
                and not self.ui.radioButton_3.isChecked():
                test = self.result_arer()
                if test:
                    return True
                else:
                    False
        elif not self.ui.radioButton.isChecked() and self.ui.radioButton_2.isChecked()\
                and not self.ui.radioButton_3.isChecked():
                test = self.result_height()
                if test:
                    return True
                else:
                    False
        elif not self.ui.radioButton.isChecked() and not self.ui.radioButton_2.isChecked()\
                and self.ui.radioButton_3.isChecked():
                test = self.result_width()
                if test:
                    return True
                else:
                    False
        elif self.ui.radioButton.isChecked() and self.ui.radioButton_2.isChecked() \
                and not self.ui.radioButton_3.isChecked():
                test = self.result_arer_height()
                if test:
                    return True
                else:
                    False
        elif self.ui.radioButton.isChecked() and not self.ui.radioButton_2.isChecked() \
                and self.ui.radioButton_3.isChecked():
                test = self.result_arer_width()
                if test:
                    return True
                else:
                    False
        elif not self.ui.radioButton.isChecked() and self.ui.radioButton_2.isChecked() \
                and self.ui.radioButton_3.isChecked():
                test = self.result_height_width()
                if test:
                    return True
                else:
                    False
        elif self.ui.radioButton.isChecked() and self.ui.radioButton_2.isChecked() \
                and self.ui.radioButton_3.isChecked():
                test = self.result_arer_height_width()
                if test:
                    return True
                else:
                    False
        elif not self.ui.radioButton.isChecked() and not self.ui.radioButton_2.isChecked() \
                and not self.ui.radioButton_3.isChecked() and not self.ui.radioButton_4.isChecked():
          self.ui.label_Result_test.setText("Please selection type test!")
          self.ui.label_Result_Area.setText("No result")
    def noi_diem(self):
        for i in range (len(self.items)):
            print(self.items[i][0].sceneBoundingRect().right(), self.items[i][0].sceneBoundingRect().bottom())
            self.pen = QPen(QColor(Qt.yellow))
            self.line = QGraphicsLineItem(10,120,30,50)
            self.line.setZValue(0)
            self.line.setPen(self.pen)
            self.scene.addItem(self.line)
    def result_arer(self):
        gettotalResult = 0
        for i in range(len(self.items)):
            if self.items[i][0].isSelected():
                cal = self.arer_xoay_only(i)
                if cal:
                    self.ui.label_Result_Area.setText("OK One")
                    text = "Min_area/Max_area: %d / %d" % (self.min_are, self.max_are)
                    self.ui.label_Result_test.setText(text)
                    return True
                else:
                    self.ui.label_Result_Area.setText("NG One")
                    text = "Min_area/Max_area: %d / %d" % (self.min_are, self.max_are)
                    self.ui.label_Result_test.setText(text)
                    return False
        for i in range(len(self.items)):
            cal = self.arer_xoay_only(i)
            if cal:
                gettotalResult += 1
        if gettotalResult == len(self.items):
            text = "OK Total: %d / %d" % (gettotalResult, len(self.items))
            self.ui.label_Result_test.setText(text)
            self.ui.label_Result_Area.setText("All OK")
            return True
        else:
            text = "NG Total: %d / %d" % (gettotalResult, len(self.items))
            self.ui.label_Result_test.setText(text)
            self.ui.label_Result_Area.setText("All NG")
            return False
    def result_height(self):
        gettotalResult = 0
        for i in range(len(self.items)):
            if self.items[i][0].isSelected():
                cal = self.Dis_height(i)
                if cal:
                    self.ui.label_Result_test.setText("OK One")
                    max_min = "Min_H/Max_H: %d / %d" % (self.min_height_xoay, self.max_height_xoay)
                    self.ui.label_Result_Area.setText(max_min)
                    return True
                else:
                    self.ui.label_Result_test.setText("NG One")
                    max_min = "Min_H/Max_H: %d / %d" % (self.min_height_xoay, self.max_height_xoay)
                    self.ui.label_Result_Area.setText(max_min)
                    return False
        for i in range(len(self.items)):
            cal = self.Dis_height(i)
            if cal:
                gettotalResult += 1
        if gettotalResult == len(self.items):
            text = "OK Total: %d / %d" % (gettotalResult, len(self.items))
            self.ui.label_Result_test.setText(text)
            self.ui.label_Result_Area.setText("All OK")
            return True
        else:
            text = "NG Total: %d / %d" % (gettotalResult, len(self.items))
            self.ui.label_Result_test.setText(text)
            self.ui.label_Result_Area.setText("All NG")
            return False
    def result_width(self):
        gettotalResult = 0
        for i in range(len(self.items)):
            if self.items[i][0].isSelected():
                width = self.Dis_width(i)
                if width:
                    self.ui.label_Result_test.setText("OK One")
                    max_min = "Min_W/Max_W: %d / %d" % (self.min_width_xoay, self.max_width_xoay)
                    self.ui.label_Result_Area.setText(max_min)
                    return True
                else:
                    self.ui.label_Result_test.setText("NG One")
                    max_min = "Min_W/Max_W: %d / %d" % (self.min_width_xoay, self.max_width_xoay)
                    self.ui.label_Result_Area.setText(max_min)
                    return False
        for i in range(len(self.items)):
            cal = self.Dis_width(i)
            if cal:
                gettotalResult += 1
        if gettotalResult == len(self.items):
            text = "OK Total: %d / %d" % (gettotalResult, len(self.items))
            self.ui.label_Result_test.setText(text)
            self.ui.label_Result_Area.setText("All OK")
            return True
        else:
            text = "NG Total: %d / %d" % (gettotalResult, len(self.items))
            self.ui.label_Result_test.setText(text)
            self.ui.label_Result_Area.setText("All NG")
            return False
    def result_arer_height(self):
        gettotalResult = 0
        for i in range(len(self.items)):
            if self.items[i][0].isSelected():
                cal = self.arer_xoay_only(i)
                hight = self.Dis_height(i)
                if cal and hight:
                    self.ui.label_Result_test.setText("OK One")
                    self.ui.label_Result_Area.setText("S_H OK")
                    return True
                else:
                    self.ui.label_Result_test.setText("NG One")
                    self.ui.label_Result_Area.setText("S_H NG")
                    return False
        for i in range(len(self.items)):
            cal = self.arer_xoay_only(i)
            hight = self.Dis_height(i)
            if cal and hight:
                gettotalResult += 1
        if gettotalResult == len(self.items):
            text = "OK Total: %d / %d" % (gettotalResult, len(self.items))
            self.ui.label_Result_test.setText(text)
            self.ui.label_Result_Area.setText("All S_H OK")
            return True
        else:
            text = "NG Total: %d / %d" % (gettotalResult, len(self.items))
            self.ui.label_Result_test.setText(text)
            self.ui.label_Result_Area.setText("All S_H NG")
            return False
    def result_arer_width(self):
        gettotalResult = 0
        for i in range(len(self.items)):
            if self.items[i][0].isSelected():
                cal = self.arer_xoay_only(i)
                width = self.Dis_width(i)
                if cal and width:
                    self.ui.label_Result_test.setText("OK One")
                    self.ui.label_Result_Area.setText("S_W OK")
                    return True
                else:
                    self.ui.label_Result_test.setText("NG One")
                    self.ui.label_Result_Area.setText("S_W NG")
                    return False
        for i in range(len(self.items)):
            cal = self.arer_xoay_only(i)
            width = self.Dis_width(i)
            if cal and width:
                gettotalResult += 1
        if gettotalResult == len(self.items):
            text = "OK Total: %d / %d" % (gettotalResult, len(self.items))
            self.ui.label_Result_test.setText(text)
            self.ui.label_Result_Area.setText("All S_W OK")
            return True
        else:
            text = "NG Total: %d / %d" % (gettotalResult, len(self.items))
            self.ui.label_Result_test.setText(text)
            self.ui.label_Result_Area.setText("All S_W NG")
            return False
    def result_height_width(self):
        gettotalResult = 0
        for i in range(len(self.items)):
            if self.items[i][0].isSelected():
                width = self.Dis_width(i)
                hight = self.Dis_height(i)
                if width and hight:
                    self.ui.label_Result_test.setText("OK One")
                    self.ui.label_Result_Area.setText("H_W OK")
                    return True
                else:
                    self.ui.label_Result_test.setText("NG One")
                    self.ui.label_Result_Area.setText("H_W NG")
                    return False
        for i in range(len(self.items)):
            width = self.Dis_width(i)
            hight = self.Dis_height(i)
            if width and hight:
                gettotalResult += 1
        if gettotalResult == len(self.items):
            text = "OK Total: %d / %d" % (gettotalResult, len(self.items))
            self.ui.label_Result_test.setText(text)
            self.ui.label_Result_Area.setText("All H_W OK")
            return True
        else:
            text = "NG Total: %d / %d" % (gettotalResult, len(self.items))
            self.ui.label_Result_test.setText(text)
            self.ui.label_Result_Area.setText("All H_W NG")
            return False
    def result_arer_height_width(self):
        gettotalResult = 0
        for i in range(len(self.items)):
            if self.items[i][0].isSelected():
                cal = self.arer_xoay_only(i)
                hight = self.Dis_height(i)
                width = self.Dis_width(i)
                if cal and hight and width:
                    self.ui.label_Result_test.setText("OK One")
                    self.ui.label_Result_Area.setText("S_H_W OK")
                    return True
                else:
                    self.ui.label_Result_test.setText("NG One")
                    self.ui.label_Result_Area.setText("S_H_W NG")
                    return False
        for i in range(len(self.items)):
            cal = self.arer_xoay_only(i)
            hight = self.Dis_height(i)
            width = self.Dis_width(i)
            if cal and hight and width:
                gettotalResult += 1
        if gettotalResult == len(self.items):
            text = "OK Total: %d / %d" % (gettotalResult, len(self.items))
            self.ui.label_Result_test.setText(text)
            self.ui.label_Result_Area.setText("All OK")
            return True
        else:
            text = "NG Total: %d / %d" % (gettotalResult, len(self.items))
            self.ui.label_Result_test.setText(text)
            self.ui.label_Result_Area.setText("All NG")
            return False
    def tinh_goc(self,index):
      self.GetDataFromRect(index)
      if self.items[index][18]!=0:
        dem_goc = int(360 / self.items[index][18])
        return dem_goc
    def arer_xoay_only(self,index):
        self.Number = self.ui.tru_diem.value()
        test_NG = 0
        mang_are = []
        self.goc = 0
        if self.angle==0:
            dem_goc = 0
        else:
            dem_goc = self.tinh_goc(index)
        self.loaidiem()
        if self.angle != 0 and len(self.itemp) != 0:
            for i in range(0,dem_goc):
                self.xoay_rect(index)
                if i not in self.loai_diem:
                  area_only = self.are_xoay(index)
                  mang_are.append(area_only)
                  if self.minvalue > area_only or area_only > self.maxvalue:
                      cenx, ceny = self.center_rect(index)
                      cenx_xoay,ceny_xoay = self.xoay_diem(self.center_x,self.center_y,cenx,ceny,self.goc)
                      self.draw_circle(cenx_xoay,ceny_xoay)
                      test_NG += 1
                else:
                    cenx, ceny = self.center_rect(index)
                    cenx_xoay, ceny_xoay = self.xoay_diem(self.center_x, self.center_y, cenx, ceny, self.goc)
                    self.draw_circle_xanh(cenx_xoay, ceny_xoay)
                self.goc += self.angle
            self.max_are = max(mang_are)
            self.min_are = min(mang_are)
            if test_NG <= self.num3:
                return True
            else:
                return False
        elif self.angle == 0 :
            test_NG0 = 0
            area_only = self.are_xoay(index)
            mang_are.append(area_only)
            self.max_are = max(mang_are)
            self.min_are = min(mang_are)
            if self.minvalue > area_only or area_only > self.maxvalue:
                cenx, ceny = self.center_rect(index)
                cenx_xoay, ceny_xoay = self.xoay_diem(self.center_x, self.center_y, cenx, ceny, self.goc)
                self.draw_circle(cenx_xoay, ceny_xoay)
                test_NG0 += 1
            if test_NG0 > self.num3:
                return False
            else:
                return True
    def mang_height_only(self, index):
        mang_x = []
        height_x = []
        height_xm = []
        mang_Dish = []
        if self.imageoutside:
            self.imageforprocess = self.imageopen1
        else:
            self.imageforprocess = self.frame
        self.GetDataFromRect(index)
        self.ProcessImage(self.imageforprocess, index,self.x, self.y, self.width, self.height)
        contours, hierarchy = cv2.findContours(self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) == 0 or len(hierarchy) == 0 or self.num1==0:
            self.max_height_xoay_only = self.min_height_xoay_only = 0
            return False
        else:
            contour = max(contours, key=cv2.contourArea)
            min_ar = (np.amin(contour, axis=0))
            self.min_x = min_ar[0][0]
            max_ar = (np.amax(contour, axis=0))
            self.max_x = max_ar[0][0]
            self.max_y = max_ar[0][1]
            self.min_y = min_ar[0][1]
            kc_x = self.min_x
            if 0 <= self.num1 < self.max_x:
                for i in range(1, len(contour)):
                    kc_x = kc_x + int(self.max_x / (self.num1 + 1))
                    if 0 <= len(mang_x) < self.num1 and kc_x <= self.max_x:
                        mang_x.append(kc_x)
            if len(mang_x) < self.num1:
                mang_x.append(self.max_x - 2)
            for i in range(len(mang_x)):
                for j in range(1, len(contour)):
                    if contour[j][0][0] == mang_x[i]:
                        height_x.append(contour[j])
            i = 0
            while (1):
                if i < len(height_x) - 1:
                    if height_x[i][0][0] == height_x[i + 1][0][0]:
                        height_xm.append([height_x[i], height_x[i + 1]])
                        i = i + 2
                    else:
                        i = i + 3
                else:
                    break
            for i7 in range(len(height_xm)):
                self.pen = QPen(QColor(Qt.yellow))
                pointx_line1,pointx_line2 = height_xm[i7][0][0][0] + self.x, height_xm[i7][0][0][1] + self.y
                pointy_line1,pointy_line2 = height_xm[i7][1][0][0] + self.x, height_xm[i7][1][0][1] + self.y
                pointx1, pointx2,pointy1,pointy2 = self.xoay_line(pointx_line1,pointx_line2, pointy_line1,pointy_line2)
                self.line = QGraphicsLineItem(pointx1, pointx2,pointy1,pointy2)
                self.line.setZValue(0)
                self.line.setPen(self.pen)
                self.scene.addItem(self.line)
                # tao duong mui ten
                numline = 30
                div_line = int((height_xm[i7][0][0][1] - height_xm[i7][1][0][1]) / numline)

                y_div = height_xm[i7][1][0][1] + self.y + div_line
                x_div1 = height_xm[i7][1][0][0] + self.x - div_line
                x_div2 = height_xm[i7][1][0][0] + self.x + div_line

                y_divd = height_xm[i7][0][0][1] + self.y - div_line
                x_divd1 = height_xm[i7][0][0][0] + self.x - div_line
                x_divd2 = height_xm[i7][0][0][0] + self.x + div_line

                self.pen1 = QPen(QColor(Qt.blue))
                y_line1, y_line2 = height_xm[i7][1][0][0] + self.x, height_xm[i7][1][0][1] + self.y
                x1, x2, y1, y2 = self.xoay_line(x_div1, y_div, y_line1, y_line2)
                self.line1 = QGraphicsLineItem(x1, x2, y1, y2)
                self.line1.setZValue(0)
                self.line1.setPen(self.pen1)
                self.scene.addItem(self.line1)

                self.pen2 = QPen(QColor(Qt.blue))
                y_line, y_line2 = height_xm[i7][1][0][0] + self.x, height_xm[i7][1][0][1] + self.y
                x1, x2, y1, y2 = self.xoay_line(x_div2, y_div, y_line1, y_line2)
                self.line2 = QGraphicsLineItem(x1, x2, y1, y2)
                self.line2.setZValue(0)
                self.line2.setPen(self.pen2)
                self.scene.addItem(self.line2)

                self.pen3 = QPen(QColor(Qt.blue))
                y_line, y_line2 = height_xm[i7][0][0][0] + self.x, height_xm[i7][0][0][1] + self.y
                x1, x2, y1, y2 = self.xoay_line(x_divd1, y_divd, y_line1, y_line2)
                self.line3 = QGraphicsLineItem(x1, x2, y1, y2)
                self.line3.setZValue(0)
                self.line3.setPen(self.pen3)
                self.scene.addItem(self.line3)

                self.pen4 = QPen(QColor(Qt.blue))
                y_line, y_line2 = height_xm[i7][0][0][0] + self.x, height_xm[i7][0][0][1] + self.y
                x1, x2, y1, y2 = self.xoay_line(x_divd2, y_divd, y_line1, y_line2)
                self.line4 = QGraphicsLineItem(x1, x2, y1, y2)
                self.line4.setZValue(0)
                self.line4.setPen(self.pen3)
                self.scene.addItem(self.line4)
                self.Distance_h1 = dist.euclidean((height_xm[i7][0][0][0], height_xm[i7][0][0][1]),
                                                 (height_xm[i7][1][0][0], height_xm[i7][1][0][1]))
                mang_Dish.append(self.Distance_h1)
            if len(mang_Dish)!=0:
               self.max_height_xoay_only = max(mang_Dish)
               self.min_height_xoay_only = min(mang_Dish)
            else:
                self.max_height_xoay_only = self.min_height_xoay_only = 0
            if self.minD<=self.max_height_xoay_only<=self.maxD and\
                    self.minD<=self.min_height_xoay_only<=self.maxD:
                return True
            else:
                return False
    def mang_width_only(self,index):
        mang_y = []
        width_y = []
        width_ym = []
        mang_Dish = []
        if self.imageoutside:
            self.imageforprocess = self.imageopen1
        else:
            self.imageforprocess = self.frame
        self.GetDataFromRect(index)
        self.ProcessImage(self.imageforprocess, index, self.x, self.y, self.width, self.height)
        contours, hierarchy = cv2.findContours(self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) == 0 or len(hierarchy) == 0 or self.num2 == 0:
            self.max_width_xoay_only = self.min_width_xoay_only = 0
            return False
        else:
            contour = max(contours, key=cv2.contourArea)
            min_ar = (np.amin(contour, axis=0))
            self.min_y = min_ar[0][1]
            max_ar = (np.amax(contour, axis=0))
            self.max_y = max_ar[0][1]
            kc_y = self.min_y
            if 0 < self.num2 < self.max_y:
                for i in range(1, len(contour)):
                    kc_y = kc_y + int(self.max_y / (self.num2 + 1))
                    if 0 <= len(mang_y) < self.num2 and kc_y <= self.max_y:
                        mang_y.append(kc_y)
            if len(mang_y) < self.num2:
                mang_y.append(self.max_y - 2)
            for i in range(len(mang_y)):
                for j in range(1, len(contour)):
                    if contour[j][0][1] == mang_y[i]:
                        width_y.append(contour[j])
            i = 0
            while (1):
                if i < len(width_y) - 1:
                    if width_y[i][0][1] == width_y[i + 1][0][1]:
                        width_ym.append([width_y[i], width_y[i + 1]])
                        i = i + 2
                    else:
                        i = i + 3
                else:
                    break
            for i7 in range(len(width_ym)):
                self.pen = QPen(QColor(Qt.yellow))
                pointx_line1, pointx_line2 = width_ym[i7][0][0][0] + self.x, width_ym[i7][0][0][1] + self.y
                pointy_line1, pointy_line2 = width_ym[i7][1][0][0] + self.x, width_ym[i7][1][0][1] + self.y
                pointx1, pointx2, pointy1, pointy2 = self.xoay_line(pointx_line1, pointx_line2, pointy_line1,
                                                                    pointy_line2)
                self.line = QGraphicsLineItem(pointx1, pointx2, pointy1, pointy2)
                self.line.setZValue(0)
                self.line.setPen(self.pen)
                self.scene.addItem(self.line)
                # tao duong mui ten
                numline = 30
                div_line = int((width_ym[i7][0][0][0] - width_ym[i7][1][0][0]) / numline)

                x_div = width_ym[i7][1][0][0] + self.x + div_line
                y_div1 = width_ym[i7][1][0][1] + self.y - div_line
                y_div2 = width_ym[i7][1][0][1] + self.y + div_line

                x_divd = width_ym[i7][0][0][0] + self.x - div_line
                y_divd1 = width_ym[i7][0][0][1] + self.y - div_line
                y_divd2 = width_ym[i7][0][0][1] + self.y + div_line

                self.pen1 = QPen(QColor(Qt.blue))
                y_line1, y_line2 = width_ym[i7][1][0][0] + self.x, width_ym[i7][1][0][1] + self.y
                x1, x2, y1, y2 = self.xoay_line(x_div, y_div1, y_line1, y_line2)
                self.line1 = QGraphicsLineItem(x1, x2, y1, y2)
                self.line1.setZValue(0)
                self.line1.setPen(self.pen1)
                self.scene.addItem(self.line1)

                self.pen2 = QPen(QColor(Qt.blue))
                y_line, y_line2 = width_ym[i7][1][0][0] + self.x, width_ym[i7][1][0][1] + self.y
                x1, x2, y1, y2 = self.xoay_line(x_div, y_div2, y_line1, y_line2)
                self.line2 = QGraphicsLineItem(x1, x2, y1, y2)
                self.line2.setZValue(0)
                self.line2.setPen(self.pen2)
                self.scene.addItem(self.line2)

                self.pen3 = QPen(QColor(Qt.blue))
                y_line3, y_line4 = width_ym[i7][0][0][0] + self.x, width_ym[i7][0][0][1] + self.y
                x1, x2, y1, y2 = self.xoay_line(x_divd, y_divd1, y_line3, y_line4)
                self.line3 = QGraphicsLineItem(x1, x2, y1, y2)
                self.line3.setZValue(0)
                self.line3.setPen(self.pen3)
                self.scene.addItem(self.line3)

                self.pen4 = QPen(QColor(Qt.blue))
                y_line3, y_line4 = width_ym[i7][0][0][0] + self.x, width_ym[i7][0][0][1] + self.y
                x1, x2, y1, y2 = self.xoay_line(x_divd, y_divd2, y_line3, y_line4)
                self.line4 = QGraphicsLineItem(x1, x2, y1, y2)
                self.line4.setZValue(0)
                self.line4.setPen(self.pen3)
                self.scene.addItem(self.line4)
                self.Distance_w = dist.euclidean((width_ym[i7][0][0][0], width_ym[i7][0][0][1]),
                                                 (width_ym[i7][1][0][0], width_ym[i7][1][0][1]))
                mang_Dish.append(self.Distance_w)
            if len(mang_Dish) != 0:
                self.max_width_xoay_only = max(mang_Dish)
                self.min_width_xoay_only = min(mang_Dish)
            else:
                self.max_width_xoay_only = self.min_width_xoay_only = 0
            if self.minD <= self.max_width_xoay_only <= self.maxD and \
                    self.minD <= self.min_width_xoay_only <= self.maxD:
                return True
            else:
                return False
    def are_xoay(self,index):
        arear = 0
        if self.imageoutside:
            self.imageforprocess = self.imageopen1
        else:
            self.imageforprocess = self.frame
        self.GetDataFromRect(index)
        self.ProcessImage(self.imageforprocess, index, self.x, self.y, self.width, self.height)
        gray = cv2.cvtColor(self.res, cv2.COLOR_BGR2GRAY)
        contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0 or len(hierarchy) == 0:
            self.ui.label_Result_Area.setText("Area is None")
            arear = 0
            return arear
        for i in range(len(contours)):
            arear = cv2.contourArea(contours[i]) / 100 + arear
        return arear
    def center_are(self,mask):
       try:
        if self.imageoutside:
            self.imageforprocess = self.imageopen1
        else:
            self.imageforprocess = self.frame
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0 or len(hierarchy) == 0:
            self.ui.label_Result_Area.setText("Area is No have")
        contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(contour)
        self.cx = int(M['m10'] / M['m00'])
        self.cy = int(M['m01'] / M['m00'])
       except:
              pass
    def show_center(self):
        if len(self.itemp) != 0:
            self.center_position()
            self.pen = QPen(QColor(Qt.yellow))
            self.center = QGraphicsEllipseItem(self.center_x, self.center_y, 5, 5)
            self.center.setZValue(0)
            self.center.setPen(self.pen)
            self.scene.addItem(self.center)
        else:
            pass
    def center_position(self):
      try:
        self.center_are(self.maskp)
        self.center_x = self.cx  + self.xp
        self.center_y = self.cy + self.yp
      except:
        pass
    def chinh_hinh(self):
        self.center_position()
        if len(self.itemp) == 0 :
            self.center_XL = 0
            self.center_YL = 0
        else:
            self.center_XL = self.center_x - self.itemp[0][14]
            self.center_YL = self.center_y - self.itemp[0][15]

            self.itemp[0][14] = self.center_x
            self.itemp[0][15] = self.center_y
        for i in range(len(self.items)):
            self.GetDataFromRect(i)
            self.x_lech = self.center_XL
            self.y_lech = self.center_YL
            self.items[i][0].moveBy(self.x_lech, self.y_lech)
            self.threadProcessImage(i, self.x, self.y, self.width, self.height)
    def Dis_height(self,index):
        mang_max_height_xoay = []
        mang_min_height_xoay = []
        test_NG = 0
        self.goc = 0
        self.GetDataFromRect(index)
        if self.angle == 0:
            dem_goc = 1
        else:
            dem_goc = self.tinh_goc(index)
        self.loaidiem()
        if self.num1 != 0:
            for i in range(0,dem_goc):
                self.xoay_rect(index)
                if i not in self.loai_diem:
                    test_height_xoay = self.mang_height_only(index)
                    mang_max_height_xoay.append(self.max_height_xoay_only)
                    mang_min_height_xoay.append(self.min_height_xoay_only)
                    if test_height_xoay == False:
                       test_NG += 1
                       cenx, ceny = self.center_rect(index)
                       cenx_xoay, ceny_xoay = self.xoay_diem(self.center_x, self.center_y, cenx, ceny, self.goc)
                       self.draw_circle(cenx_xoay, ceny_xoay)
                else:
                    cenx, ceny = self.center_rect(index)
                    cenx_xoay, ceny_xoay = self.xoay_diem(self.center_x, self.center_y, cenx, ceny, self.goc)
                    self.draw_circle_xanh(cenx_xoay, ceny_xoay)
                self.goc += self.angle
            self.max_height_xoay = max(mang_max_height_xoay)
            self.min_height_xoay = min(mang_min_height_xoay)
            if test_NG <= self.num3:
                return True
            else:
                return False
        else:
            self.max_height_xoay = self.min_height_xoay = 0
            return False
    def Dis_width(self,index):
        test_NG = 0
        mang_max_width_xoay = []
        mang_min_width_xoay = []
        self.goc = 0
        self.GetDataFromRect(index)
        if self.angle == 0:
            dem_goc = 1
        else:
            dem_goc = self.tinh_goc(index)
        self.loaidiem()
        if self.num2 != 0:
            for i in range(0, dem_goc):
                self.xoay_rect(index)
                if i not in self.loai_diem:
                   test_width_xoay = self.mang_width_only(index)
                   mang_max_width_xoay.append(self.max_width_xoay_only)
                   mang_min_width_xoay.append(self.min_width_xoay_only)
                   if test_width_xoay == False:
                       test_NG += 1
                       cenx, ceny = self.center_rect(index)
                       cenx_xoay, ceny_xoay = self.xoay_diem(self.center_x, self.center_y, cenx, ceny, self.goc)
                       self.draw_circle(cenx_xoay, ceny_xoay)
                else:
                    cenx, ceny = self.center_rect(index)
                    cenx_xoay, ceny_xoay = self.xoay_diem(self.center_x, self.center_y, cenx, ceny, self.goc)
                    self.draw_circle_xanh(cenx_xoay, ceny_xoay)
                self.goc += self.angle
            self.max_width_xoay = max(mang_max_width_xoay)
            self.min_width_xoay = min(mang_min_width_xoay)
            if test_NG <= self.num3:
                return True
            else:
                return False
        else:
            self.max_width_xoay = self.min_width_xoay = 0
            return False
    def setValueZ(self):
        j = 0
        for i in range(len(self.items)):
            if self.items[i][0].isSelected():
                j = j+1
        if j == 0:
            self.img = self.scene.addPixmap(QPixmap(self.image))
            self.img.setZValue(0)
    def Rectchild(self,valx,valy):
        self.chon_hcnx.clear()
        self.chon_hcny.clear()
        for i in range (len(self.items)):
            self.xt_gan = abs(self.items[i][0].sceneBoundingRect().left() - valx + 4)
            self.xp_gan = abs(self.items[i][0].sceneBoundingRect().right()  - valx-4)
            self.yt_gan = abs(self.items[i][0].sceneBoundingRect().top() - valy + 4)
            self.yp_gan = abs(self.items[i][0].sceneBoundingRect().bottom() - valy - 4)
            if self.xt_gan>=self.xp_gan :
                self.chon_hcnx.append(self.xp_gan)
            elif self.xt_gan<self.xp_gan :
                self.chon_hcnx.append(self.xt_gan)
            if self.yt_gan>=self.yp_gan :
                self.chon_hcny.append(self.yp_gan)
            elif self.yt_gan<self.yp_gan :
                self.chon_hcny.append(self.yt_gan)
        if len(self.itemp)!=0:
            self.xt_ganp = abs(self.itemp[0][0].sceneBoundingRect().left() - valx + 4)
            self.xp_ganp = abs(self.itemp[0][0].sceneBoundingRect().right() - valx - 4)
        if len(self.chon_hcnx)!=0 and len(self.itemp)!=0:
           min_hcn = min(self.chon_hcnx)
           for i in range (len(self.chon_hcnx)):
             if min_hcn!=self.chon_hcnx[i]:
                 self.items[i][0].setFlag(QGraphicsItem.ItemIsSelectable, False)
                 self.items[i][0].setFlag(QGraphicsItem.ItemIsMovable, False)
             elif min_hcn==self.chon_hcnx[i] and min_hcn<self.xt_ganp and min_hcn<self.xp_ganp:
                 self.items[i][0].setFlag(QGraphicsItem.ItemIsSelectable, True)
                 self.items[i][0].setFlag(QGraphicsItem.ItemIsMovable, True)
                 self.itemp[0][0].setFlag(QGraphicsItem.ItemIsSelectable, False)
                 self.itemp[0][0].setFlag(QGraphicsItem.ItemIsMovable, False)
             elif min_hcn==self.chon_hcnx[i] and min_hcn>=self.xt_ganp or min_hcn>=self.xp_ganp:
                 self.itemp[0][0].setFlag(QGraphicsItem.ItemIsSelectable, True)
                 self.itemp[0][0].setFlag(QGraphicsItem.ItemIsMovable, True)
                 self.items[i][0].setFlag(QGraphicsItem.ItemIsSelectable, False)
                 self.items[i][0].setFlag(QGraphicsItem.ItemIsMovable, False)
        elif len(self.chon_hcnx)!=0 or len(self.chon_hcny)!=0:
            if len(self.itemp)==0 :
               min_hcnx = min(self.chon_hcnx)
               min_hcny = min(self.chon_hcny)
               j = 0
               for i in range(len(self.items)):
                   if self.items[i][0].sceneBoundingRect().left() + 4 < valx < self.items[i][0].sceneBoundingRect().right() - 4:
                      if self.items[i][0].sceneBoundingRect().top() + 4 < valy < self.items[i][0].sceneBoundingRect().bottom()-4:
                          j = j+1
                          if min_hcnx != self.chon_hcnx[i] and min_hcny != self.chon_hcny[i]:
                              self.items[i][0].setFlag(QGraphicsItem.ItemIsSelectable, False)
                              self.items[i][0].setFlag(QGraphicsItem.ItemIsMovable, False)
                          elif min_hcnx == self.chon_hcnx[i] or min_hcny == self.chon_hcny[i]:
                              self.items[i][0].setFlag(QGraphicsItem.ItemIsSelectable, True)
                              self.items[i][0].setFlag(QGraphicsItem.ItemIsMovable, True)

class QGraphicsView(QGraphicsView):
    clickItems = pyqtSignal(int,int)
    moveItems = pyqtSignal(int, int)
    def __init__(self, *args):
        super().__init__(*args)
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        valx = event.pos().x()
        valy = event.pos().y()
        self.clickItems.emit(valx, valy)
    def mouseMoveEvent(self,event):
        super().mouseMoveEvent(event)
        if event.buttons() == QtCore.Qt.LeftButton:
            valx=event.pos().x()
            valy=event.pos().y()
            self.moveItems.emit(valx,valy)

class WorkThread(QThread):
    letdoit = pyqtSignal()
    Error = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.stopserial=True
        self.check = False
        self.check1=False
    def run(self):
        list=['COM1','COM2','COM3','COM4','COM5','COM6','COM7','COM8','COM9','COM10','COM11','COM12','COM13','COM14','COM15','COM16','COM17','COM18',]



        COM1='COM1'
        COM2='COM2'
        COM3='COM3'
        COM4='COM4'
        COM5='COM5'
        COM6='COM6'
        COM7='COM7'
        COM8='COM8'
        COM9='COM9'
        COM10='COM10'
        COM11='COM11'
        COM12='COM12'
        COM13='COM13'
        COM14='COM14'
        COM15='COM15'
        COM16='COM16'
        COM17='COM17'
        COM18='COM18'
        COM19='COM19'

        i=1
        
        while(1):
                 #ports = serial.tools.list_ports.comports(include_links=False)
                 #print("number",len(ports))
               
                 port = list[i]
                 try:
                   if self.check==False:
                         self.ser = serial.Serial(port)
                         if self.ser.isOpen():
                             self.ser.close()
                             self.ser = serial.Serial(port, 9600,timeout=2)
                             self.check = True
                             self.check1= True
                   data = self.ser.readline().decode("utf-8").strip('\n').strip('\r')
                   time.sleep(0.3)
                   if data == "SenSor In" and self.stopserial==False:
                        self.letdoit.emit()
                 except :
                  print('waiting')
                  i=i+1
                  if i==18:
                      break
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
    def Send_OK(self,data_arduino):
        Sending = bytearray(data_arduino)
        self.ser.write(Sending)
if __name__=="__main__":
    app = QApplication(sys.argv)
    V = app.desktop().screenGeometry()
    h = V.height()
    w = V.width()
    f = Foster_app(h,w)
    f.show()
    sys.exit(app.exec_())

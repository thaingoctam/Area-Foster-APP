# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5.QtCore import *
import numpy as np
from .UI.Settingwindown_UI import *
from .UI.SVG import *
from .DrawRect import *
from .SaveAndReadFile import *
import cv2
from scipy.spatial import distance as dist
import math
from builtins import *
import glob, os
from pathlib import Path
from toucamera import *


class Setting_Windown(QMainWindow):
    def __init__(self, dialog, image, frame, name):
        super().__init__()
        self.name = name
        self.ui = Ui_MainWindow()
        self.ui.setupUi(dialog, self.name)
        self.xuat_kq = []
        self.xuat_so = []
        self.xuat_so_all = []
        self.noi_diem = []
        self.loai_diem = []
        self.dem_chon = 0
        self.goc = 0
        self.chon_hcnx = []
        self.chon_hcny = []
        self.itemp = []
        self.items = []
        self.loai_diem = []
        self.frame = frame
        self.image = image
        self.imageoutside = False
        self.isCapturing = False
        self.center_x = 0
        self.center_y = 0
        self.URLfile = ""
        self.SandRFile = SaveAndRead(name)
        self.listPort = self.SandRFile.getPort()
        self.scene = QGraphicsScene()  # Lop quan ly 2D
        self.scene.setSceneRect(0, 0, 640, 480)
        self.scene.addPixmap(QPixmap(self.image))
        self.grview = QGraphicsView(self.scene,
                                    self.ui.label_ImageSetting)  # lop cung cap Widget de hien thi QGraphicsScene
        self.grview.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.valueslide = self.ui.horizontalSlider_LH.value()
        self.initiateRect("", False)
        self.innitalProcessImage()
        self.innitalProcessImagep()
        self.ui.pushButton_Live.toggled.connect(self.start_cam1)
        self.ui.pushButton_DrawRect.clicked.connect(self.drawrect)
        self.ui.pushButton_Position.clicked.connect(self.Position)
        self.ui.pushButton_RemoveARect.clicked.connect(self.removerect)
        self.ui.pushButton_SaveAllParameter.clicked.connect(self.saveAsData)
        self.ui.pushButton_OpenImg.clicked.connect(self.openImage)
        self.ui.pushButton_testSample.clicked.connect(self.GetResult)
        self.ui.pushButton_ClearAll.clicked.connect(self.delete_all)
        self.ui.pushButton_OpenFileParameter.clicked.connect(self.openFParameter)
        self.ui.pushButton_Apply.clicked.connect(lambda: self.saveData(self.URLfile))
        self.grview.moveItems.connect(self.MoveItems)
        self.grview.clickItems.connect(self.showParameter)
        self.grview.clickItems.connect(self.setValueZ)
        self.grview.clickItems.connect(self.Rectchild)
        dialog.close_setting.connect(self.stop_cam)

        self.ui.spinBox_Angle.editingFinished.connect(self.UpdateDataOnList)
        self.ui.spinBox_MaxArea.editingFinished.connect(self.UpdateDataOnList)
        self.ui.spinBox_MinArea.editingFinished.connect(self.UpdateDataOnList)
        self.ui.spinBox_MinDistance.editingFinished.connect(self.UpdateDataOnList)
        self.ui.spinBox_MaxDistance.editingFinished.connect(self.UpdateDataOnList)
        self.ui.spinBox_Num.editingFinished.connect(self.UpdateDataOnList)
        self.ui.spinBox_NumW.editingFinished.connect(self.UpdateDataOnList)
        self.ui.spinBox_NumO.editingFinished.connect(self.UpdateDataOnList)
        self.ui.spinBox_NumH.editingFinished.connect(self.UpdateDataOnList)
        self.ui.spinBox_Nothing.editingFinished.connect(self.UpdateDataOnList)
        self.ui.horizontalSlider_LH.valueChanged.connect(self.UpdateDataOnList)
        self.ui.horizontalSlider_LS.valueChanged.connect(self.UpdateDataOnList)
        self.ui.horizontalSlider_LV.valueChanged.connect(self.UpdateDataOnList)
        self.ui.horizontalSlider_UH.valueChanged.connect(self.UpdateDataOnList)
        self.ui.horizontalSlider_US.valueChanged.connect(self.UpdateDataOnList)
        self.ui.horizontalSlider_UV.valueChanged.connect(self.UpdateDataOnList)
        self.ui.spinBox_Num.setEnabled(True)

    def start_cam1(self):
        if self.ui.pushButton_Live.isChecked():
            if self.name == "cam1_setting":
                self.isCapturing = True
                self.fps = 24
                self.cap1 = cv2.VideoCapture(int(self.listPort[0]))
                self.Starttime()
            elif self.name == "cam2_setting":
                self.isCapturing = True
                self.fps = 24
                self.cap2 = cv2.VideoCapture(int(self.listPort[1]))
                self.Starttime()
        else:
            self.stop_cam()

    def Starttime(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.Display_cam)
        self.timer.start(1000. / self.fps)

    def Display_cam(self):
        try:
            if self.name == "cam1_setting" and self.cap1.isOpened():
                try:
                    self.scene.removeItem(self.pixmapiterm)
                except:
                    pass
                ret, self.frame = self.cap1.read()
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                self.imageforprocess2 = cv2.resize(src=self.frame, dsize=(640, 480))
                img = QtGui.QImage(self.imageforprocess2, self.imageforprocess2.shape[1],
                                   self.imageforprocess2.shape[0], QtGui.QImage.Format_RGB888)

                pixm = QtGui.QPixmap.fromImage(img)
                self.pixmapiterm = QGraphicsPixmapItem(pixm)
                self.scene.addItem(self.pixmapiterm)
                QtCore.QCoreApplication.processEvents()
                self.image = pixm
            elif self.name == "cam2_setting" and self.cap2.isOpened():
                try:
                    self.scene.removeItem(self.pixmapiterm)
                except:
                    pass
                ret, self.frame = self.cap2.read()
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                self.imageforprocess2 = cv2.resize(src=self.frame, dsize=(640, 480))
                img = QtGui.QImage(self.imageforprocess2, self.imageforprocess2.shape[1],
                                   self.imageforprocess2.shape[0], QtGui.QImage.Format_RGB888)
                self.pixm = QtGui.QPixmap.fromImage(img)
                self.pixmapiterm = QGraphicsPixmapItem(self.pixm)
                self.scene.addItem(self.pixmapiterm)
                QtCore.QCoreApplication.processEvents()
                self.image = self.pixm
        except:
            pass

    def stop_cam(self):
        if self.isCapturing:
            self.isCapturing = False
            self.timer.stop()
            if self.name == "cam1_setting":
                self.cap1.release()
            elif self.name == "cam2_setting":
                self.cap2.release()
            cv2.destroyAllWindows()


    def MoveItems(self):
        for i in range(len(self.items)):
            if self.items[i][0].isSelected():
                self.GetDataFromRect(i)
                self.threadProcessImage(i, self.x, self.y, self.width, self.height)
        for j in range(len(self.itemp)):
            if self.itemp[j][0].isSelected():
                self.GetDataFromRectp(j)
                self.threadProcessImagep(j, self.xp, self.yp, self.widthp, self.heightp)

    def openFParameter(self):
        fileName = self.SandRFile.openFileDialog()
        if fileName:
            self.initiateRect(fileName, True)
            self.dropdownBox(fileName)

    def dropdownBox(self, URLfile):
        try:
            if URLfile:
                p = Path(URLfile)
                os.chdir(p.parent)
                self.URLfile = URLfile.replace(".txt", "")
                if (os.path.exists(URLfile)):
                    fileName = URLfile.split("/")[-1]
                    self.ui.comboBox_Parameter.setItemText(0, fileName)
                    i = 1
                    for file in glob.glob("*.txt"):
                        if file != fileName:
                            self.ui.comboBox_Parameter.setItemText(i, file)
                            i = i + 1
                else:
                    self.ui.comboBox_Parameter.setItemText(0, "New File")
            else:
                pass
        except:
            print("Url config wrong")
            pass

    @pyqtSlot()
    def saveAsData(self):
        self.test_pin = True
        filename = self.SandRFile.saveFileDialog()
        f = open(filename + ".txt", "w+")
        f.close()
        self.Measure()
        if filename and self.URLfile:
            self.SandRFile.saveAsFile(self.URLfile, filename, self.items, self.itemp, self.loai_diem, self.Area,
                                      self.Distance,
                                      self.Distancew, self.Number, self.test_pin, self.all_area)
            self.ui.label_fsave_notification.setText("New file has been saved")
        else:
            self.saveData(filename)
        self.dropdownBox(filename + ".txt")

    def saveData(self, URL):
        self.test_pin = True
        self.Measure()
        fNotFound = self.SandRFile.saveFile(URL, self.items, self.itemp, self.loai_diem, self.Area, self.Distance,
                                            self.Distancew, self.Number, self.test_pin, self.all_area)
        if not fNotFound:
            self.ui.label_fsave_notification.setText("File not found")
            self.saveAsData()
        else:
            self.ui.label_fsave_notification.setText("Save/Apply Success")

    def SaveDataOnList(self):
        for i in range(len(self.items)):
            if self.items[i][0].isSelected():
                self.GetDataFromRect(i)
                self.items[i] = [self.itemRect, self.maxvalue, self.minvalue, self.slidevalue_LH, self.slidevalue_LS,
                                 self.slidevalue_LV, self.slidevalue_UH, self.slidevalue_US, self.slidevalue_UV, self.x,
                                 self.y, self.width, self.height, self.Pixitem, self.num1, self.num2, self.maxD,
                                 self.minD, self.angle, self.num3, self.khoi]
                self.threadProcessImage(i, self.x, self.y, self.width, self.height)

        for j in range(len(self.itemp)):
            if self.itemp[j][0].isSelected():
                self.GetDataFromRectp(j)
                self.itemp[j] = [self.itemRectp, self.maxvaluep, self.minvaluep, self.slidevalue_LHp,
                                 self.slidevalue_LSp,
                                 self.slidevalue_LVp, self.slidevalue_UHp, self.slidevalue_USp, self.slidevalue_UVp,
                                 self.xp, self.yp, self.widthp, self.heightp, self.Pixitemp,
                                 self.center_x, self.center_y]
                self.threadProcessImagep(j, self.xp, self.yp, self.widthp, self.heightp)

    def docdiem(self):
        self.loaidiem()
        if len(self.loai_diem) == 6:
            self.diem1 = self.loai_diem[0]
            self.diem2 = self.loai_diem[1]
            self.diem3 = self.loai_diem[2]
            self.diem4 = self.loai_diem[3]
            self.diem5 = self.loai_diem[4]
            self.diem6 = self.loai_diem[5]
        if len(self.loai_diem) == 5:
            self.diem1 = self.loai_diem[0]
            self.diem2 = self.loai_diem[1]
            self.diem3 = self.loai_diem[2]
            self.diem4 = self.loai_diem[3]
            self.diem5 = self.loai_diem[4]
            self.diem6 = self.diem5
        if len(self.loai_diem) == 4:
            self.diem1 = self.loai_diem[0]
            self.diem2 = self.loai_diem[1]
            self.diem3 = self.loai_diem[2]
            self.diem4 = self.loai_diem[3]
            self.diem5 = self.diem6 = self.diem4
        if len(self.loai_diem) == 3:
            self.diem1 = self.loai_diem[0]
            self.diem2 = self.loai_diem[1]
            self.diem3 = self.loai_diem[2]
            self.diem5 = self.diem6 = self.diem4 = self.diem3
        if len(self.loai_diem) == 2:
            self.diem1 = self.loai_diem[0]
            self.diem2 = self.loai_diem[1]
            self.diem5 = self.diem6 = self.diem4 = self.diem3 = self.diem2
        if len(self.loai_diem) == 1:
            self.diem1 = self.loai_diem[0]
            self.diem5 = self.diem6 = self.diem4 = self.diem2 = self.diem3 = self.diem1
        if len(self.loai_diem) > 6:
            self.diem5 = self.diem6 = self.diem4 = self.diem2 = self.diem3 = self.diem1 = 0

    def GetDataFromRect(self, i):
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
        self.num1 = self.items[i][14]
        self.num2 = self.items[i][15]
        self.maxD = self.items[i][16]
        self.minD = self.items[i][17]
        self.angle = self.items[i][18]
        self.num3 = self.items[i][19]
        self.khoi = self.items[i][20]

    @pyqtSlot()
    def GetDataFromRectp(self, j):
        self.Pixitemp = self.itemp[j][13]
        self.itemRectp = self.itemp[j][0]
        self.xp = self.itemp[j][0].sceneBoundingRect().left() + 4
        self.yp = self.itemp[j][0].sceneBoundingRect().top() + 4
        self.widthp = self.itemp[j][0].sceneBoundingRect().width() - 8
        self.heightp = self.itemp[j][0].sceneBoundingRect().height() - 8
        self.maxvaluep = self.itemp[j][1]
        self.minvaluep = self.itemp[j][2]
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
        self.Area = self.ui.checkBox_Area.isChecked()
        self.Distance = self.ui.checkBox_Height.isChecked()
        self.Distancew = self.ui.checkBox_Width.isChecked()
        self.Number = self.ui.spinBox_Num.value()
        self.test_pin = self.ui.checkBox_10.isChecked()
        self.all_area = self.ui.checkBox_Nothing.isChecked()

    @pyqtSlot()
    def initiateRect(self, URLs, openF):
        listItems, listItemP, listcheckBox, listLoaidiem, URLfile = self.SandRFile.readFile2List(URLs, openF)
        self.dropdownBox(URLfile)
        self.delete_all()
        try:
            for i in listItems:
                rectItems = GraphicsRectItem(i[8], i[9], i[10], i[11])
                rectItems.setZValue(1)
                i.insert(0, rectItems)
                i.insert(13, None)
                self.items.append(i)
                self.scene.addItem(rectItems)
            for i in listItemP:
                rectItems = GraphicsRectItem(i[8], i[9], i[10], i[11])
                rectItems.setZValue(1)
                i.insert(0, rectItems)
                i.insert(13, None)
                self.itemp.append(i)
                self.scene.addItem(rectItems)
            if len(listcheckBox) == 6:
                self.Area = True if (listcheckBox[0] == 'True') else False
                self.Distance = True if (listcheckBox[1] == 'True') else False
                self.Distancew = True if (listcheckBox[2] == 'True') else False
                self.Number = float(listcheckBox[3])
                self.test_pin = True if (listcheckBox[4].replace("\n", "") == 'True') else False
                self.all_area = True if (listcheckBox[5].replace("\n", "") == 'True') else False
            else:
                self.Area = False
                self.Distance = False
                self.Distancew = False
                self.Number = 0
                self.test_pin = False
                self.all_area = False
            self.ui.checkBox_Area.setChecked(self.Area)
            self.ui.checkBox_Height.setChecked(self.Distance)
            self.ui.checkBox_Width.setChecked(self.Distancew)
            self.ui.spinBox_Num.setValue(self.Number)
            self.ui.checkBox_10.setChecked(self.test_pin)
            self.ui.checkBox_Nothing.setChecked(self.all_area)
        except:
            self.items = []
            self.itemp = []
            self.Area = False
            self.Distance = False
            self.Distancew = False
            self.Number = 0
            self.test_pin = False
            self.all_area = False
            self.ui.checkBox_Area.setChecked(self.Area)
            self.ui.checkBox_Height.setChecked(self.Distance)
            self.ui.checkBox_Width.setChecked(self.Distancew)
            self.ui.spinBox_Num.setValue(self.Number)
            self.ui.checkBox_10.setChecked(self.test_pin)
            self.ui.checkBox_Nothing.setChecked(self.all_area)

    def innitalProcessImage(self):
        for i in range(len(self.items)):
            self.GetDataFromRect(i)
            self.threadProcessImage(i, self.x, self.y, self.width, self.height)

    def innitalProcessImagep(self):
        for j in range(len(self.itemp)):
            self.GetDataFromRectp(j)
            self.threadProcessImagep(j, self.xp, self.yp, self.widthp, self.heightp)

    @pyqtSlot()
    def drawrect(self):
        self.value = GraphicsRectItem(0, 0, 50, 25)
        self.value.setZValue(2)
        self.Pixmapitem = QGraphicsPixmapItem()
        self.Pixmapitem.setZValue(1)
        self.items.append(
            [self.value, 0, 0, 0, 0, 0, 255, 255, 255, 0, 0, 100, 50, self.Pixmapitem, 0, 0, 0, 0, 0, 0, 0])
        self.scene.addItem(self.value)

    @pyqtSlot()
    def Position(self):
        if len(self.itemp) == 0:
            self.pst = GraphicsRectItem(0, 0, 30, 30)
            self.pst.setZValue(1)
            self.Pixmapitem = QGraphicsPixmapItem()
            self.Pixmapitem.setZValue(0)
            self.itemp.append([self.pst, 0, 0, 0, 0, 0, 255, 255, 255, 0, 0, 30, 30, self.Pixmapitem, 10, 10])
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
    def center_rect(self, index):
        cenrec_x = self.items[index][0].sceneBoundingRect().center().x()
        cenrec_y = self.items[index][0].sceneBoundingRect().center().y()
        return cenrec_x, cenrec_y

    def draw_circle_xanh(self, cenx, ceny):
        pen = QPen(QColor(Qt.blue))
        circle = QGraphicsEllipseItem(cenx, ceny, 8, 8)
        circle.setZValue(0)
        circle.setPen(pen)
        circle.moveBy(self.center_x, self.center_y)
        self.scene.addItem(circle)

    def draw_circle(self, cenx, ceny):
        pen = QPen(QColor(Qt.red))
        circle = QGraphicsEllipseItem(cenx, ceny, 5, 5)
        circle.setZValue(0)
        circle.setPen(pen)
        circle.moveBy(self.center_x, self.center_y)
        self.scene.addItem(circle)

    def xoay_rect(self, index):
        if self.angle != 0:
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

    def xoay_diem(self, centerx, centery, xr1, yr1, goc):
        newpx1 = xr1 - centerx
        newpy1 = yr1 - centery
        point_x1 = newpx1 * math.cos(math.radians(goc)) - newpy1 * math.sin(math.radians(goc))
        point_y1 = newpx1 * math.sin(math.radians(goc)) + newpy1 * math.cos(math.radians(goc))
        return point_x1, point_y1

    def loaidiem(self):
        self.Number = int(self.ui.spinBox_Num.value())
        if self.Number != 0 and self.Number <= 360:
            if self.Number not in self.loai_diem:
                self.loai_diem.append(self.Number)
        if self.Number == 0:
            self.loai_diem.clear()

    def showParameter(self):
        count = 0
        countp = 0
        self.scene.update()
        for i in range(len(self.items)):
            self.ui.spinBox_NumO.setEnabled(True)
            if self.items[i][0].isSelected() and self.ui.checkBox_Area.isChecked():
                self.ui.spinBox_Angle.setEnabled(True)
                self.ui.spinBox_Angle.setValue(self.items[i][18])
                self.ui.spinBox_MaxArea.setEnabled(True)
                self.ui.spinBox_MaxArea.setValue(self.items[i][1])
                self.ui.spinBox_MinArea.setEnabled(True)
                self.ui.spinBox_MinArea.setValue(self.items[i][2])
            if self.items[i][0].isSelected() and self.ui.checkBox_Height.isChecked():
                self.ui.spinBox_MaxArea.setEnabled(True)
                self.ui.spinBox_MaxArea.setValue(self.items[i][1])
                self.ui.spinBox_Nothing.setEnabled(True)
                self.ui.spinBox_Nothing.setValue(self.items[i][20])
                self.ui.spinBox_NumO.setEnabled(True)
                self.ui.spinBox_NumO.setValue(self.items[i][19])
                self.ui.spinBox_Angle.setEnabled(True)
                self.ui.spinBox_Angle.setValue(self.items[i][18])
                self.ui.spinBox_NumH.setEnabled(True)
                self.ui.spinBox_NumH.setValue(self.items[i][14])
                self.ui.spinBox_MaxDistance.setEnabled(True)
                self.ui.spinBox_MaxDistance.setValue(self.items[i][16])
                self.ui.spinBox_MinDistance.setEnabled(True)
                self.ui.spinBox_MinDistance.setValue(self.items[i][17])
            if self.items[i][0].isSelected() and self.ui.checkBox_Width.isChecked():
                self.ui.spinBox_NumO.setEnabled(True)
                self.ui.spinBox_NumO.setValue(self.items[i][19])
                self.ui.spinBox_Angle.setEnabled(True)
                self.ui.spinBox_Angle.setValue(self.items[i][18])
                self.ui.spinBox_NumW.setEnabled(True)
                self.ui.spinBox_NumW.setValue(self.items[i][15])
                self.ui.spinBox_MaxDistance.setEnabled(True)
                self.ui.spinBox_MaxDistance.setValue(self.items[i][16])
                self.ui.spinBox_MinDistance.setEnabled(True)
                self.ui.spinBox_MinDistance.setValue(self.items[i][17])
            if self.items[i][0].isSelected():
                count = 1
                self.ui.horizontalSlider_LH.setEnabled(True)
                self.ui.horizontalSlider_LH.blockSignals(True)
                self.ui.horizontalSlider_LH.setValue(self.items[i][3])
                self.ui.horizontalSlider_LH.blockSignals(False)
                self.ui.label_value_LH.setText(str(self.items[i][3]))
                self.ui.horizontalSlider_LS.setEnabled(True)
                self.ui.horizontalSlider_LS.blockSignals(True)
                self.ui.horizontalSlider_LS.setValue(self.items[i][4])
                self.ui.horizontalSlider_LS.blockSignals(False)
                self.ui.label_value_LS.setText(str(self.items[i][4]))
                self.ui.horizontalSlider_LV.setEnabled(True)
                self.ui.horizontalSlider_LV.blockSignals(True)
                self.ui.horizontalSlider_LV.setValue(self.items[i][5])
                self.ui.horizontalSlider_LV.blockSignals(False)
                self.ui.label_Value_LV.setText(str(self.items[i][5]))
                self.ui.horizontalSlider_UH.setEnabled(True)
                self.ui.horizontalSlider_UH.blockSignals(True)
                self.ui.horizontalSlider_UH.setValue(self.items[i][6])
                self.ui.horizontalSlider_UH.blockSignals(False)
                self.ui.label_Value_UH.setText(str(self.items[i][6]))
                self.ui.horizontalSlider_US.setEnabled(True)
                self.ui.horizontalSlider_US.blockSignals(True)
                self.ui.horizontalSlider_US.setValue(255)
                self.ui.horizontalSlider_US.blockSignals(False)
                self.ui.label_Value_US.setText(str(self.items[i][7]))
                self.ui.horizontalSlider_UV.setEnabled(True)
                self.ui.horizontalSlider_UV.blockSignals(True)
                self.ui.horizontalSlider_UV.setValue(self.items[i][8])
                self.ui.horizontalSlider_UV.blockSignals(False)
                self.ui.label_Value_UV.setText(str(self.items[i][8]))

                self.GetDataFromRect(i)
                self.threadProcessImage(i, self.x, self.y, self.width, self.height)
            if count == 0 and countp == 0:
                self.lockParameter()
        for j in range(0, len(self.itemp)):
            if self.itemp[j][0].isSelected():
                self.ui.horizontalSlider_LH.setEnabled(True)
                self.ui.horizontalSlider_LH.blockSignals(True)
                self.ui.horizontalSlider_LH.setValue(self.itemp[j][3])
                self.ui.horizontalSlider_LH.blockSignals(False)
                self.ui.label_value_LH.setText(str(self.itemp[j][3]))

                self.ui.horizontalSlider_LS.setEnabled(True)
                self.ui.horizontalSlider_LS.blockSignals(True)
                self.ui.horizontalSlider_LS.setValue(self.itemp[j][4])
                self.ui.horizontalSlider_LS.blockSignals(False)
                self.ui.label_value_LS.setText(str(self.itemp[j][4]))

                self.ui.horizontalSlider_LV.setEnabled(True)
                self.ui.horizontalSlider_LV.blockSignals(True)
                self.ui.horizontalSlider_LV.setValue(self.itemp[j][5])
                self.ui.horizontalSlider_LV.blockSignals(False)
                self.ui.label_Value_LV.setText(str(self.itemp[j][5]))

                self.ui.horizontalSlider_UH.setEnabled(True)
                self.ui.horizontalSlider_UH.blockSignals(True)
                self.ui.horizontalSlider_UH.setValue(self.itemp[j][6])
                self.ui.horizontalSlider_UH.blockSignals(False)
                self.ui.label_Value_UH.setText(str(self.itemp[j][6]))

                self.ui.horizontalSlider_US.setEnabled(True)
                self.ui.horizontalSlider_US.blockSignals(True)
                self.ui.horizontalSlider_US.setValue(self.itemp[j][7])
                self.ui.horizontalSlider_US.blockSignals(False)
                self.ui.label_Value_US.setText(str(self.itemp[j][7]))

                self.ui.horizontalSlider_UV.setEnabled(True)
                self.ui.horizontalSlider_UV.blockSignals(True)
                self.ui.horizontalSlider_UV.setValue(self.itemp[j][8])
                self.ui.horizontalSlider_UV.blockSignals(False)
                self.ui.label_Value_UV.setText(str(self.itemp[j][8]))
                self.GetDataFromRectp(j)
                self.threadProcessImagep(j, self.xp, self.yp, self.widthp, self.heightp)
                countp = 1

            if countp == 0 and count == 0:
                self.lockParameter()

    @pyqtSlot()
    def lockParameter(self):
        self.ui.spinBox_Nothing.setEnabled(False)
        self.ui.spinBox_NumO.setEnabled(False)
        self.ui.spinBox_Angle.setEnabled(False)
        self.ui.spinBox_MaxArea.setEnabled(False)
        self.ui.spinBox_MinArea.setEnabled(False)
        self.ui.spinBox_NumH.setEnabled(False)
        self.ui.spinBox_NumW.setEnabled(False)
        self.ui.spinBox_Nothing.setEnabled(False)
        self.ui.spinBox_MaxDistance.setEnabled(False)
        self.ui.spinBox_MinDistance.setEnabled(False)
        self.ui.horizontalSlider_LH.setEnabled(False)
        self.ui.horizontalSlider_LS.setEnabled(False)
        self.ui.horizontalSlider_LV.setEnabled(False)
        self.ui.horizontalSlider_UH.setEnabled(False)
        self.ui.horizontalSlider_US.setEnabled(False)
        self.ui.horizontalSlider_UV.setEnabled(False)

    @pyqtSlot()
    def UpdateDataOnList(self):
        try:
            # self.Number = self.ui.spinBox_NumO.value()
            for i in range(len(self.items)):
                if self.items[i][0].isSelected():
                    self.GetDataFromRect(i)
                    self.maxvalue = self.ui.spinBox_MaxArea.value()
                    self.minvalue = self.ui.spinBox_MinArea.value()
                    self.slidevalue_LH = self.ui.horizontalSlider_LH.value()
                    self.slidevalue_LS = self.ui.horizontalSlider_LS.value()
                    self.slidevalue_LV = self.ui.horizontalSlider_LV.value()
                    self.slidevalue_UH = self.ui.horizontalSlider_UH.value()
                    self.slidevalue_US = self.ui.horizontalSlider_US.value()
                    self.slidevalue_UV = self.ui.horizontalSlider_UV.value()
                    self.ui.label_value_LH.setText(str(self.slidevalue_LH))
                    self.ui.label_value_LS.setText(str(self.slidevalue_LS))
                    self.ui.label_Value_LV.setText(str(self.slidevalue_LV))
                    self.ui.label_Value_UH.setText(str(self.slidevalue_UH))
                    self.ui.label_Value_US.setText(str(self.slidevalue_US))
                    self.ui.label_Value_UV.setText(str(self.slidevalue_UV))
                    self.num1 = self.ui.spinBox_NumH.value()
                    self.num2 = self.ui.spinBox_NumW.value()
                    self.maxD = self.ui.spinBox_MaxDistance.value()
                    self.minD = self.ui.spinBox_MinDistance.value()
                    self.angle = self.ui.spinBox_Angle.value()
                    self.num3 = self.ui.spinBox_NumO.value()
                    self.khoi = self.ui.spinBox_Nothing.value()
                    self.items[i] = [self.items[i][0], self.maxvalue, self.minvalue, self.slidevalue_LH,
                                     self.slidevalue_LS, self.slidevalue_LV, self.slidevalue_UH, self.slidevalue_US,
                                     self.slidevalue_UV, self.x, self.y, self.width, self.height, self.Pixitem,
                                     self.num1, self.num2, self.maxD, self.minD, self.angle, self.num3, self.khoi]
                    self.threadProcessImage(i, self.x, self.y, self.width, self.height)
            for j in range(len(self.itemp)):
                if self.itemp[j][0].isSelected():
                    self.GetDataFromRectp(j)
                    maxvaluep = self.ui.spinBox_MaxArea.value()
                    minvaluep = self.ui.spinBox_MinArea.value()
                    slidevalue_LHp = self.ui.horizontalSlider_LH.value()
                    slidevalue_LSp = self.ui.horizontalSlider_LS.value()
                    slidevalue_LVp = self.ui.horizontalSlider_LV.value()
                    slidevalue_UHp = self.ui.horizontalSlider_UH.value()
                    slidevalue_USp = self.ui.horizontalSlider_US.value()
                    slidevalue_UVp = self.ui.horizontalSlider_UV.value()
                    self.ui.label_value_LH.setText(str(slidevalue_LHp))
                    self.ui.label_value_LS.setText(str(slidevalue_LSp))
                    self.ui.label_Value_LV.setText(str(slidevalue_LVp))
                    self.ui.label_Value_UH.setText(str(slidevalue_UHp))
                    self.ui.label_Value_US.setText(str(slidevalue_USp))
                    self.ui.label_Value_UV.setText(str(slidevalue_UVp))
                    self.itemp[j] = (
                        self.itemp[j][0], maxvaluep, minvaluep, slidevalue_LHp, slidevalue_LSp, slidevalue_LVp,
                        slidevalue_UHp, slidevalue_USp, slidevalue_UVp, self.xp, self.yp, self.widthp, self.heightp,
                        self.Pixitemp, self.center_x, self.center_y)
                    self.threadProcessImagep(j, self.xp, self.yp, self.widthp, self.heightp)
        except:
            pass

    @pyqtSlot()
    def threadProcessImage(self, index, x, y, width, height):
        try:
            if self.imageoutside:
                self.imageforprocess2 = self.imageopen1
            else:
                self.imageforprocess2 = self.frame
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            if x + width > 640:
                x = 640 - width
            if y + height > 480:
                y = 480 - height
            self.ProcessImage(self.imageforprocess2, index, x, y, width, height)
            self.CovertoPixmap(self.res, x, y)
            self.CreateListPixmapIterm(self.pixm, index, x, y)
        except:
            pass

    def threadProcessImagep(self, index, x, y, width, height):
        if self.imageoutside:
            self.imageforprocess2 = self.imageopen1
        else:
            self.imageforprocess2 = self.frame
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x + width > 640:
            x = 640 - width
        if y + height > 480:
            y = 480 - height
        self.ProcessImagep(self.imageforprocess2, index, x, y, width, height)
        self.CovertoPixmap(self.resp, x, y)
        self.CreateListPixmapItermp(self.pixm, index, x, y)
        self.chinh_hinh()

    @pyqtSlot()
    def ProcessImage(self, orginalImage, index, x, y, width, height):
        try:
            if len(self.items) != 0:
                imgx, imgy, im = orginalImage.shape
                center = (self.center_x, self.center_y)
                scale = 1
                self.GetDataFromRect(index)
                M = cv2.getRotationMatrix2D(center, self.goc, scale)
                orginalImage = cv2.warpAffine(orginalImage, M, (imgy, imgx))
                crop_image = orginalImage[int(y):int(y + height), int(x):int(x + width)]
                # crop_image = cv2.GaussianBlur(crop_image, (5, 5), 0)
                self.HsvColor = cv2.cvtColor(crop_image, cv2.COLOR_BGR2HSV)
                L_b = np.array([self.slidevalue_LH, self.slidevalue_LS, self.slidevalue_LV])
                U_b = np.array([self.slidevalue_UH, self.slidevalue_US, self.slidevalue_UV])
                self.mask = cv2.inRange(self.HsvColor, L_b, U_b)
                self.res = cv2.bitwise_and(crop_image, crop_image, mask=self.mask)
        except:
            pass

    def ProcessImagep(self, orginalImage, index, x, y, width, height):
        try:
            if len(self.itemp) != 0:
                self.GetDataFromRectp(index)
                crop_image = orginalImage[int(y):int(y + height), int(x):int(x + width)]
                self.HsvColorp = cv2.cvtColor(crop_image, cv2.COLOR_BGR2HSV)
                L_bp = np.array([self.slidevalue_LHp, self.slidevalue_LSp, self.slidevalue_LVp])
                U_bp = np.array([self.slidevalue_UHp, self.slidevalue_USp, self.slidevalue_UVp])
                self.maskp = cv2.inRange(self.HsvColorp, L_bp, U_bp)
                self.resp = cv2.bitwise_and(crop_image, crop_image, mask=self.maskp)
        except:
            pass

    def CovertoPixmap(self, image, x, y):
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if (image.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_BGR888
        img = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        img = img.rgbSwapped()
        self.pixm = QtGui.QPixmap.fromImage(img)

    def CreateListPixmapIterm(self, pix, index, x, y):
        self.scene.removeItem(self.items[index][13])
        self.pixmapiterm = QGraphicsPixmapItem(pix)
        self.pixmapiterm.setPos(x, y)
        self.pixmapiterm.setZValue(0)
        self.scene.addItem(self.pixmapiterm)
        self.GetDataFromRect(index)
        self.items[index] = [self.itemRect, self.maxvalue, self.minvalue, self.slidevalue_LH,
                             self.slidevalue_LS, self.slidevalue_LV, self.slidevalue_UH,
                             self.slidevalue_US, self.slidevalue_UV, self.x, self.y, self.width, self.height,
                             self.pixmapiterm, self.num1, self.num2, self.maxD, self.minD, self.angle, self.num3,
                             self.khoi]

    def CreateListPixmapItermp(self, pix, index, x, y):
        self.scene.removeItem(self.itemp[index][13])
        self.pixmapitermp = QGraphicsPixmapItem(pix)
        self.pixmapitermp.setPos(x, y)
        self.pixmapitermp.setZValue(0)
        self.scene.addItem(self.pixmapitermp)
        self.GetDataFromRectp(index)
        self.itemp[index] = [self.itemRectp, self.maxvaluep, self.minvaluep, self.slidevalue_LHp,
                             self.slidevalue_LSp, self.slidevalue_LVp, self.slidevalue_UHp,
                             self.slidevalue_USp, self.slidevalue_UVp, self.xp, self.yp,
                             self.widthp, self.heightp, self.pixmapitermp, self.center_x, self.center_y]

    def openImage(self):
        fileChoosen = QFileDialog.getOpenFileName(self, 'Open Files', 'D:\\', "Image Files (*.jpg *.png *.bmp)")
        if fileChoosen[0] != '':
            self.imagepath = fileChoosen[0]
            self.image = QPixmap(self.imagepath).scaled(640, 480)
            self.scene.addPixmap(self.image)
            self.imageopen1 = cv2.imread(fileChoosen[0])
            self.imageopen1 = cv2.resize(src=self.imageopen1, dsize=(640, 480))
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
        self.show_center()
        if len(self.items) == 0:
            self.ui.label_Result.setText("NG")
            self.ui.label_notify.setText("No Items")
            return False
        elif self.ui.checkBox_Area.isChecked() and not self.ui.checkBox_Height.isChecked() \
                and not self.ui.checkBox_Width.isChecked():
            test = self.result_area()
            if test:
                return True
            else:
                False
        elif not self.ui.checkBox_Area.isChecked() and self.ui.checkBox_Height.isChecked() \
                and not self.ui.checkBox_Width.isChecked():
            test = self.result_height()
            if test:
                return self.mang_xuat, True, self.xuat_kq
            elif not test:
                return self.mang_xuat, False, self.xuat_kq
        elif not self.ui.checkBox_Area.isChecked() and not self.ui.checkBox_Height.isChecked() \
                and self.ui.checkBox_Width.isChecked():
            test = self.result_width()
            if test:
                return True
            else:
                False
        elif self.ui.checkBox_Area.isChecked() and self.ui.checkBox_Height.isChecked() \
                and not self.ui.checkBox_Width.isChecked():
            test = self.result_area_height()
            if test:
                return True
            else:
                False
        elif self.ui.checkBox_Area.isChecked() and not self.ui.checkBox_Height.isChecked() \
                and self.ui.checkBox_Width.isChecked():
            test = self.result_area_width()
            if test:
                return True
            else:
                False
        elif not self.ui.checkBox_Area.isChecked() and self.ui.checkBox_Height.isChecked() \
                and self.ui.checkBox_Width.isChecked():
            test = self.result_height_width()
            if test:
                return True
            else:
                False
        elif self.ui.checkBox_Area.isChecked() and self.ui.checkBox_Height.isChecked() \
                and self.ui.checkBox_Width.isChecked():
            test = self.result_area_height_width()
            if test:
                return True
            else:
                False
        elif not self.ui.checkBox_Area.isChecked() and not self.ui.checkBox_Height.isChecked() \
                and not self.ui.checkBox_Width.isChecked():
            self.ui.label_Result.setText("Please selection type test!")
            self.ui.label_notify.setText("No result")

    def chenh_lech(self):
        dem_lech = 0
        limit_lech = self.items[0][19]
        min_lech = min(self.mang_xuat)
        if self.ui.checkBox_10.isChecked():
            for i in self.mang_xuat:
                lech_chan = i - min_lech
                if lech_chan > limit_lech:
                    dem_lech += 1
            return dem_lech

    def noidiem(self):
        for i in range(len(self.items) - 1):
            noidiem1, noidiem2 = self.items[i][0].sceneBoundingRect().left() + 4, \
                                 self.items[i][0].sceneBoundingRect().top() + 4
            noidiem3, noidiem4 = self.items[i + 1][0].sceneBoundingRect().left() + 4, \
                                 self.items[i + 1][0].sceneBoundingRect().top() + 4
            noidiem5, noidiem6 = self.items[i][0].sceneBoundingRect().right() - 4, \
                                 self.items[i][0].sceneBoundingRect().bottom() - 4
            noidiem7, noidiem8 = self.items[i + 1][0].sceneBoundingRect().right() - 4, \
                                 self.items[i + 1][0].sceneBoundingRect().bottom() - 4
            self.pen = QPen(QColor(Qt.red))
            self.line1 = QGraphicsLineItem(noidiem1, noidiem2, noidiem3, noidiem4)
            self.line1.setZValue(2)
            self.line1.setPen(self.pen)
            self.scene.addItem(self.line1)
            self.line2 = QGraphicsLineItem(noidiem5, noidiem6, noidiem7, noidiem8)
            self.line2.setZValue(2)
            self.line2.setPen(self.pen)
            self.scene.addItem(self.line2)

    def result_area(self):
        gettotalResult = 0
        for i in range(len(self.items)):
            if self.items[i][0].isSelected():
                cal = self.arer_xoay_only(i)
                if cal:
                    self.ui.label_notify.setText("OK One")
                    text = "Min_area/Max_area: %d / %d" % (self.min_are, self.max_are)
                    self.ui.label_Result.setText(text)
                    return True
                else:
                    self.ui.label_notify.setText("NG One")
                    text = "Min_area/Max_area: %d / %d" % (self.min_are, self.max_are)
                    self.ui.label_Result.setText(text)
                    return False
        for i in range(len(self.items)):
            cal = self.arer_xoay_only(i)
            if cal:
                gettotalResult += 1
        if gettotalResult == len(self.items):
            text = "OK Total: %d / %d" % (gettotalResult, len(self.items))
            self.ui.label_Result.setText(text)
            self.ui.label_notify.setText("All OK")
            return True
        else:
            text = "NG Total: %d / %d" % (gettotalResult, len(self.items))
            self.ui.label_Result.setText(text)
            self.ui.label_notify.setText("All NG")
            return False

    def result_height(self):

        gettotalResult = 0
        self.mang_xuat = []
        for i in range(len(self.items)):
            if self.items[i][0].isSelected():
                cal = self.Dis_height(i)
                if cal:
                    self.ui.label_Result.setText("OK One")
                    max_min = "Min_H/Max_H: %.2f / %.2f" % (self.min_height_xoay, self.max_height_xoay)
                    self.ui.label_notify.setText(max_min)
                    label_Pin = "%.2f" % (self.min_height_xoay)
                    if i == 0:
                        self.ui.label_Pin1.setText(label_Pin)
                    if i == 1:
                        self.ui.label_Pin2.setText(label_Pin)
                    if i == 2:
                        self.ui.label_Pin3.setText(label_Pin)
                    if i == 3:
                        self.ui.label_Pin4.setText(label_Pin)
                    if i == 4:
                        self.ui.label_Pin5.setText(label_Pin)
                    if i == 5:
                        self.ui.label_Pin6.setText(label_Pin)
                    return True
                else:
                    self.ui.label_Result.setText("NG One")
                    max_min = "Min_H/Max_H: %.2f / %.2f" % (self.min_height_xoay, self.max_height_xoay)
                    self.ui.label_notify.setText(max_min)
                    label_Pin = "%.2f" % (self.min_height_xoay)
                    if i == 0:
                        self.ui.label_Pin1.setText(label_Pin)
                    if i == 1:
                        self.ui.label_Pin2.setText(label_Pin)
                    if i == 2:
                        self.ui.label_Pin3.setText(label_Pin)
                    if i == 3:
                        self.ui.label_Pin4.setText(label_Pin)
                    if i == 4:
                        self.ui.label_Pin5.setText(label_Pin)
                    if i == 5:
                        self.ui.label_Pin6.setText(label_Pin)
                    return False
        for i in range(len(self.items)):
            cal = self.Dis_height(i)
            if i == 0:
                text1 = "%.2f" % (self.min_height_xoay)
                self.ui.label_Pin1.setText(text1)
                self.mang_xuat.append(self.min_height_xoay)
            if i == 1:
                text2 = "%.2f" % (self.min_height_xoay)
                self.ui.label_Pin2.setText(text2)
                self.mang_xuat.append(self.min_height_xoay)
            if i == 2:
                text3 = "%.2f" % (self.min_height_xoay)
                self.ui.label_Pin3.setText(text3)
                self.mang_xuat.append(self.min_height_xoay)
            if i == 3:
                text4 = "%.2f" % (self.min_height_xoay)
                self.ui.label_Pin4.setText(text4)
                self.mang_xuat.append(self.min_height_xoay)
            if i == 4:
                text5 = "%.2f" % (self.min_height_xoay)
                self.ui.label_Pin5.setText(text5)
                self.mang_xuat.append(self.min_height_xoay)
            if i == 5:
                text6 = "%.2f" % (self.min_height_xoay)
                self.ui.label_Pin6.setText(text6)
                self.mang_xuat.append(self.min_height_xoay)
            if cal:
                gettotalResult += 1
        if self.ui.checkBox_10.isChecked():
            test_lech = self.chenh_lech()
        else:
            test_lech = 1
        if gettotalResult == len(self.items) or test_lech == 0:
            text = "OK Total: %.2f/ %.2f" % (gettotalResult, len(self.items))
            self.ui.label_Result.setText(text)
            self.ui.label_notify.setText("All OK")
            return True
        elif gettotalResult != len(self.items):
            text = "NG Total: %.2f / %.2f" % (gettotalResult, len(self.items))
            self.ui.label_Result.setText(text)
            self.ui.label_notify.setText("All NG")
            return False

    def result_width(self):
        gettotalResult = 0
        for i in range(len(self.items)):
            if self.items[i][0].isSelected():
                width = self.Dis_width(i)
                if width:
                    self.ui.label_Result.setText("OK One")
                    max_min = "Min_W/Max_W: %f / %f" % (self.min_width_xoay, self.max_width_xoay)
                    self.ui.label_notify.setText(max_min)
                    return True
                else:
                    self.ui.label_Result.setText("NG One")
                    max_min = "Min_W/Max_W: %f / %f" % (self.min_width_xoay, self.max_width_xoay)
                    self.ui.label_notify.setText(max_min)
                    return False
        for i in range(len(self.items)):
            cal = self.Dis_width(i)
            if cal:
                gettotalResult += 1
        if gettotalResult == len(self.items):
            text = "OK Total: %f / %f" % (gettotalResult, len(self.items))
            self.ui.label_Result.setText(text)
            self.ui.label_notify.setText("All OK")
            return True
        else:
            text = "NG Total: %f / %f" % (gettotalResult, len(self.items))
            self.ui.label_Result.setText(text)
            self.ui.label_notify.setText("All NG")
            return False

    def result_area_height(self):
        gettotalResult = 0
        for i in range(len(self.items)):
            if self.items[i][0].isSelected():
                cal = self.arer_xoay_only(i)
                hight = self.Dis_height(i)
                if cal and hight:
                    self.ui.label_Result.setText("OK One")
                    self.ui.label_notify.setText("S_H OK")
                    return True
                else:
                    self.ui.label_Result.setText("NG One")
                    self.ui.label_notify.setText("S_H NG")
                    return False
        for i in range(len(self.items)):
            cal = self.arer_xoay_only(i)
            hight = self.Dis_height(i)
            if cal and hight:
                gettotalResult += 1
        if gettotalResult == len(self.items):
            text = "OK Total: %d / %d" % (gettotalResult, len(self.items))
            self.ui.label_Result.setText(text)
            self.ui.label_notify.setText("All S_H OK")
            return True
        else:
            text = "NG Total: %d / %d" % (gettotalResult, len(self.items))
            self.ui.label_Result.setText(text)
            self.ui.label_notify.setText("All S_H NG")
            return False

    def result_area_width(self):
        gettotalResult = 0
        for i in range(len(self.items)):
            if self.items[i][0].isSelected():
                cal = self.arer_xoay_only(i)
                width = self.Dis_width(i)
                if cal and width:
                    self.ui.label_Result.setText("OK One")
                    self.ui.label_notify.setText("S_W OK")
                    return True
                else:
                    self.ui.label_Result.setText("NG One")
                    self.ui.label_notify.setText("S_W NG")
                    return False

        for i in range(len(self.items)):
            cal = self.arer_xoay_only(i)
            width = self.Dis_width(i)
            if cal and width:
                gettotalResult += 1

        if gettotalResult == len(self.items):
            text = "OK Total: %d / %d" % (gettotalResult, len(self.items))
            self.ui.label_Result.setText(text)
            self.ui.label_notify.setText("All S_W OK")
            return True
        else:
            text = "NG Total: %d / %d" % (gettotalResult, len(self.items))
            self.ui.label_Result.setText(text)
            self.ui.label_notify.setText("All S_W NG")
            return False

    def result_height_width(self):
        gettotalResult = 0
        for i in range(len(self.items)):
            if self.items[i][0].isSelected():
                width = self.Dis_width(i)
                hight = self.Dis_height(i)
                if width and hight:
                    self.ui.label_Result.setText("OK One")
                    self.ui.label_notify.setText("H_W OK")
                    return True
                else:
                    self.ui.label_Result.setText("NG One")
                    self.ui.label_notify.setText("H_W NG")
                    return False
        for i in range(len(self.items)):
            width = self.Dis_width(i)
            hight = self.Dis_height(i)
            if width and hight:
                gettotalResult += 1
        if gettotalResult == len(self.items):
            text = "OK Total: %d / %d" % (gettotalResult, len(self.items))
            self.ui.label_Result.setText(text)
            self.ui.label_notify.setText("All H_W OK")
            return True
        else:
            text = "NG Total: %d / %d" % (gettotalResult, len(self.items))
            self.ui.label_Result.setText(text)
            self.ui.label_notify.setText("All H_W NG")
            return False

    def result_area_height_width(self):
        gettotalResult = 0
        for i in range(len(self.items)):
            if self.items[i][0].isSelected():
                cal = self.arer_xoay_only(i)
                hight = self.Dis_height(i)
                width = self.Dis_width(i)
                if cal and hight and width:
                    self.ui.label_Result.setText("OK One")
                    self.ui.label_notify.setText("S_H_W OK")
                    return True
                else:
                    self.ui.label_Result.setText("NG One")
                    self.ui.label_notify.setText("S_H_W NG")
                    return False
        for i in range(len(self.items)):
            cal = self.arer_xoay_only(i)
            hight = self.Dis_height(i)
            width = self.Dis_width(i)
            if cal and hight and width:
                gettotalResult += 1
        if gettotalResult == len(self.items):
            text = "OK Total: %d / %d" % (gettotalResult, len(self.items))
            self.ui.label_Result.setText(text)
            self.ui.label_notify.setText("All OK")
            return True
        else:
            text = "NG Total: %d / %d" % (gettotalResult, len(self.items))
            self.ui.label_Result.setText(text)
            self.ui.label_notify.setText("All NG")
            return False

    def tinh_goc(self, index):
        # self.GetDataFromRect(index)
        if self.items[index][18] != 0:
            dem_goc = int(360 / self.items[index][18])
            return dem_goc

    def arer_xoay_only(self, index):
        self.Number = self.ui.spinBox_Num.value()
        test_NG = 0
        mang_are = []
        self.goc = 0
        if self.angle == 0:
            dem_goc = 0
        else:
            dem_goc = self.tinh_goc(index)
        self.loaidiem()
        if self.angle != 0 and len(self.itemp) != 0:
            for i in range(0, dem_goc):
                self.xoay_rect(index)
                if i not in self.loai_diem:
                    area_only = self.are_xoay(index)
                    mang_are.append(area_only)
                    if self.minvalue > area_only or area_only > self.maxvalue:
                        cenx, ceny = self.center_rect(index)
                        cenx_xoay, ceny_xoay = self.xoay_diem(self.center_x, self.center_y, cenx, ceny, self.goc)
                        self.draw_circle(cenx_xoay, ceny_xoay)
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
        elif self.angle == 0:
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
        self.ti_le = self.ui.spinBox_Num.value()
        mang_x = []
        height_x = []
        height_xm = []
        mang_Dish = []
        self.dem_khoi = 0
        if self.imageoutside:
            self.imageforprocess2 = self.imageopen1
        else:
            self.imageforprocess2 = self.frame
        self.GetDataFromRect(index)
        self.ProcessImage(self.imageforprocess2, index, self.x, self.y, self.width, self.height)
        contours, hierarchy = cv2.findContours(self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) == 0 or len(hierarchy) == 0 or self.num1 == 0:
            self.max_height_xoay_only = self.min_height_xoay_only = 0
            if self.minD <= self.max_height_xoay_only <= self.maxD:
                return True
            else:
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
                pointx_line1, pointx_line2 = height_xm[i7][0][0][0] + self.x, height_xm[i7][0][0][1] + self.y
                pointy_line1, pointy_line2 = height_xm[i7][1][0][0] + self.x, height_xm[i7][1][0][1] + self.y
                pointx1, pointx2, pointy1, pointy2 = self.xoay_line(pointx_line1, pointx_line2, pointy_line1,
                                                                    pointy_line2)
                self.line = QGraphicsLineItem(pointx1, pointx2, pointy1, pointy2)
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
                if self.Distance_h1 != 0:
                    mang_Dish.append(self.Distance_h1)
            if len(mang_Dish) != 0:
                if self.ti_le == 0:
                    self.max_height_xoay_only = max(mang_Dish)
                    self.min_height_xoay_only = min(mang_Dish)
                else:
                    self.max_height_xoay_only = max(mang_Dish) * self.ti_le
                    self.min_height_xoay_only = min(mang_Dish) * self.ti_le
                    self.max_height_xoay_only = round(self.max_height_xoay_only, 2)
                    self.min_height_xoay_only = round(self.min_height_xoay_only, 2)
            else:
                self.max_height_xoay_only = self.min_height_xoay_only = 0
            if len(contours) >= 2:
                for i in range(len(contours)):
                    area = cv2.contourArea(contours[i])
                    if area >= self.maxvalue:
                        self.dem_khoi += 1
            if self.minD <= self.min_height_xoay_only <= self.maxD or self.dem_khoi >= self.khoi:

                return True
            else:
                return False

    def mang_width_only(self, index):
        mang_y = []
        width_y = []
        width_ym = []
        mang_Dish = []
        if self.imageoutside:
            self.imageforprocess2 = self.imageopen1
        else:
            self.imageforprocess2 = self.frame
        self.GetDataFromRect(index)
        self.ProcessImage(self.imageforprocess2, index, self.x, self.y, self.width, self.height)
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

    def are_xoay(self, index):
        area = 0
        if self.imageoutside:
            self.imageforprocess2 = self.imageopen1
        else:
            self.imageforprocess2 = self.frame
        self.GetDataFromRect(index)
        self.ProcessImage(self.imageforprocess2, index, self.x, self.y, self.width, self.height)
        gray = cv2.cvtColor(self.res, cv2.COLOR_BGR2GRAY)
        contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0 or len(hierarchy) == 0:
            self.ui.label_notify.setText("Area is None")
            area = 0
            return area
        for i in range(len(contours)):
            area = cv2.contourArea(contours[i]) / 100 + area
        return area

    def center_are(self, mask):
        try:
            if self.imageoutside:
                self.imageforprocess2 = self.imageopen1
            else:
                self.imageforprocess2 = self.frame
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) == 0 or len(hierarchy) == 0:
                self.ui.label_notify.setText("Area is Null")
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
            self.center_x = self.cx + self.xp
            self.center_y = self.cy + self.yp
        except:
            pass

    def chinh_hinh(self):
        self.center_position()
        if len(self.itemp) == 0:
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

    def Dis_height(self, index):
        mang_max_height_xoay = []
        mang_min_height_xoay = []
        test_NG = 0
        self.goc = 0
        self.GetDataFromRect(index)
        if self.angle == 0:
            dem_goc = 1
        else:
            dem_goc = self.tinh_goc(index)
        if self.num1 != 0:
            for i in range(0, dem_goc):
                self.xoay_rect(index)
                test_height_xoay = self.mang_height_only(index)
                mang_max_height_xoay.append(self.max_height_xoay_only)
                mang_min_height_xoay.append(self.min_height_xoay_only)
                if test_height_xoay == False:
                    test_NG += 1
                    cenx, ceny = self.center_rect(index)
                    cenx_xoay, ceny_xoay = self.xoay_diem(self.center_x, self.center_y, cenx, ceny, self.goc)
                    self.draw_circle(cenx_xoay, ceny_xoay)
                self.goc += self.angle
            self.max_height_xoay = max(mang_max_height_xoay)
            if self.dem_khoi < self.khoi:
                self.min_height_xoay = min(mang_min_height_xoay)
            else:
                self.min_height_xoay = 0
            if test_NG == 0:
                self.xuat_so.append(self.min_height_xoay)
                self.xuat_kq.append("OK")
                return True
            else:
                self.xuat_so.append(self.min_height_xoay)
                self.xuat_kq.append("NG")
                return False
        else:
            self.max_height_xoay = self.min_height_xoay = 0
            return False

    def Dis_width(self, index):
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
                j = j + 1
        if j == 0:
            self.img = self.scene.addPixmap(QPixmap(self.image))
            self.img.setZValue(0)

    def Rectchild(self, valx, valy):
        self.chon_hcnx.clear()
        self.chon_hcny.clear()
        for i in range(len(self.items)):
            self.xt_gan = abs(self.items[i][0].sceneBoundingRect().left() - valx + 4)
            self.xp_gan = abs(self.items[i][0].sceneBoundingRect().right() - valx - 4)
            self.yt_gan = abs(self.items[i][0].sceneBoundingRect().top() - valy + 4)
            self.yp_gan = abs(self.items[i][0].sceneBoundingRect().bottom() - valy - 4)
            if self.xt_gan >= self.xp_gan:
                self.chon_hcnx.append(self.xp_gan)
            elif self.xt_gan < self.xp_gan:
                self.chon_hcnx.append(self.xt_gan)
            if self.yt_gan >= self.yp_gan:
                self.chon_hcny.append(self.yp_gan)
            elif self.yt_gan < self.yp_gan:
                self.chon_hcny.append(self.yt_gan)
        if len(self.itemp) != 0:
            self.xt_ganp = abs(self.itemp[0][0].sceneBoundingRect().left() - valx + 4)
            self.xp_ganp = abs(self.itemp[0][0].sceneBoundingRect().right() - valx - 4)
        if len(self.chon_hcnx) != 0 and len(self.itemp) != 0:
            min_hcn = min(self.chon_hcnx)
            for i in range(len(self.chon_hcnx)):
                if min_hcn != self.chon_hcnx[i]:
                    self.items[i][0].setFlag(QGraphicsItem.ItemIsSelectable, False)
                    self.items[i][0].setFlag(QGraphicsItem.ItemIsMovable, False)
                elif min_hcn == self.chon_hcnx[i] and min_hcn < self.xt_ganp and min_hcn < self.xp_ganp:
                    self.items[i][0].setFlag(QGraphicsItem.ItemIsSelectable, True)
                    self.items[i][0].setFlag(QGraphicsItem.ItemIsMovable, True)
                    self.itemp[0][0].setFlag(QGraphicsItem.ItemIsSelectable, False)
                    self.itemp[0][0].setFlag(QGraphicsItem.ItemIsMovable, False)
                elif min_hcn == self.chon_hcnx[i] and min_hcn >= self.xt_ganp or min_hcn >= self.xp_ganp:
                    self.itemp[0][0].setFlag(QGraphicsItem.ItemIsSelectable, True)
                    self.itemp[0][0].setFlag(QGraphicsItem.ItemIsMovable, True)
                    self.items[i][0].setFlag(QGraphicsItem.ItemIsSelectable, False)
                    self.items[i][0].setFlag(QGraphicsItem.ItemIsMovable, False)
        elif len(self.chon_hcnx) != 0 or len(self.chon_hcny) != 0:
            if len(self.itemp) == 0:
                min_hcnx = min(self.chon_hcnx)
                min_hcny = min(self.chon_hcny)
                j = 0
                for i in range(len(self.items)):
                    if self.items[i][0].sceneBoundingRect().left() + 4 < valx < self.items[i][
                        0].sceneBoundingRect().right() - 4:
                        if self.items[i][0].sceneBoundingRect().top() + 4 < valy < self.items[i][
                            0].sceneBoundingRect().bottom() - 4:
                            j = j + 1
                            if min_hcnx != self.chon_hcnx[i] and min_hcny != self.chon_hcny[i]:
                                self.items[i][0].setFlag(QGraphicsItem.ItemIsSelectable, False)
                                self.items[i][0].setFlag(QGraphicsItem.ItemIsMovable, False)
                            elif min_hcnx == self.chon_hcnx[i] or min_hcny == self.chon_hcny[i]:
                                self.items[i][0].setFlag(QGraphicsItem.ItemIsSelectable, True)
                                self.items[i][0].setFlag(QGraphicsItem.ItemIsMovable, True)


class QGraphicsView(QGraphicsView):
    clickItems = pyqtSignal(int, int)
    moveItems = pyqtSignal(int, int)

    def __init__(self, *args):
        super().__init__(*args)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        valx = event.pos().x()
        valy = event.pos().y()
        self.clickItems.emit(valx, valy)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if event.buttons() == QtCore.Qt.LeftButton:
            valx = event.pos().x()
            valy = event.pos().y()
            self.moveItems.emit(valx, valy)


class QGraphicsScene(QGraphicsScene):
    entered = pyqtSignal()

    def __init__(self, *args):
        super().__init__(*args)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    image = QPixmap("luc_giac.jpg").scaled(640, 480)
    frame = cv2.imread("luc_giac.jpg")
    frame = cv2.resize(src=frame, dsize=(640, 480))
    ui = Setting_Windown(MainWindow, image, frame)
    MainWindow.show()
    sys.exit(app.exec_())

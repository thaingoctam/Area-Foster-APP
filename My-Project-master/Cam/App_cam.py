from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *
from cam import *
import cv2
import sys
from os.path import expanduser

import serial
import threading
import time
import serial.tools.list_ports


class MyForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.timer = QtCore.QTimer()
        self.workThread = WorkThread()
        self.isCapturing = False

        self.workThread.trigger.connect(self.capture)
        self.ui.Start_btt.clicked.connect(self.startCapture)
        self.ui.Exits_btt.clicked.connect(self.endCapture)
        self.ui.Capture_btt.clicked.connect(self.work)
        self.ui.toolButton.clicked.connect(self.Folderchoose)
        self.ui.Stop_btt.clicked.connect(self.stop)
        self.ui.actionExits.triggered.connect(self.deleteLater)
        self.show()

    def startCapture(self):
        self.isCapturing = True
        self.fps = 24
        self.cap = cv2.VideoCapture(0)

        # ------ Modification ------ #
        self.ith_frame = 1
        # ------ Modification ------ #

            # self.capture.setFPS(1)
        self.start()
        self.show()
    def endCapture(self):
        self.deleteLater()
        self.capture = None
    def saveCapture(self):
        self.capture()

    def setFPS(self, fps):
        self.fps = fps

    def nextFrameSlot(self):
        ret, self.frame= self.cap.read()

        # My webcam yields frames in BGR format
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        img = QtGui.QImage(self.frame, self.frame.shape[1],self.frame.shape[0], QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.ui.label.setPixmap(pix)

    def start(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000./self.fps)

    def stop(self):
        self.cap.release()
        self.timer.stop()
        cv2.destroyAllWindows()


    # ------ Modification ------ #
    def capture(self):
            if self.ui.lineEdit.text() != None:
                cv2.imwrite(str(self.folderChoosen) +'/img_%s_%d.jpg' % (self.ui.lineEdit.text(),self.ith_frame), self.frame)
            else:
                cv2.imwrite(str(self.folderChoosen) + '/img_%d.jpg' % self.ith_frame, self.frame)
            self.ith_frame += 1

    # ------ Modification ------ #

    def deleteLater(self):
        if self.isCapturing:
           self.cap.release()
           super(QWidget, self).deleteLater()
        else:
            self.close()

    def closeEvent(self, event):
        close = QtWidgets.QMessageBox.question(self,
                                               "QUIT CAM",
                                               "Are you sure want to stop process?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def Folderchoose(self):
        self.folderChoosen = QFileDialog.getExistingDirectory(self, 'Folfer Contain Image', expanduser('~'))
        if self.folderChoosen != None:
            print(self.folderChoosen)

    def work(self):
        self.workThread.start()


class WorkThread(QThread):
    trigger = pyqtSignal()
    def __init__(self):
        super().__init__()

    def run(self):
        print('Search...')
        ports = serial.tools.list_ports.comports(include_links=False)
        for port in ports:
            print('Find port ' + port.device)
        ser = serial.Serial(port.device)
        if ser.isOpen():
            ser.close()
            ser = serial.Serial(port.device, 9600)
        while (1):
            data = ser.readline().decode("utf-8").strip('\n').strip('\r')
            print("We got: '{}'".format(data))
            time.sleep(0.1)
            if data == "Cam ON":
                print("Fail")
            else:
                print("Succed")
                self.trigger.emit()


if __name__=="__main__":
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())
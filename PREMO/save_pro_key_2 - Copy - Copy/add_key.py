# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
import sys
import wmi
import datetime as dt
from requestKey import *
from Module.SaveAndReadFile import *
import time
import smtplib


class ban_quyen():
    def __init__(self):
        super().__init__()
        self.serial_disk = []
        self.key=keyMenu()
    def checkdate(self):
        try:
            enday = self.key.readKey()[-10:]
        except:
            enday=dt.datetime.now().strftime('%m/%d/%Y')
            enday = dt.datetime.strptime(enday, "%m/%d/%Y")
            enday = (enday + dt.timedelta(days=1)).strftime('%m/%d/%Y')
        start_date = dt.datetime.now().strftime('%m/%d/%Y')
        time_string = dt.datetime.strptime(start_date, "%m/%d/%Y").strftime('%m/%d/%Y')
        time = []
        time.append(enday)
        while (1):
            if time_string not in time:
                break
            else:
                pass


class kt_serial_disk:
    def __init__(self):
        super().__init__()
        self.serial_disk = []
        self.key = keyMenu()

    def ma_serial(self):
        ma_disk = "W761TD39"
        return ma_disk

    def test_serial(self):
        c = wmi.WMI()
        for item in c.Win32_PhysicalMedia():
            items = (item.wmi_property('SerialNumber').Value)
            self.serial_disk.append(items)
        self.serial_disk1 = (self.serial_disk[0])
        return self.serial_disk1.replace(" ","")


class key_menu(QDialog):
    def __init__(self):
        super().__init__()
        self.test_user = ['1111']
        self.user_name = None
        self.ui = Ui_Lience()
        self.ui.setupUi(self)
        self.key = keyMenu()
        self.lience = ban_quyen()
        self.CPUCode = kt_serial_disk().test_serial()
        self.checkKey()
        self.ui.submitButton.clicked.connect(self.test_disk)
        self.ui.RequestKey.clicked.connect(self.sendmessage)
        self.ui.pushButton_sendemail.clicked.connect(self.showmessage)

    def checkKey(self):
        try:
            key = self.key.readKey()[:-10]
            if key == self.CPUCode:
                self.ui.logTextEdit.setDisabled(True)
                self.ui.logTextEdit.setReadOnly(True)
                self.ui.RequestKey.hide()
                return True
        except:
            return False

    def test_disk(self):
        try:
            lencpuCode = len(self.CPUCode)
            user_name = self.ui.usernameLineEdit.displayText()
            password = self.ui.passwordLineEdit.text()
            if (self.ui.logTextEdit.isReadOnly()):
                if password in self.test_user and user_name == "admin":
                    self.accept()
                else:
                    self.ui.label_3.show()
            else:
                inputKey = self.ui.logTextEdit.toPlainText()[:lencpuCode]
                day = int(self.ui.logTextEdit.toPlainText()[lencpuCode:])
                if password in self.test_user and inputKey == self.CPUCode:
                    enday = self.coverToDate(day)
                    self.key.saveKey(self.CPUCode + enday)
                    self.accept()
                else:
                    self.ui.label_3.show()
        except:
            self.ui.label_3.show()

    def sendmessage(self):
        if (self.ui.label_5.isHidden()):
            self.ui.label_5.show()
            self.ui.lineEdit_email.show()
            self.ui.pushButton_sendemail.show()
        else:
            self.ui.label_5.hide()
            self.ui.lineEdit_email.hide()
            self.ui.pushButton_sendemail.hide()
            self.ui.label_message.hide()

    def showmessage(self):
        self.sendmail(self.ui.lineEdit_email.displayText(), self.CPUCode)
        self.ui.label_message.show()

    def sendmail(self, useremail, CPUcode):
        gmail_user = 'daiwavn.tam195@gmail.com'
        gmail_password = 'daiwavn.tam195@123'
        sent_from = gmail_user
        to = ['thaingoctam11cdt2@gmail.com', 'Nguyenvinhstv@gmail.com']
        subject = 'Lience'
        email_text = "Request Key, My email is: " + useremail + "\n" + "Serial: " + CPUcode
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (sent_from, ", ".join(to), subject, email_text)
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to, message)
            server.close()

        except:
            print('Something went wrong...')

    def coverToDate(self, days):
        start_date1 = dt.datetime.now().strftime('%m/%d/%Y')
        date_1 = dt.datetime.strptime(start_date1, "%m/%d/%Y")
        end_date = (date_1 + dt.timedelta(days=days)).strftime('%m/%d/%Y')
        return end_date


if __name__ == "__main__":
    k = kt_serial_disk()
    serial_disk = k.ma_serial()
    test_serial_disk = k.test_serial()
    if serial_disk in test_serial_disk:
        app = QApplication(sys.argv)
        r = key_menu()
        r.show()
        sys.exit(app.exec_())

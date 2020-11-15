# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import glob, os, time
from pathlib import Path
import re


class SaveAndRead(QMainWindow):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.absoluteUrlFile = os.path.dirname(__file__).replace("\Module", "")

    def writeFileConfig(self, URLfile, dateModified):
        try:
            os.mkdir(self.absoluteUrlFile + "/config")
            file = open(self.absoluteUrlFile + "/config/config.txt", "w+", encoding='utf-8')
            file.close()
        except FileExistsError:
            pass
        file = open(self.absoluteUrlFile + "/config/config.txt", "r+", encoding='utf-8')
        data = file.readlines()
        file.seek(0)
        file.truncate()
        if ((URLfile != None) & (dateModified != None)):
            if (len(data) >= 1):
                data[0] = URLfile + "\n"
                data[1] = dateModified + "\n"
                file.writelines(data)
            else:
                file.write(URLfile + "\n")
                file.write(dateModified + "\n")
        elif ((URLfile != None) & (dateModified == None)):
            if (len(data) >= 1):
                data[0] = URLfile + "\n"
                file.writelines(data)
            else:
                file.write(URLfile + "\n")
                file.write("" + "\n")
        elif ((URLfile == None) & (dateModified != None)):
            if (len(data) >= 1):
                data[1] = dateModified + "\n"
                file.writelines(data)
            else:
                file.write("" + "\n")
                file.write(dateModified + "\n")
        file.close()

    def readFileConfig(self):
        try:
            fileURL = open(self.absoluteUrlFile + "/config/config.txt", "r", encoding='utf-8')

            URL = fileURL.readline().replace("\n", "") + ".txt"
            dateModified = fileURL.readline().replace("\n", "")
            portCam = fileURL.readline().replace("\n", "")
            urlproductCode = fileURL.readline().replace("\n", "")
            fileURL.close()
            return URL, dateModified, portCam, urlproductCode
            # return URL, dateModified, portCam, None
        except:
            return None, None, None, None

    def getNameConfig(self):
        try:
            filename, _, _, _ = self.readFileConfig()
            filename = filename.split("/")[-1]
            return str(filename).replace(".txt","")
        except:
            return None

    def formatURl(self, URl):
        URL = re.sub(r'[?|\\\||!]', r'/', URl)
        return URL

    def copyListAndRemoveObject(self, list):
        ListCopy = []
        for item in list:
            listTG = []
            for i in range(len(item)):
                if i == 0 or i == 13:
                    pass
                else:
                    listTG.append(item[i])
            ListCopy.append(listTG)
        return ListCopy

    def formatList(self, string):
        lista = list(string.split(","))
        listb = []
        start = 0
        end = 0
        for n, i in enumerate(lista):
            if i.startswith("[") or i.startswith(" ["):
                start = n
                i = i.replace("[", "").replace(" ", "")
                self.convertToNumber(lista, i, n)
            if i.endswith("]"):
                end = n
                i = i.replace("]", "")
                self.convertToNumber(lista, i, n)
                listb.append(lista[start:end + 1])
            else:
                self.convertToNumber(lista, i, n)
        return listb

    def list2String(self, list):
        string = str(list)
        return string[1:-1]

    def convertToNumber(self, lista, i, n):
        try:
            i = int(i)
            lista[n] = i
        except:
            try:
                i = float(i)
                lista[n] = i
            except:
                pass

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "Text Files (*.txt)", options=options)
        return fileName

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "Text Files (*.txt)", options=options)
        return fileName

    def writeFile(self, text_file, data, saveList, saveListPosition, loaidiem, area, width, height, number, testPin,
                  all_area):
        if self.name == "cam1_setting":
            if len(data) >= 7:
                data[3] = self.list2String(saveList) + "\n"
                data[4] = self.list2String(saveListPosition) + "\n"
                data[5] = str(area) + "," + str(width) + "," + str(height) + "," + str(number) + "," + str(
                    testPin) + "," + str(all_area) + "\n"
                data[6] = self.list2String(loaidiem) + "\n"
                text_file.writelines(data)
            else:
                text_file.write("------------------------------------" + "\n")
                text_file.write("----------------Camera 1------------" + "\n")
                text_file.write("" + "\n")
                text_file.write(self.list2String(saveList) + "\n")
                text_file.write(self.list2String(saveListPosition) + "\n")
                text_file.write(
                    str(area) + "," + str(width) + "," + str(height) + "," + str(number) + "," + str(
                        testPin) + "," + str(all_area) + "\n")
                text_file.write(self.list2String(loaidiem) + "\n")
            text_file.close()

        elif self.name == "cam2_setting":
            if len(data) >= 13:
                data[10] = self.list2String(saveList) + "\n"
                data[11] = self.list2String(saveListPosition) + "\n"
                data[12] = str(area) + "," + str(width) + "," + str(height) + "," + str(number) + "," + str(
                    testPin) + "," + str(all_area) + "\n"
                data[13] = self.list2String(loaidiem) + "\n"
                text_file.writelines(data)
            elif len(data) >= 7:
                text_file.writelines(data)
                text_file.write("------------------------------------" + "\n")
                text_file.write("----------------Camera 2------------" + "\n")
                text_file.write("" + "\n")
                text_file.write(self.list2String(saveList) + "\n")
                text_file.write(self.list2String(saveListPosition) + "\n")
                text_file.write(
                    str(area) + "," + str(width) + "," + str(height) + "," + str(number) + "," + str(
                        testPin) + "," + str(all_area) + "\n")
                text_file.write(self.list2String(loaidiem) + "\n")
            else:
                text_file.write("" + "\n")
                text_file.write("" + "\n")
                text_file.write("" + "\n")
                text_file.write("" + "\n")
                text_file.write("" + "\n")
                text_file.write("" + "\n")
                text_file.write("" + "\n")
                text_file.write("------------------------------------" + "\n")
                text_file.write("----------------Camera 2------------" + "\n")
                text_file.write("" + "\n")
                text_file.write(self.list2String(saveList) + "\n")
                text_file.write(self.list2String(saveListPosition) + "\n")
                text_file.write(
                    str(area) + "," + str(width) + "," + str(height) + "," + str(number) + "," + str(
                        testPin) + "," + str(all_area) + "\n")
                text_file.write(self.list2String(loaidiem) + "\n")
            text_file.close()

    def saveFile(self, URLFile, items, itemp, loaidiem, area, width, height, number, testPin, all_area):
        saveList = self.copyListAndRemoveObject(items)
        saveListPosition = self.copyListAndRemoveObject(itemp)
        try:
            text_file = open(URLFile + ".txt", "r+")
            data = text_file.readlines()
            text_file.seek(0)
            text_file.truncate()
            self.writeFile(text_file, data, saveList, saveListPosition, loaidiem, area, width, height, number, testPin,
                           all_area)
            self.writeFileConfig(URLFile, None)
            return True
        except:
            return self.fileError()

    def saveAsFile(self, URLFile, URLNewFile, items, itemp, loaidiem, area, width, height, number, testPin, all_area):
        saveList = self.copyListAndRemoveObject(items)
        saveListPosition = self.copyListAndRemoveObject(itemp)
        try:
            if (os.path.exists(URLFile + ".txt")):
                text_file = open(URLFile + ".txt", "r+")
                data = text_file.readlines()
                text_file.close()
            else:
                data = []
            new_file = open(URLNewFile + ".txt", "r+")
            self.writeFile(new_file, data, saveList, saveListPosition, loaidiem, area, width, height, number, testPin,
                           all_area)
            # self.writeFileConfig(URLNewFile,None)
            return True
        except:
            self.fileError()

    def readFile2List(self, URLs, openF):
        try:
            if not openF:
                fileURL = open(self.absoluteUrlFile + "/config/config.txt", "r", encoding='utf-8')
                URLCam = fileURL.readline().replace("\n", "") + ".txt"
                fileURL.close()
            else:
                URLCam = URLs
        except:
            URLCam = URLs

        try:
            f = open(URLCam, "r", encoding='utf-8')
            data = f.readlines()
            if (self.name == "cam1_setting"):
                listlineitems = self.formatList(data[3].replace("\n", ""))
                listlineItemp = self.formatList(data[4].replace("\n", ""))
                listLineCheckbox = list(data[5].replace("\n", "").split(","))
                listlineloaidiem = self.formatList(data[6].replace("\n", ""))
                return listlineitems, listlineItemp, listLineCheckbox, listlineloaidiem, URLCam
            else:
                listlineitems = self.formatList(data[10].replace("\n", ""))
                listlineItemp = self.formatList(data[11].replace("\n", ""))
                listLineCheckbox = list(data[12].replace("\n", "").split(","))
                listlineloaidiem = self.formatList(data[13].replace("\n", ""))
                return listlineitems, listlineItemp, listLineCheckbox, listlineloaidiem, URLCam
        except:
            listlineitems = []
            listlineItemp = []
            listLineCheckbox = []
            listlineloaidiem = []
            return listlineitems, listlineItemp, listLineCheckbox, listlineloaidiem, URLCam

    def getFProductCode(self):
        try:
            _, _, _, urlProduct = self.readFileConfig()
            # file = open(self.absoluteUrlFile + "/data/ProductCode.txt", "r", encoding='utf-8')
            file = open(urlProduct, "r", encoding='utf-8')
            productCode = file.readline().replace("\n", "")
            return productCode
        except:
            self.ProductCodeError()
            return None

    def getDateModified(self):
        try:
            _, _, _, urlProduct = self.readFileConfig()
            dateModified = time.ctime(os.path.getmtime(urlProduct))
            _, lastDateModified, _, _ = self.readFileConfig()
            return lastDateModified, dateModified
        except:
            self.ProductCodeError()
            return None, None

    def getPort(self):
        try:
            _, _, port, _ = self.readFileConfig()
            listPort = list(port.split(","))
            return listPort
        except:
            return [0, 0]


    def fileError(self):
        close = QMessageBox.question(self,
                                     "File Not Found",
                                     "Do you want save new file ?",
                                     QMessageBox.Yes | QMessageBox.No)
        return False if close == QMessageBox.Yes else True

    def ProductCodeError(self):
        QMessageBox.question(self,
                             "File ProductCode Error",
                             "Please check Again?",
                             QMessageBox.Ok)


class keyMenu():

    def saveKey(self, key):
        try:
            os.mkdir("key")
        except FileExistsError:
            pass
        file = open("key/key.txt", "w+", encoding='utf-8')
        encode = key.encode('utf-8')
        myint = int.from_bytes(encode, 'little')
        file.write(str(myint) + "\n")
        file.close()

    def readKey(self):
        try:
            fileURL = open("key/key.txt", "r", encoding='utf-8')
            key = int(fileURL.readline().replace("\n", ""))
            fileURL.close()
            recoveredbytes = key.to_bytes((key.bit_length() + 7) // 8, 'little')
            recoveredstring = recoveredbytes.decode('utf-8')
            return recoveredstring
        except:
            return None

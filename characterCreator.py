import sys
import xml.etree.ElementTree as ET
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class MainWindow(QMainWindow):
    mainWindow = None
    filePath = 'C:\\Users\\Jan-m\\Documents\\My Games\\Binding of Isaac Afterbirth+ Mods\\fiendfoliosteamworkshop_2305131709\\content'
    currentXML = None
    enabledUI = False
    lookupTable = {}

    def resetAll(self):
        self.mainWindow.comboBoxCharacter.clear()
        self.mainWindow.comboBoxCharacter.addItem("<Nothing selected>")
        self.mainWindow.comboBoxCharacter.addItem("+ Create new Character...")
        self.mainWindow.labelXML.clear()

    def updateSpritesheetImage(self):
        path = self.filePath.replace("players.xml","").replace("content", "resources")
        pixmap = QPixmap(path+self.currentXML.attrib["root"]+self.mainWindow.textSpritesheet.text())
        self.mainWindow.labelSpritesheet.setPixmap(pixmap)

    def updateNameImage(self):
        path = self.filePath.replace("players.xml","").replace("content", "resources")
        pixmap = QPixmap(path+self.currentXML.attrib["nameimageroot"]+self.mainWindow.textNameImage.text())
        self.mainWindow.labelNameImage.setPixmap(pixmap)

    def updatePortraitImage(self):
        path = self.filePath.replace("players.xml","").replace("content", "resources")
        pixmap = QPixmap(path+self.currentXML.attrib["portraitroot"]+self.mainWindow.textPortraitImage.text())
        self.mainWindow.labelPortraitImage.setPixmap(pixmap)

    def loadCharacter(self, index):
        characterXML = list(self.currentXML)[index]
        self.mainWindow.labelXML.clear()
        self.mainWindow.labelXML.insertPlainText(ET.tostring(characterXML, encoding="unicode"))
        attrs = characterXML.attrib

        self.mainWindow.boxHP.setValue(float(attrs["hp"])/2 if "hp" in attrs else 0)
        self.mainWindow.boxSoulHP.setValue(float(attrs["armor"])/2 if "armor" in attrs else 0)
        self.mainWindow.boxBlackHP.setValue(float(attrs["black"])/2 if "black" in attrs else 0)
        self.mainWindow.boxCoins.setValue(float(attrs["coins"]) if "coins" in attrs else 0)
        self.mainWindow.boxKeys.setValue(float(attrs["keys"]) if "keys" in attrs else 0)
        self.mainWindow.boxBombs.setValue(float(attrs["bombs"]) if "bombs" in attrs else 0)
        self.mainWindow.boxPill.setCurrentIndex(float(attrs["pill"]) if "pill" in attrs else 0)
        self.mainWindow.boxCard.setCurrentIndex(float(attrs["card"]) if "card" in attrs else 0)
        self.mainWindow.boxPocketActive.setValue(float(attrs["pocketActive"]) if "pocketActive" in attrs else 0)
        self.mainWindow.boxItems.setText(attrs["items"] if "items" in attrs else "")
        self.mainWindow.boxTrinket.setText(attrs["trinket"] if "trinket" in attrs else "")
        self.mainWindow.boxCharName.setText(attrs["name"] if "name" in attrs else "")
        self.mainWindow.textSpritesheet.setText(attrs["skin"] if "skin" in attrs else "")
        self.mainWindow.textNameImage.setText(attrs["nameimage"] if "nameimage" in attrs else "")
        self.mainWindow.textPortraitImage.setText(attrs["portrait"] if "portrait" in attrs else "")
        self.mainWindow.textBirthright.setText(attrs["birthright"] if "birthright" in attrs else "")
        self.mainWindow.textCostumeSuffix.setText(attrs["costumeSuffix"] if "costumeSuffix" in attrs else "")
        self.mainWindow.boxSkinColor.setCurrentIndex(int(attrs["skinColor"]) if "skinColor" in attrs else -1)
        self.mainWindow.boxCostumeID.setValue(int(attrs["costume"]) if "costume" in attrs else 0)
        self.mainWindow.checkBoxCanShoot.setChecked(False if "canShoot" in attrs and attrs["canShoot"] == "false" else True)
        self.mainWindow.boxAchievement.setValue(int(attrs["achievement"]) if "achievement" in attrs else 0)
        
        self.updatePortraitImage()
        self.updateSpritesheetImage()
        self.updateNameImage()

    def updateValue(self, attrList, attrName, val, defaultVal):
        if str(val) != defaultVal :
            attrList[attrName] = str(val)
        elif attrName in attrList:
            del attrList[attrName]

        
    def updateXML(self):
        MW = self.mainWindow
        characterXML = list(self.currentXML)[ MW.comboBoxCharacter.currentIndex() - 2]
        attrs = characterXML.attrib
        attrs["hp"] = str(int(MW.boxHP.value() * 2))
        self.updateValue(attrs, "armor", int(MW.boxSoulHP.value() * 2), "0")
        self.updateValue(attrs, "black", int(MW.boxBlackHP.value() * 2), "0")
        self.updateValue(attrs, "coins", MW.boxCoins.value(), "0")
        self.updateValue(attrs, "keys", MW.boxKeys.value(), "0")
        self.updateValue(attrs, "bombs", MW.boxBombs.value(), "0")
        self.updateValue(attrs, "pill", MW.boxPill.currentIndex(), "0")
        self.updateValue(attrs, "card", MW.boxCard.currentIndex(), "0")
        self.updateValue(attrs, "pocketActive", MW.boxPocketActive.value(), "0")
        self.updateValue(attrs, "items", MW.boxItems.text(), "")
        self.updateValue(attrs, "trinket", MW.boxTrinket.text(), "")
        self.updateValue(attrs, "name", MW.boxCharName.text(), "")
        self.updateValue(attrs, "skin", MW.textSpritesheet.text(), "")
        self.updateValue(attrs, "nameimage", MW.textNameImage.text(), "")
        self.updateValue(attrs, "portrait", MW.textPortraitImage.text(), "")
        self.updateValue(attrs, "birthright", MW.textBirthright.text(), "")
        self.updateValue(attrs, "costumeSuffix", MW.textCostumeSuffix.text(), "")
        self.updateValue(attrs, "skinColor", MW.boxSkinColor.currentIndex()-1, "-1")
        self.updateValue(attrs, "costume", MW.boxCostumeID.value(), "0")
        self.updateValue(attrs, "canShoot", str(MW.checkBoxCanShoot.isChecked()).lower(), "true")
        self.updateValue(attrs, "achievement", MW.boxAchievement.value(), "0")

        MW.labelXML.clear()
        MW.labelXML.insertPlainText(ET.tostring(characterXML, encoding="unicode"))

    @Slot()
    def openFile(self):
        self.resetAll()
        fname = QFileDialog.getOpenFileName(None, 'Open character file', self.filePath ,"XML file (*.xml )")
        self.filePath = fname[0]
        self.currentXML = ET.parse(self.filePath).getroot()
        for child in list(self.currentXML):
            attrs = child.attrib
            if attrs["name"]:
                self.mainWindow.comboBoxCharacter.addItem(attrs["name"])
        
        self.enabledUI = True


    @Slot()
    def newFile(self):
        print("new")

    @Slot()
    def magic(self):
        print("test")

    @Slot()
    def switchCharacter(self, index):
        print(self.enabledUI)
        if not self.enabledUI:
            return

        if index == 0:
            return
        elif index == 1:
            print("NEW Character")
        else:
            self.loadCharacter(index-2)



    def readPocketitems(self, filePath):
        if "colors" not in self.lookupTable:
            self.lookupTable["colors"] = {"-1": "Default","0": "Black", "1": "Blue", "2": "Green", "3": "Grey", "4": "Red", "5": "White"}
        if "pilleffect" not in self.lookupTable:
            self.lookupTable["pilleffect"] = {}
            self.lookupTable["pilleffect"][-1] = "-"
        if "card" not in self.lookupTable:
            self.lookupTable["card"] = {}
            self.lookupTable["card"][0] = "-"

        root = ET.parse(filePath).getroot()
        for child in list(root):
            attrib = child.attrib
            if "card" in child.tag or "rune" in child.tag:
                self.lookupTable["card"][int(attrib["id"])] = attrib["name"]
            if "pilleffect" in child.tag:
                self.lookupTable["pilleffect"][int(attrib["id"])] = attrib["name"]
        self.lookupTable["card"][0] = "-"


    def updateSelectionMenus(self):
        for x, y in self.lookupTable["card"].items():
            self.mainWindow.boxCard.addItem(y)
        for x, y in self.lookupTable["pilleffect"].items():
            self.mainWindow.boxPill.addItem(y)
        for x, y in self.lookupTable["colors"].items():
            self.mainWindow.boxSkinColor.addItem(y)

    def __init__(self):
        app = QApplication(sys.argv)
        ui_file_name = "mainWindow.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        loader = QUiLoader()
        self.mainWindow = loader.load(ui_file)
        ui_file.close()
        if not self.mainWindow:
            print(loader.errorString())
            sys.exit(-1)

        # Init UI
        enabledUI = False
        self.resetAll()
        self.readPocketitems('data\\pocketitems.xml')
        self.updateSelectionMenus()

        # Connect stuff
        self.mainWindow.createButton.clicked.connect(self.magic)
        self.mainWindow.actionNew.triggered.connect(self.newFile)
        self.mainWindow.actionLoad_File.triggered.connect(self.openFile)
        self.mainWindow.actionSave.triggered.connect(self.updateXML)
        self.mainWindow.comboBoxCharacter.currentIndexChanged.connect(self.switchCharacter)


        
        self.mainWindow.show()
        sys.exit( app.exec_() )

if __name__ == "__main__":
    MainWindow()


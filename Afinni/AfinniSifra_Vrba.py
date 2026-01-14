from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
from math import gcd
import os

slozka = os.path.dirname(os.path.abspath(__file__))
moje_gui = "GUI_Afinni_Vrba.ui"
directions = os.path.join(slozka, moje_gui)

Ui_MainWindow, QtBaseClass = uic.loadUiType(directions)

class GUI(QMainWindow, Ui_MainWindow):

    abeceda=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

    def odstraneniDiakritiky(self, text):
        specialniZnaky = "ÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝßàáâãäåçèéêëìíîïñòóôõöùúûüýÿĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĶķĸĹĺĻļĽľĿŀŁłŃńŅņŇňŉŊŋŌōŎŏŐőŔŕŖŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽžſ"
        normalniZnaky = "AAAAAACEEEEIIIINOOOOOUUUUYsaaaaaaceeeeiiiinooooouuuuyyAaAaAaCcCcCcCcDdDdEeEeEeEeEeGgGgGgGgHhHhIiIiIiIiIiKkkLlLlLlLlLlNnNnNnNnNOoOoOoRrRrRrSsSsSsSsTtTtTtUuUuUuUuUuUuWwYyYZzZzZzs"
        newText = ""

        for i in text:
            if i in specialniZnaky:
                newText = newText + normalniZnaky[specialniZnaky.find(i)]
            else:
                newText = newText + i
        return newText
    
    def odstraneniSpecialZnaku(self, text):
        newText = ""

        for i in text:
            if i.isalnum() or i == " ":
                newText = newText + i
        return newText
    
    def inverzni_prvek(self, a, m):
        if gcd(a, m) != 1:
            return -1
        else:
            for i in range(0, m):
                if (i*a % m) == 1:
                    break
            return i
        
    def sifrovani(self):

        popupError = QMessageBox()
        popupError.setIcon(QMessageBox.Critical)
        popupError.setWindowTitle("Nepodařilo se.")

        zasifrovanyText = ""

        if self.lineEditCisloA.text() != "":
            a = int(self.lineEditCisloA.text())
        else:
            popupError.setText("Chybí klíč A")
            popupError.exec()
            return None
        
        if self.lineEditCisloB.text() != "":
            b = int(self.lineEditCisloB.text())
        else:
            popupError.setText('Chybí klíč B')
            popupError.exec()
            return None
        
        activeText = self.lineEditTextSifrovani.text()

        if activeText != "":
            activeText = activeText.upper()
            activeText = activeText.replace(" ", "XMEZERAX")
            activeText = activeText.replace("1", "XJEDNAX")
            activeText = activeText.replace("2", "XDVAX")
            activeText = activeText.replace("3", "XTRIX")
            activeText = activeText.replace("4", "XCTYRIX")
            activeText = activeText.replace("5", "XPETX")
            activeText = activeText.replace("6", "XSESTX")
            activeText = activeText.replace("7", "XSEDMX")
            activeText = activeText.replace("8", "XOSMX")
            activeText = activeText.replace("9", "XDEVETX")
            activeText = activeText.replace("0", "XNULAX")
            activeText = activeText.upper()
            activeText = self.odstraneniDiakritiky(activeText)
            activeText = self.odstraneniSpecialZnaku(activeText)

            filtActiveText = activeText

            sifrovaciAbeceda = ""
        else:
            popupError.setText("Chybí text pro šifrování")
            popupError.exec()
            return None
        
        if gcd(a, 26) == 1:
            for x in range(len(activeText)):
                for y in range(len(self.abeceda)):
                    if activeText[x] == self.abeceda[y]:
                        novePismeno = (a*y+b)%26
                        zasifrovanyText += self.abeceda[novePismeno]

            rozdelenyText = ""

            for x in range(len(zasifrovanyText)):
                rozdelenyText = rozdelenyText + zasifrovanyText[x]
                if (x + 1) % 5 == 0:
                    rozdelenyText = rozdelenyText + " "

            for x in range(len(self.abeceda)):
                sifrovaciAbeceda = sifrovaciAbeceda + self.abeceda[(a*x+b)%26] + ""

            self.zasifrovanyTextGUI.setText("Zašifrovaný text: " + rozdelenyText)
            self.sifrovaciAbecedaGUI.setText("Šifrovací abeceda: " + sifrovaciAbeceda)
            self.vyfiltrovanyTextGUI.setText("Vyfiltrovaný text: " + filtActiveText)
        else:
            popupError.setText("Číslo A nesmí být soudělné s číslem 26")
            popupError.exec()
            return None
        
    def desifrovani(self):

        popupError = QMessageBox()
        popupError.setIcon(QMessageBox.Critical)
        popupError.setWindowTitle("Nepodařilo se.")

        if self.lineEditCisloA.text() != "":
            a = int(self.lineEditCisloA.text())
        else:
            popupError.setText("Chybí klíč A")
            popupError.exec()
            return None
        
        if self.lineEditCisloB.text() != "":
            b = int(self.lineEditCisloB.text())
        else:
            popupError.setText('Chybí klíč B')
            popupError.exec()
            return None

        activeText = self.lineEditTextDesifrovani.text().upper().replace(" ", "")

        if activeText == "":
            popupError.setText("Chybí text pro dešifrování")
            popupError.exec()
            return None

        a_invert = self.inverzni_prvek(a, 26)
        if a_invert != -1:
            desifrovanyText = ""
            activetext = self.lineEditTextDesifrovani.text()

            for x in activetext:
                for y in range(len(self.abeceda)):
                    if x == self.abeceda[y]:
                        novy_index = (y-b)*a_invert%26
                        desifrovanyText += self.abeceda[novy_index]
        else:
            popupError.setText("A klíč nemá inverzní číslo.")
            popupError.exec()
            return None
        
        if activetext != "":
            desifrovanyText = desifrovanyText.replace("XMEZERAX", " ")
            desifrovanyText = desifrovanyText.replace("XJEDNAX", "1")
            desifrovanyText = desifrovanyText.replace("XDVAX", "2")
            desifrovanyText = desifrovanyText.replace("XTRIX", "3")
            desifrovanyText = desifrovanyText.replace("XCTYRIX", "4")
            desifrovanyText = desifrovanyText.replace("XPETX", "5")
            desifrovanyText = desifrovanyText.replace("XSESTX", "6")
            desifrovanyText = desifrovanyText.replace("XSEDMX", "7")
            desifrovanyText = desifrovanyText.replace("XOSMX", "8")
            desifrovanyText = desifrovanyText.replace("XDEVETX", "9")
            desifrovanyText = desifrovanyText.replace("XNULAX", "0")

            self.desifrovanyTextGUI.setText("Dešifrování: " + desifrovanyText)

        else:
            popupError.setText("Chybí text pro dešifrování")
            popupError.exec()
            return None

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushZasifrovat.clicked.connect(self.sifrovani)
        self.pushDesifrovat.clicked.connect(self.desifrovani)
        self.abecedaGUI.setText("Abeceda: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z")


if __name__ == "__main__":
    gui = QApplication(sys.argv)
    popupWindow = GUI()
    popupWindow.show()
    sys.exit(gui.exec_())
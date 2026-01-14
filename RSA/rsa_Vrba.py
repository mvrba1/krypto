from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
import os
from random import randint
from math import gcd, sqrt

slozka = os.path.dirname(os.path.abspath(__file__))
moje_gui = "GUI_RSA_Vrba.ui"
directions = os.path.join(slozka, moje_gui)

Ui_MainWindow, QtBaseClass = uic.loadUiType(directions)

class GUI(QMainWindow, Ui_MainWindow):

    def prvocislo(self, n):
        for i in range(2, int(sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generovaniRandomCisla(self):
        while True:
            cislo = randint(10**12, 10**13 - 1)
            if self.prvocislo(cislo):
                return cislo
            
    def prevodSlova(self, slovo):
        binarka = ""
        decimal = []
        blocks = [slovo[i:i + 7] for i in range(0, len(slovo), 7)]

        for i in range(len(blocks)):
            while len(blocks[i]) != 7:
                blocks[i] =  blocks[i] + " "
        for i in blocks:
            for j in i:
                char = bin(ord(j))[2:]
                while len(char) < 12:
                    char = "0" + char
                binarka = binarka + char
            decimal.append(int(binarka, 2))
            binarka = ""
        return decimal
    
    def prevodCisla(self, cislo):
        text = ""
        for i in cislo:
            binarka = bin(i)[2:]
            while len(binarka) % 12 != 0:
                binarka = "0" + binarka
            blocks = [binarka[i:i + 12] for i in range(0, len(binarka), 12)]
            decimal = []
            for i in blocks:
                decimal.append(int(i, 2))
            for i in decimal:
                text = text + chr(i)
        return text
    
    def hodnota(self):
        if self.radioButtonNahodna.isChecked():
            p = self.generovaniRandomCisla()
            q = self.generovaniRandomCisla()
            n = p * q
            eulerCislo = (p - 1) * (q - 1)
            e = randint(1, n - 1)
            while gcd(e, eulerCislo) != 1:
                e = randint(1, n - 1)
            d = pow(e, -1, eulerCislo)

        elif self.radioButtonRucni.isChecked():
            n = int(self.lineEditHodnotaN.text())
            d = int(self.lineEditHodnotaD.text())
            e = int(self.lineEditHodnotaE.text())

        global privatniKlic
        global verejnyKlic

        verejnyKlic = [n, e]
        privatniKlic = [n, d]

        self.verejnyKlicGUI.setText("Veřejný klíč: " + str(verejnyKlic))
        self.privatniKlicGUI.setText("Privátní klíč: " + str(privatniKlic))
        self.lineEditHodnotaN.setText(str(n))
        self.lineEditHodnotaD.setText(str(d))
        self.lineEditHodnotaE.setText(str(e))

    def sifrovani(self):
        popupError = QMessageBox()
        popupError.setIcon(QMessageBox.Critical)
        popupError.setWindowTitle("Nepodařilo se.")

        self.hodnota()
        text = self.lineEditSifrovani.text()
        slovo = self.prevodSlova(text)

        if any(i > verejnyKlic[0] for i in slovo):
            popupError.setText("Slovo musí být větší než n")
            popupError.exec_()
            return None
        
        zasifrovanyText = ""

        for i in slovo:
            zasifrovanyText = zasifrovanyText + str(pow(i, verejnyKlic[1], verejnyKlic[0])) + " "
        self.desitkovaSoustavaGUI.setText("V desítkové soustavě: " + str(slovo))
        self.zasifrovanyTextGUI.setText("Zasifrovaný text: " + zasifrovanyText.strip())

    def desifrovani(self):
        popupError = QMessageBox()
        popupError.setIcon(QMessageBox.Critical)
        popupError.setWindowTitle("Nepodařilo se.")

        textProDesifrovani = self.lineEditDesifrovani.text()
        textProDesifrovani = textProDesifrovani.split()

        desifrovanyText = []

        for i in textProDesifrovani:
            desifrovanyText.append(pow(int(i), privatniKlic[1], privatniKlic[0]))
        self.desifrovanyTextGUI.setText("Dešifrovaný text: " + self.prevodCisla(desifrovanyText).strip())

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushZasifrovat.clicked.connect(self.sifrovani)
        self.pushDesifrovat.clicked.connect(self.desifrovani)

if __name__ == "__main__":
    gui = QApplication(sys.argv)
    popupWindow = GUI()
    popupWindow.show()
    sys.exit(gui.exec_())
    
         

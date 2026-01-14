from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
import sys
import os
from random import randint
from math import gcd, sqrt
import base64
import zipfile
import time
import hashlib

slozka = os.path.dirname(os.path.abspath(__file__))
moje_gui = "GUI_DSA_Vrba.ui"
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
    
    podpisSoubor = ""

    def slozkaPodpisu(self):
        self.podpisSoubor = QFileDialog.getOpenFileName(self, "Vyberte složku pro podpis")
        cesta = self.podpisSoubor[0]

        self.nactenySoubor.setText("Soubor pro podpis: " + cesta)
        self.nazevSouboru.setText("Název souboru pro podpis: " + os.path.basename(cesta))

        stat = os.stat(cesta)
        datum = time.ctime(stat.st_mtime)
        self.datumSouboru.setText("Datum vytvoření souboru pro podpis: " + datum)

    ulozeniPodpisuCesta = os.getcwd()

    def ulozeniPodpisu(self):
        self.ulozeniPodpisuCesta = QFileDialog.getExistingDirectory(self, "Vyberte složku pro uložení podpisu")
        self.ulozeniCesta.setText("Cesta pro uložení podpisu: " + self.ulozeniPodpisuCesta)

    otevreniPodpisuCesta = ""

    def otevreniPodpisu(self):
        self.otevreniPodpisuCesta = QFileDialog.getOpenFileName(self, "Vyberte soubor .zip s podpisem")
        self.overeniSouboru.setText("Načtený soubor: " + self.otevreniPodpisuCesta[0])
    
    def hodnota(self):

        p = self.generovaniRandomCisla()
        q = self.generovaniRandomCisla()
        n = p * q
        eulerCislo = (p - 1) * (q - 1)
        e = randint(1, n - 1)
        while gcd(e, eulerCislo) != 1:
            e = randint(1, n - 1)
        d = pow(e, -1, eulerCislo)

        global privatniKlic
        global verejnyKlic

        verejnyKlic = [n, e]
        privatniKlic = [n, d]

        base64_n = str(base64.b64encode(str(n).encode()))[1:]
        base64_d = str(base64.b64encode(str(d).encode()))[1:]
        base64_e = str(base64.b64encode(str(e).encode()))[1:]

        with open("soukromy.priv", "w") as file:
            file.write("RSA [" + base64_n + ", " + base64_d + "]")
        
        with open("verejny.pub", "w") as file:
            file.write("RSA [" + base64_n + ", " + base64_e + "]")


    def sifrovani(self):
        popupError = QMessageBox()
        popupError.setIcon(QMessageBox.Critical)
        popupError.setWindowTitle("Nepodařilo se.")

        sha = hashlib.sha3_512()

        self.hodnota()
        
        with open(self.podpisSoubor[0], "rb") as file:
            text = file.read()
            sha.update(text)
            hashText = sha.hexdigest()

        slovo = self.prevodSlova(hashText)

        zasifrovanyText = ""

        for i in slovo:
            zasifrovanyText = zasifrovanyText + str(pow(i, privatniKlic[1], privatniKlic[0])) + " "

        with open("podpis.sign", "w") as file:
            file.write("RSA_SHA3-512 " + str(base64.b64encode(str(zasifrovanyText).encode()))[1:])

        with zipfile.ZipFile(self.ulozeniPodpisuCesta + "/podepsanySoubor.zip", "w") as zip:
            zip.write("podpis.sign")
            zip.write(self.podpisSoubor[0], arcname = "soubor.txt")

        os.remove("podpis.sign")

    def desifrovani(self):
        popupError = QMessageBox()
        popupError.setIcon(QMessageBox.Critical)
        popupError.setWindowTitle("Nepodařilo se.")

        sha = hashlib.sha3_512()
        
        with zipfile.ZipFile(self.otevreniPodpisuCesta[0], "r") as unzip:
            with unzip.open("podpis.sign") as file:
                podpis = file.read()
            with unzip.open("soubor.txt") as file:
                text = file.read()
                sha.update(text)
                hashText = sha.hexdigest()
        
        with open("verejny.pub", "r") as file:
            klic = file.read()

        klic = klic.split()
        klic.pop(0)
        klic[0] = int(base64.b64decode(klic[0]))
        klic[1] = int(base64.b64decode(klic[1]))

        podpis = str(podpis)[15:]
        podpis = base64.b64decode(podpis).decode()
        podpis = podpis.split()

        desifrovanyText = []

        for i in podpis:
            desifrovanyText.append(pow(int(i), klic[1], klic[0]))

        if self.prevodCisla(desifrovanyText).strip() == hashText:
            self.vysledekOvereni.setText("Úspěšné ověření podpisu.")
        else:
            self.vysledekOvereni.setText("Neúspěšné ověření podpisu.")

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushZasifrovat.clicked.connect(self.sifrovani)
        self.pushDesifrovat.clicked.connect(self.desifrovani)
        self.ulozeniCesta.setText("Cesta pro uložení: " + self.ulozeniPodpisuCesta)
        self.vybraniSouboruPodpis.clicked.connect(self.slozkaPodpisu)
        self.cestaSoubor.clicked.connect(self.ulozeniPodpisu)
        self.vybraniSouboruOvereni.clicked.connect(self.otevreniPodpisu)

if __name__ == "__main__":
    gui = QApplication(sys.argv)
    popupWindow = GUI()
    popupWindow.show()
    sys.exit(gui.exec_())
    
         

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QTimer
import sys
import os
from random import sample
from math import ceil

slozka = os.path.dirname(os.path.abspath(__file__))
moje_gui = "GUI_ADFGX_Vrba.ui"
directions = os.path.join(slozka, moje_gui)

Ui_MainWindow, QtBaseClass = uic.loadUiType(directions)

class GUI(QMainWindow, Ui_MainWindow):

    abeceda=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    abecedaSCisly=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9']

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
    
    def odstraneniDuplicity(self, text):
        text = text.upper()
        newText = ""

        for i in text:
            if i not in newText:
                newText = newText + i
        return newText
    
    def chybejiciZnakyAbeceda(self):
        if self.radioButtonADFGX.isChecked():
            if self.radioButtonCzech.isChecked():
                abeceda = self.abeceda.copy()
                if "W" in abeceda:
                    abeceda.remove("W")
            elif self.radioButtonEnglish.isChecked():
                abeceda = self.abeceda.copy()
                if "J" in abeceda:
                    abeceda.remove("J")
            else:
                return False
        elif self.radioButtonADFGVX.isChecked():
            abeceda = self.abecedaSCisly.copy()
        else:
            return False
        text = self.lineEditTextTabulka.text().upper()
        chybi = " ".join(abeceda) + " "
        for i in text:
            if i in abeceda and i != " " and i != ",":
                chybi = chybi.replace(i + " ", "")
        self.chybiGUI.setText(chybi)
        return chybi == ""

    
    def vytvoreniTabulky(self, sifra):
        tabulka = []

        if self.radioButtonNahodna.isChecked():
            choice = "nahodna"
        elif self.radioButtonRucni.isChecked():
            choice = "rucne"

        if self.radioButtonCzech.isChecked():
            jazyk = "czech"
        elif self.radioButtonEnglish.isChecked():
            jazyk = "english"

        if choice == "nahodna":
            if sifra == "ADFGX":
                if jazyk == "czech":
                    pozice = sample(range(0, 26), 26)
                    for i in pozice:
                        if self.abeceda[i] != "W":
                            tabulka.append(self.abeceda[i])
                    tabulka = [tabulka[i:i+5] for i in range(0, 25, 5)]

                elif jazyk == "english":
                    pozice = sample(range(0, 26), 26)
                    for i in pozice:
                        if self.abeceda[i] != "J":
                            tabulka.append(self.abeceda[i])
                    tabulka = [tabulka[i:i+5] for i in range(0, 25, 5)]
                
                return tabulka
            
            elif sifra == "ADFGVX":
                pozice = sample(range(0, 36), 36)
                for i in pozice:
                    tabulka.append(self.abecedaSCisly[i])
                tabulka = [tabulka[i:i+6] for i in range(0, 36, 6)]
                
                return tabulka
        
        elif choice == "rucne":
            popupError = QMessageBox()
            popupError.setIcon(QMessageBox.Critical)
            popupError.setWindowTitle("Nepodařilo se.")

            if self.chybejiciZnakyAbeceda():
                text = self.zadaniRucne.text().upper()
                text = self.odstraneniDuplicity(text)
                text = self.odstraneniSpecialZnaku(text)

                tabulka = []

                if choice == "ADFGX":
                    if any(char.isdigit() for char in text):
                        popupError.setText("V ADFGX nesmí být číslo")
                        popupError.exec()
                        return None
                    if jazyk == "czech" and "W" in text:
                        text = text.replace("W", "")
                    elif jazyk == "english" and "J" in text:
                        text = text.replace("J", "")
                    for i in text:
                        tabulka.append(i)

                    tabulka = [tabulka[i:i+5] for i in range (0, 25, 5)]

                elif choice == "ADFGVX":
                    for i in text:
                        tabulka.append(i)
                    
                    tabulka = [tabulka[i:i+6] for i in range (0, 36, 6)]

                return tabulka
            
            else:
                popupError.setText("Chybí nějaký znak")
                popupError.exec()
                return None
            
    def pripravaTextu(self, text):
        if self.radioButtonCzech.isChecked():
            jazyk = "czech"
        elif self.radioButtonEnglish.isChecked():
            jazyk = "english"

        if jazyk == "czech":
            text = text.upper().replace("W", "V")
        elif jazyk == "english":
            text = text.upper().replace("J", "I")

        text = text.replace(" ", "XMEZERAX")

        if self.radioButtonADFGX.isChecked():
            text = text.replace("1", "JEDNA")
            text = text.replace("2", "DVA")
            text = text.replace("3", "TRI")
            text = text.replace("4", "CTYRI")
            text = text.replace("5", "PET")
            text = text.replace("6", "SEST")
            text = text.replace("7", "SEDM")
            text = text.replace("8", "OSM")
            text = text.replace("9", "DEVET")
            text = text.replace("0", "NULA")
            text = text.replace(" ", "")

        text = self.odstraneniDiakritiky(text)
        text = self.odstraneniSpecialZnaku(text)

        return text
    
    def najitiPozice(self, char, tabulka, sifra):
        if sifra == "ADFGX":
            number = 5
        elif sifra == "ADFGVX":
            number = 6
        
        for radek in range(number):
            for sloupec in range(number):
                if tabulka[radek][sloupec] == char:
                    return radek, sloupec
                
    def sifrovani(self):
        popupError = QMessageBox()
        popupError.setIcon(QMessageBox.Critical)
        popupError.setWindowTitle("Nepodařilo se.")

        if self.radioButtonADFGX.isChecked():
            sifra = "ADFGX"
        elif self.radioButtonADFGVX.isChecked():
            sifra = "ADFGVX"
        
        klicoveSlovo = self.lineEditKlicoveSlovo.text()
        
        if klicoveSlovo != "":
            klicoveSlovo = klicoveSlovo.upper()
            klicoveSlovo = self.odstraneniDuplicity(klicoveSlovo)
            self.lineEditKlicoveSlovo.setText(klicoveSlovo)

        else:
            popupError.setText("Není zadán klíč")
            popupError.exec()
            return None
        
        activeText = self.lineEditTextSifrovani.text()

        if activeText == "":
            popupError.setText("Není zadán text pro šifrování")
            popupError.exec()
            return None
        
        filtrovanyText = self.pripravaTextu(activeText)

        self.vyfiltrovanyTextGUI.setText("Vyfiltrovaný text: " + filtrovanyText)

        global tabulka
        tabulka = self.vytvoreniTabulky(sifra)

        zasifrovanyText = ""
        for i in filtrovanyText:
            radek, sloupec = self.najitiPozice(i, tabulka, sifra)
            zasifrovanyText = zasifrovanyText + sifra[radek] + sifra[sloupec]

        radky = []
        sloupce = []

        for i in range(0, len(zasifrovanyText), len(klicoveSlovo)):
            radky.append(zasifrovanyText[i:i + len(klicoveSlovo)])

        for i in range(len(radky)):
            while (len(radky[i]) != len(klicoveSlovo)):
                radky[i] += " "

        for i in range(len(klicoveSlovo)):
            chars = [s[i] for s in radky if i < len(s)]
            sloupce.append("".join(chars))

        sloupceFinal = list(zip(klicoveSlovo, sloupce))
        transpozice = sorted(sloupceFinal)

        finalText = ""
        for i in range(len(transpozice)):
            finalText = finalText + transpozice[i][1]

        self.zasifrovanyTextGUI.setText("Zašifrovaný text: " + finalText)
        if sifra == "ADFGX":
            self.tabulkaGUI.setText("Tabulka: \n" +
                                str(tabulka[0]) + "\n" +
                                str(tabulka[1]) + "\n" +
                                str(tabulka[2]) + "\n" +
                                str(tabulka[3]) + "\n" +
                                str(tabulka[4]))
        elif sifra == "ADFGVX":
            self.tabulkaGUI.setText("Tabulka: \n" +
                                str(tabulka[0]) + "\n" +
                                str(tabulka[1]) + "\n" +
                                str(tabulka[2]) + "\n" +
                                str(tabulka[3]) + "\n" +
                                str(tabulka[4]) + "\n" +
                                str(tabulka[5]))
            
    def desifrovani(self):
        popupError = QMessageBox()
        popupError.setIcon(QMessageBox.Critical)
        popupError.setWindowTitle("Nepodařilo se.")

        if self.radioButtonADFGX.isChecked():
            sifra = "ADFGX"
        elif self.radioButtonADFGVX.isChecked():
            sifra = "ADFGVX"

        klicoveSlovo = self.lineEditKlicoveSlovo.text()
        
        if klicoveSlovo != "":
            klicoveSlovo = klicoveSlovo.upper()
            klicoveSlovo = self.odstraneniDuplicity(klicoveSlovo)
            self.lineEditKlicoveSlovo.setText(klicoveSlovo)

        else:
            popupError.setText("Není zadán klíč")
            popupError.exec()
            return None
        
        activeText = self.lineEditTextDesifrovani.text()

        if activeText == "":
            popupError.setText("Není zadán text pro dešifrování")
            popupError.exec()
            return None
        
        desifrovanyText = ""
        sloupce = []

        for i in range(0, len(activeText), ceil(len(activeText)/len(klicoveSlovo))):
            sloupce.append(activeText[i:i + ceil(len(activeText)/len(klicoveSlovo))])

        sloupceFinal = list(zip(sorted(klicoveSlovo), sloupce))

        def poradiZnaku(tupl):
            return klicoveSlovo.index(tupl[0])
        
        transpozice = sorted(sloupceFinal, key = poradiZnaku)

        helpText = ""
        for j in range(ceil(len(activeText)/len(klicoveSlovo))):
            for i in range(len(transpozice)):
                if j < len(transpozice[i][1]):
                    helpText = helpText + transpozice[i][1][j]

        helpText = helpText.replace(" ", "")

        dvojice = [helpText[i:i+2] for i in range(0, len(helpText), 2)]

        for x in dvojice:
            for i in range(len(sifra)):
                if sifra[i] == x[0]:
                    radek = i
            for i in range(len(sifra)):
                if sifra[i] == x[1]:
                    sloupec = i
            desifrovanyText = desifrovanyText + tabulka[radek][sloupec]

        desifrovanyText = desifrovanyText.replace("XMEZERAX", " ")
        desifrovanyText = desifrovanyText.replace("JEDNA","1")
        desifrovanyText = desifrovanyText.replace("DVA","2")
        desifrovanyText = desifrovanyText.replace("TRI","3")
        desifrovanyText = desifrovanyText.replace("CTYRI","4")
        desifrovanyText = desifrovanyText.replace("PET","5")
        desifrovanyText = desifrovanyText.replace("SEST","6")
        desifrovanyText = desifrovanyText.replace("SEDM","7")
        desifrovanyText = desifrovanyText.replace("OSM","8")
        desifrovanyText = desifrovanyText.replace("DEVET","9")
        desifrovanyText = desifrovanyText.replace("NULA", "0")

        self.desifrovanyTextGUI.setText("Dešifrovaný text: " + desifrovanyText)

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.chybejiciZnakyAbeceda)
        self.timer.start()
        self.pushZasifrovat.clicked.connect(self.sifrovani)
        self.pushDesifrovat.clicked.connect(self.desifrovani)

if __name__ == "__main__":
    gui = QApplication(sys.argv)
    popupWindow = GUI()
    popupWindow.show()
    sys.exit(gui.exec_())

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
from math import gcd
import os

slozka = os.path.dirname(os.path.abspath(__file__))
moje_gui = "GUI_Playfair_Vrba.ui"
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
    
    def odstraneniDuplicity(self, text):
        text = text.upper()
        newText = ""

        for i in text:
            if i not in newText:
                newText = newText + i
        return newText
    
    def vytvoreniTabulky(self, klicoveSlovo, jazyk):
        tabulka = []

        skip = "W" if jazyk == "czech" else "J" if jazyk == "english" else ""

        for i in klicoveSlovo:
            if i not in tabulka:
                tabulka.append(i)

        for i in self.abeceda:
            if i not in tabulka and i != skip:
                tabulka.append(i)

        tabulka = [tabulka[i:i+5] for i in range(0, 25, 5)]
        return tabulka
    
    def pripravaTextu(self, text, jazyk):
        if jazyk == "czech":
            text = text.upper().replace("W", "V")
        if jazyk == "english":
            text = text.upper().replace("J", "I")

        upravenyText = []

        text = text.replace(" ", "XMEZERAX")
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

        i = 0

        while i < len(text):
            if i == len(text) - 1:
                if text[i] == "X":
                    upravenyText.append(text[i] + "Q")
                else:
                    upravenyText.append(text[i] + "X")
                i = i + 1
            elif text[i] == text[i + 1]:
                if text[i] == "X":
                    upravenyText.append(text[i] + "Q")
                else:
                    upravenyText.append(text[i] + "X")
                i = i + 2
            else:
                upravenyText.append(text[i] + text[i + 1])
                i = i + 2
        return upravenyText    
    
    def najitiPozice(self, char, tabulka):
        for x in range(5):
            for y in range(5):
                if tabulka[x][y] == char:
                    return x, y
                
    def sifrovani(self):
        popupError = QMessageBox()
        popupError.setIcon(QMessageBox.Critical)
        popupError.setWindowTitle("Nepodařilo se.")

        klicoveSlovo = self.lineEditKlicoveSlovo.text()

        if klicoveSlovo != "":
            klicoveSlovo = klicoveSlovo.upper()
            klicoveSlovo = self.odstraneniDiakritiky(klicoveSlovo)
            klicoveSlovo = self.odstraneniSpecialZnaku(klicoveSlovo)
            klicoveSlovo = self.odstraneniDuplicity(klicoveSlovo)
            self.lineEditKlicoveSlovo.setText(klicoveSlovo)


            if len(klicoveSlovo)<7:
                popupError.setText("Klíč musí mít aspoň 8 znaků")
                popupError.exec()
                return None
            
            if any(char.isdigit() for char in klicoveSlovo):
                popupError.setText("Klíč nesmí mít číslice")
                popupError.exec()
                return None
        else:
            popupError.setText("Není zadán klíč")
            popupError.exec()
            return None
        
        activeText = self.lineEditTextSifrovani.text()

        if activeText != "":
            activeText = activeText.upper()
            activeText = self.odstraneniDiakritiky(activeText)
            activeText = self.odstraneniSpecialZnaku(activeText)
        else:
            popupError.setText("Chybí text pro šifrování")
            popupError.exec()
            return None
        
        if self.radioButtonCzech.isChecked():
            jazyk = "czech"
            klicoveSlovo = klicoveSlovo.replace("W", "V")
        elif self.radioButtonEnglish.isChecked():
            jazyk = "english"
            klicoveSlovo = klicoveSlovo.replace("Q", "O")

        self.lineEditKlicoveSlovo.setText(klicoveSlovo)

        tabulka = self.vytvoreniTabulky(klicoveSlovo, jazyk)
        duplikaty = self.pripravaTextu(activeText, jazyk)

        zasifrovanyText = ""
        filtrovanyText = ""

        for i in duplikaty:
            filtrovanyText = filtrovanyText + i

            radek1, sloupec1 = self.najitiPozice(i[0], tabulka)
            radek2, sloupec2 = self.najitiPozice(i[1], tabulka)

            if radek1 == radek2:
                zasifrovanyText = zasifrovanyText + tabulka[radek1][(sloupec1 + 1)%5]
                zasifrovanyText = zasifrovanyText + tabulka[radek2][(sloupec2 + 1)%5]
            elif sloupec1 == sloupec2:
                zasifrovanyText = zasifrovanyText + tabulka[(radek1 + 1)%5][sloupec1]
                zasifrovanyText = zasifrovanyText + tabulka[(radek2 + 1)%5][sloupec2]
            else:
                zasifrovanyText = zasifrovanyText + tabulka[radek1][sloupec2]
                zasifrovanyText = zasifrovanyText + tabulka[radek2][sloupec1]

        filtActiveText = ""

        for i in range(len(zasifrovanyText)):
            filtActiveText = filtActiveText + zasifrovanyText[i]
            if(i + 1) % 5 == 0:
                filtActiveText = filtActiveText + " "
        
        self.vyfiltrovanyTextGUI.setText("Vyfiltrovaný text: " + filtrovanyText)
        self.zasifrovanyTextGUI.setText("Zašifrovaný text: " + filtActiveText)
        self.tabulkaGUI.setText("Tabulka: \n" +
                               str(tabulka[0]) + "\n" +
                               str(tabulka[1]) + "\n" +
                               str(tabulka[2]) + "\n" +
                               str(tabulka[3]) + "\n" +
                               str(tabulka[4]))
        
    def desifrovani(self):
        popupError = QMessageBox()
        popupError.setIcon(QMessageBox.Critical)
        popupError.setWindowTitle("Nepodařilo se.")

        klicoveSlovo = self.lineEditKlicoveSlovo.text()

        if klicoveSlovo != "":
            klicoveSlovo = klicoveSlovo.upper()
            klicoveSlovo = self.odstraneniDiakritiky(klicoveSlovo)
            klicoveSlovo = self.odstraneniSpecialZnaku(klicoveSlovo)
            klicoveSlovo = self.odstraneniDuplicity(klicoveSlovo)
            self.lineEditKlicoveSlovo.setText(klicoveSlovo)


            if len(klicoveSlovo)<7:
                popupError.setText("Klíč musí mít aspoň 8 znaků")
                popupError.exec()
                return None
            
            if any(char.isdigit() for char in klicoveSlovo):
                popupError.setText("Klíč nesmí mít číslice")
                popupError.exec()
                return None
        else:
            popupError.setText("Není zadán klíč")
            popupError.exec()
            return None
        
        activeText = self.lineEditTextDesifrovani.text()

        if activeText != "":
            activeText = activeText.replace(" ", "")
            activeText = activeText.upper()
        else:
            popupError.setText("Chybí text pro dešifrování")
            popupError.exec()
            return None
        
        if self.radioButtonCzech.isChecked():
            jazyk = "czech"
        elif self.radioButtonEnglish.isChecked():
            jazyk = "english"

        self.lineEditKlicoveSlovo.setText(klicoveSlovo)

        tabulka = self.vytvoreniTabulky(klicoveSlovo, jazyk)
        duplikaty = self.pripravaTextu(activeText, jazyk)

        desifrovanyText = ""

        for i in duplikaty:
            radek1, sloupec1 = self.najitiPozice(i[0], tabulka)
            radek2, sloupec2 = self.najitiPozice(i[1], tabulka)

            if radek1 == radek2:
                desifrovanyText = desifrovanyText + tabulka[radek1][(sloupec1 - 1)%5]
                desifrovanyText = desifrovanyText + tabulka[radek2][(sloupec2 - 1)%5]
            elif sloupec1 == sloupec2:
                desifrovanyText = desifrovanyText + tabulka[(radek1 - 1)%5][sloupec1]
                desifrovanyText = desifrovanyText + tabulka[(radek2 - 1)%5][sloupec2]
            else:
                desifrovanyText = desifrovanyText + tabulka[radek1][sloupec2]
                desifrovanyText = desifrovanyText + tabulka[radek2][sloupec1]

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

        finalText = ""

        i = 0

        while i < len(desifrovanyText):
            if i != len(desifrovanyText) - 1 and desifrovanyText[i] == "X" and desifrovanyText[i + 1] == "Q":
                finalText = finalText + "X"
                i = i + 2
            elif i < len(desifrovanyText) - 2 and desifrovanyText[i] == desifrovanyText[i + 2] and desifrovanyText[i + 1] == "X":
                finalText = finalText + desifrovanyText[i] + desifrovanyText[i + 2]
                i = i + 3
            elif desifrovanyText[i] == "X" and i == len(desifrovanyText) - 1:
                finalText = finalText + ""
                i = i + 1
            else:
                finalText = finalText + desifrovanyText[i]
                i = i + 1

        self.desifrovanyTextGUI.setText("Dešifrovaný text: " + finalText)
        self.tabulkaGUI.setText("Tabulka: \n" +
                               str(tabulka[0]) + "\n" +
                               str(tabulka[1]) + "\n" +
                               str(tabulka[2]) + "\n" +
                               str(tabulka[3]) + "\n" +
                               str(tabulka[4]))

        
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









        
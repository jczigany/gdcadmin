from datetime import datetime
from PySide2.QtWidgets import QFormLayout, QDialog, QLineEdit, QDialogButtonBox, QCompleter
from PySide2.QtCore import *
from PySide2.QtGui import QRegExpValidator
from database.db import MysqlClient

client = MysqlClient()


class NapidijFormDialog(QDialog):
    """ A fogadott paraméter (table) alapján állítjuk össze a form-ot.
        Lekérdezzük a tábla struktúrát és összerakjuk a mezőnevek listáját,
        kihagyva a Primary mező-nevet. Ezek lesznek a LABEl-ek. A mező értékeket
        szintén egy LIST-ben tárojuk a későbbi feldolgozás lehetővé tétele érdekében"""

    def __init__(self):
        super(NapidijFormDialog, self).__init__()
        self.mezo_nevek = []
        self.mezo_ertekek = []
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        reg_datum = QRegExp('(19[0-9]{2}\\-([0][1-9]|[1][0-2])\\-([0][1-9]|[1-2][0-9]|3[0-1]))|(20[0-9]{2}\\-([0][1-9]|[1][0-2])\\-([0][1-9]|[1-2][0-9]|3[0-1]))')
        datumvalidator = QRegExpValidator(reg_datum)

        jogcim_completer = QCompleter()
        self.jogcim_model = QStringListModel()
        jogcim_completer.setModel(self.jogcim_model)
        self.get_jogcimdata()

        fizmod_completer = QCompleter()
        self.fizmod_model = QStringListModel()
        fizmod_completer.setModel(self.fizmod_model)
        self.get_fizmoddata()

        self.mezo_nevek.append("Dátum")
        self.mezo_nevek.append("Nyugta száma")
        self.mezo_nevek.append("Befizető")
        self.mezo_nevek.append("Jogcím")
        # self.mezo_nevek.append("Év")
        # self.mezo_nevek.append("Hónap")
        self.mezo_nevek.append("Összeg")
        self.mezo_nevek.append("Fizetési mód")
        self.mezo_nevek.append("Megjegyzés")

        for i in range(len(self.mezo_nevek)):
            if (self.mezo_nevek[i] == "Dátum"):
                datum = QLineEdit()
                datum.setText(datetime.today().strftime('%Y-%m-%d'))
                datum.setValidator(datumvalidator)
                self.mezo_ertekek.append(datum)
            if (self.mezo_nevek[i] == "Nyugta száma"):
                nyugta = QLineEdit()
                nyugta.setText("0")
                self.mezo_ertekek.append(nyugta)
            if (self.mezo_nevek[i] == "Befizető"):
                self.befizeto = QLineEdit()
                self.befizeto.setText("Vendég")
                self.mezo_ertekek.append(self.befizeto)
            if (self.mezo_nevek[i] == "Jogcím"):
                self.jogcim = QLineEdit()
                self.jogcim.setCompleter(jogcim_completer)
                self.mezo_ertekek.append(self.jogcim)
            if (self.mezo_nevek[i] == "Összeg"):
                self.osszeg = QLineEdit()
                self.mezo_ertekek.append(self.osszeg)
            if (self.mezo_nevek[i] == "Fizetési mód"):
                self.fizmod = QLineEdit()
                self.fizmod.setCompleter(fizmod_completer)
                self.fizmod.setText("Készpénz")
                self.mezo_ertekek.append(self.fizmod)
            if (self.mezo_nevek[i] == "Megjegyzés"):
                megjegyzes = QLineEdit()
                self.mezo_ertekek.append(megjegyzes)

            self.layout.addRow(f"{self.mezo_nevek[i]}", self.mezo_ertekek[i])

        buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        self.layout.addWidget(buttonbox)

    def get_jogcimdata(self):
        client.cursor.execute("SELECT jogcim FROM jogcim order by jogcim")
        adatok = [list(row)[0] for row in client.cursor.fetchall()]
        self.jogcim_model.setStringList(adatok)

    def get_fizmoddata(self):
        self.fizmod_model.setStringList(["Készpénz", "Átutalás"])

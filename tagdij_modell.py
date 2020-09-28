from datetime import datetime
from PySide2.QtWidgets import QFormLayout, QDialog, QLineEdit, QDialogButtonBox, QCompleter
from PySide2.QtCore import *
from PySide2.QtGui import QRegExpValidator
from database.db import MysqlClient

client = MysqlClient()


class MyFormDialog(QDialog):
    """ A fogadott paraméter (table) alapján állítjuk össze a form-ot.
        Lekérdezzük a tábla struktúrát és összerakjuk a mezőnevek listáját,
        kihagyva a Primary mező-nevet. Ezek lesznek a LABEl-ek. A mező értékeket
        szintén egy LIST-ben tárojuk a későbbi feldolgozás lehetővé tétele érdekében"""

    def __init__(self):
        super(MyFormDialog, self).__init__()
        self.mezo_nevek = []
        self.mezo_ertekek = []
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        reg_ev = QRegExp('202[0-9]{1}')
        evvalidator = QRegExpValidator(reg_ev)
        reg_honap = QRegExp('([0][1-9]|[1][0-2])')
        honapvalidator = QRegExpValidator(reg_honap)
        reg_datum = QRegExp('(19[0-9]{2}\\-([0][1-9]|[1][0-2])\\-([0][1-9]|[1-2][0-9]|3[0-1]))|(20[0-9]{2}\\-([0][1-9]|[1][0-2])\\-([0][1-9]|[1-2][0-9]|3[0-1]))')
        datumvalidator = QRegExpValidator(reg_datum)

        nev_completer = QCompleter()
        self.nev_model = QStringListModel()
        nev_completer.setModel(self.nev_model)
        self.get_nevdata()

        jogcim_completer = QCompleter()
        self.jogcim_model = QStringListModel()
        jogcim_completer.setModel(self.jogcim_model)
        self.get_jogcimdata()

        self.mezo_nevek.append("Dátum")
        self.mezo_nevek.append("Befizető")
        self.mezo_nevek.append("Jogcím")
        self.mezo_nevek.append("Év")
        self.mezo_nevek.append("Hónap")
        self.mezo_nevek.append("Összeg")
        self.mezo_nevek.append("Megjegyzés")

        for i in range(len(self.mezo_nevek)):
            mezo = QLineEdit()
            if (self.mezo_nevek[i] == "Befizető"):
                mezo.setCompleter(nev_completer)
            if (self.mezo_nevek[i] == "Jogcím"):
                mezo.setCompleter(jogcim_completer)
            if (self.mezo_nevek[i] == "Év"):
                mezo.setValidator(evvalidator)
            if (self.mezo_nevek[i] == "Hónap"):
                mezo.setValidator(honapvalidator)
            if (self.mezo_nevek[i] == "Dátum"):
                mezo.setText(datetime.today().strftime('%Y-%m-%d'))
                mezo.setValidator(datumvalidator)
            self.mezo_ertekek.append(mezo)
            self.layout.addRow(f"{self.mezo_nevek[i]}", self.mezo_ertekek[i])

        buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        self.layout.addWidget(buttonbox)

    def get_nevdata(self):
        client.cursor.execute("SELECT concat(vezeteknev, ' ', utonev) as nev FROM members order by nev")
        adatok = [list(row)[0] for row in client.cursor.fetchall()]
        self.nev_model.setStringList(adatok)

    def get_jogcimdata(self):
        client.cursor.execute("SELECT jogcim FROM jogcim order by jogcim")
        adatok = [list(row)[0] for row in client.cursor.fetchall()]
        self.jogcim_model.setStringList(adatok)


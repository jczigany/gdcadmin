from datetime import datetime, date
from PySide2.QtWidgets import QFormLayout, QDialog, QLineEdit, QDialogButtonBox, QCompleter, QDateEdit
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

        fizmod_completer = QCompleter()
        self.fizmod_model = QStringListModel()
        fizmod_completer.setModel(self.fizmod_model)
        self.get_fizmoddata()

        self.mezo_nevek.append("Dátum")
        self.mezo_nevek.append("Nyugta száma")
        self.mezo_nevek.append("Befizető")
        self.mezo_nevek.append("Jogcím")
        self.mezo_nevek.append("Év")
        self.mezo_nevek.append("Hónap")
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
                #datum.setValidator(datumvalidator)
                self.mezo_ertekek.append(nyugta)
            if (self.mezo_nevek[i] == "Befizető"):
                self.befizeto = QLineEdit()
                self.befizeto.setCompleter(nev_completer)
                self.mezo_ertekek.append(self.befizeto)
                self.befizeto.editingFinished.connect(self.befizetoselected)
            if (self.mezo_nevek[i] == "Jogcím"):
                self.jogcim = QLineEdit()
                self.jogcim.setCompleter(jogcim_completer)
                self.mezo_ertekek.append(self.jogcim)
            if (self.mezo_nevek[i] == "Év"):
                ev = QLineEdit()
                ev.setValidator(evvalidator)
                self.mezo_ertekek.append(ev)
            if (self.mezo_nevek[i] == "Hónap"):
                honap = QLineEdit()
                honap.setValidator(honapvalidator)
                self.mezo_ertekek.append(honap)
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

    def get_nevdata(self):
        client.cursor.execute("SELECT concat(vezeteknev, ' ', utonev) as nev FROM members order by nev")
        adatok = [list(row)[0] for row in client.cursor.fetchall()]
        self.nev_model.setStringList(adatok)

    def get_jogcimdata(self):
        client.cursor.execute("SELECT jogcim FROM jogcim order by jogcim")
        adatok = [list(row)[0] for row in client.cursor.fetchall()]
        self.jogcim_model.setStringList(adatok)

    def get_fizmoddata(self):
        self.fizmod_model.setStringList(["Készpénz", "Átutalás"])

    def befizetoselected(self):
        """ Itt lehet majd kiértékelni, hogy db-ben benne van-e a befizető. Ha igen, akkor a születési dátum
        alapján a jogcím (Tagdíj/Ifjúsági tagdíj) illetve az összeg (1.500/3.000) automatikusan kitölthető"""
        print(self.befizeto.text())
        if (self.befizeto.text() in self.nev_model.stringList()):
            client.cursor.execute(f"SELECT szuletesi_ido FROM members WHERE CONCAT(vezeteknev, ' ', utonev)= '{self.befizeto.text()}'")
            adatok = [list(row) for row in client.cursor.fetchall()]
            # Ha 12 évnél fiatalabb
            if ((date.today() - adatok[0][0]).days < 4380):
                print("Ingyenes")
                self.jogcim.setText("Ingyenes")
                self.osszeg.setText("0")
            # Ha 14 évnél idősebb
            elif ((date.today() - adatok[0][0]).days > 5110):
                print("Felnőtt")
                self.jogcim.setText("Tagdíj")
                self.osszeg.setText("3000")
            # Egyébként (Ha 12-14 között van)
            else:
                print("Ifjúsági")
                self.jogcim.setText("Ifjúsági tagdíj")
                self.osszeg.setText("1500")

        # else:
        #     print("Nincs db-ben")
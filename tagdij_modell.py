# from datetime import datetime
from PySide2.QtWidgets import QFormLayout, QDialog, QLineEdit, QDialogButtonBox, QCompleter, QComboBox
from PySide2.QtCore import *
from PySide2.QtGui import QRegExpValidator
from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel

db = QSqlDatabase.addDatabase('QMYSQL')
db.setHostName('localhost')
db.setDatabaseName('gdcadmindb')
db.setUserName('gdcadminuser')
db.setPassword('GdcAdmin1968')

if not db.open():
    QMessageBox.critical(
        None,
        "App Name - Error!",
        "Database Error: %s" % db.lastError().text(),
    )
    sys.exit(1)


class MyFormDialog(QDialog):
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

        self.jogcim_completer = QCompleter()
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
                datum.setText(QDate.currentDate().toString("yyyy-MM-dd"))
                datum.setValidator(datumvalidator)
                self.mezo_ertekek.append(datum)
            if (self.mezo_nevek[i] == "Nyugta száma"):
                nyugta = QLineEdit()
                nyugta.setText("0")
                self.mezo_ertekek.append(nyugta)
            if (self.mezo_nevek[i] == "Befizető"):
                self.befizeto = QComboBox()
                self.get_nevdata()
                self.befizeto.currentIndexChanged.connect(self.befizetoselected)
                self.mezo_ertekek.append(self.befizeto)
            if (self.mezo_nevek[i] == "Jogcím"):
                self.jogcim = QLineEdit()
                self.jogcim.setCompleter(self.jogcim_completer)
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
        nevlista_model = QSqlQueryModel()
        query = QSqlQuery("SELECT concat(vezeteknev, ' ', utonev) as nev FROM members order by nev", db=db)
        nevlista_model.setQuery(query)
        self.befizeto.setModel(nevlista_model)

    def get_jogcimdata(self):
        jogcimek_model = QSqlQueryModel()
        query = QSqlQuery("SELECT jogcim FROM jogcim order by jogcim", db=db)
        jogcimek_model.setQuery(query)
        self.jogcim_completer.setModel(jogcimek_model)

    def get_fizmoddata(self):
        self.fizmod_model.setStringList(["Készpénz", "Átutalás"])

    def befizetoselected(self):
        """ Itt lehet majd kiértékelni, hogy db-ben benne van-e a befizető. Ha igen, akkor a születési dátum
        alapján a jogcím (Tagdíj/Ifjúsági tagdíj) illetve az összeg (1.500/3.000) automatikusan kitölthető"""
        befizeto_model = QSqlQueryModel()
        query = QSqlQuery(f"SELECT szuletesi_ido FROM members WHERE CONCAT(vezeteknev, ' ', utonev)= '{self.befizeto.currentText()}'", db=db)
        befizeto_model.setQuery(query)
        # Ha 12 évnél fiatalabb
        if ((befizeto_model.record(0).value(0).daysTo(QDate.currentDate())) < 4380):
            self.jogcim.setText("Ingyenes")
            self.osszeg.setText("0")
        # Ha 14 évnél idősebb
        elif ((befizeto_model.record(0).value(0).daysTo(QDate.currentDate())) > 5110):
            self.jogcim.setText("Tagdíj")
            self.osszeg.setText("3000")
        # Egyébként (Ha 12-14 között van)
        else:
            self.jogcim.setText("Ifjúsági tagdíj")
            self.osszeg.setText("1500")

from PySide2.QtWidgets import QFormLayout, QDialog, QLineEdit, QDialogButtonBox, QCompleter
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

class KiadasFormDialog(QDialog):
    def __init__(self):
        super(KiadasFormDialog, self).__init__()
        self.mezo_nevek = []
        self.mezo_ertekek = []
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        reg_datum = QRegExp('(19[0-9]{2}\\-([0][1-9]|[1][0-2])\\-([0][1-9]|[1-2][0-9]|3[0-1]))|(20[0-9]{2}\\-([0][1-9]|[1][0-2])\\-([0][1-9]|[1-2][0-9]|3[0-1]))')
        datumvalidator = QRegExpValidator(reg_datum)

        self.kedvezmenyezett_completer = QCompleter()
        self.get_kedvezmenyezettdata()

        fizmod_completer = QCompleter()
        self.fizmod_model = QStringListModel()
        fizmod_completer.setModel(self.fizmod_model)
        self.get_fizmoddata()

        self.mezo_nevek.append("Dátum")
        self.mezo_nevek.append("Bizonylat száma")
        self.mezo_nevek.append("Kedvezményezett")
        self.mezo_nevek.append("Jogcím")
        self.mezo_nevek.append("Összeg")
        self.mezo_nevek.append("Fizetési mód")
        self.mezo_nevek.append("Megjegyzés")

        for i in range(len(self.mezo_nevek)):
            if (self.mezo_nevek[i] == "Dátum"):
                datum = QLineEdit()
                datum.setText(QDate.currentDate().toString("yyyy-MM-dd"))
                datum.setValidator(datumvalidator)
                self.mezo_ertekek.append(datum)
            if (self.mezo_nevek[i] == "Bizonylat száma"):
                nyugta = QLineEdit()
                nyugta.setText("0")
                self.mezo_ertekek.append(nyugta)
            if (self.mezo_nevek[i] == "Kedvezményezett"):
                self.kedvezmenyezett = QLineEdit()
                self.kedvezmenyezett.setCompleter(self.kedvezmenyezett_completer)
                # Ide kellene egy QCompleter
                # self.befizeto.setText("Vendég")
                self.mezo_ertekek.append(self.kedvezmenyezett)
            if (self.mezo_nevek[i] == "Jogcím"):
                self.jogcim = QLineEdit()
                # self.jogcim.setCompleter(self.jogcim_completer)
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

    def get_kedvezmenyezettdata(self):
        kedvezm_model = QSqlQueryModel()
        query = QSqlQuery("SELECT megnevezes FROM kedvezmenyezettek order by megnevezes", db=db)
        kedvezm_model.setQuery(query)
        self.kedvezmenyezett_completer.setModel(kedvezm_model)

    def get_fizmoddata(self):
        self.fizmod_model.setStringList(["Készpénz", "Átutalás"])

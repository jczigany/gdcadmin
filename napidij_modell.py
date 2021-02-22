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
        # Itt nincs értelme év, hónap megadásnak, ezeket implicit 0-ra állítjuk
        # self.mezo_nevek.append("Év")
        # self.mezo_nevek.append("Hónap")
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
                self.befizeto = QLineEdit()
                self.befizeto.setText("Vendég")
                self.mezo_ertekek.append(self.befizeto)
            if (self.mezo_nevek[i] == "Jogcím"):
                self.jogcim = QLineEdit()
                self.jogcim.setCompleter(self.jogcim_completer)
                self.jogcim.editingFinished.connect(self.jogcim_selected)
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
        jogcimek_model = QSqlQueryModel()
        query = QSqlQuery("SELECT jogcim FROM jogcim order by jogcim", db=db)
        jogcimek_model.setQuery(query)
        self.jogcim_completer.setModel(jogcimek_model)

    def get_fizmoddata(self):
        self.fizmod_model.setStringList(["Készpénz", "Átutalás"])

    def jogcim_selected(self):
        napidij_model = QSqlQueryModel()
        query = QSqlQuery("SELECT kulcs, ertek FROM settings WHERE kulcs LIKE '%napidij%'")
        napidij_model.setQuery(query)

        for i in range(napidij_model.rowCount()):
            if (napidij_model.record(i).value(0) == 'ar_ifjusagi_napidij') and (self.jogcim.text() == 'Ifjúsági napidíj'):
                self.osszeg.setText(str(napidij_model.record(i).value(1)))
            if (napidij_model.record(i).value(0) == 'ar_napidij') and (self.jogcim.text() == 'Napidíj'):
                self.osszeg.setText(str(napidij_model.record(i).value(1)))
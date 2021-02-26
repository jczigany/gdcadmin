from PySide2.QtWidgets import QFormLayout, QDialog, QLineEdit, QDialogButtonBox, QCompleter, QComboBox, QTextEdit
from PySide2.QtCore import *
from PySide2.QtGui import QRegExpValidator
from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlTableModel

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
        self.havidij = 0

        reg_ev = QRegExp('202[0-9]{1}')
        evvalidator = QRegExpValidator(reg_ev)
        reg_honap = QRegExp('([0][1-9]|[1][0-2])')
        honapvalidator = QRegExpValidator(reg_honap)
        reg_datum = QRegExp('(19[0-9]{2}\\-([0][1-9]|[1][0-2])\\-([0][1-9]|[1-2][0-9]|3[0-1]))|(20[0-9]{2}\\-([0][1-9]|[1][0-2])\\-([0][1-9]|[1-2][0-9]|3[0-1]))')
        datumvalidator = QRegExpValidator(reg_datum)

        fizmod_completer = QCompleter()
        self.fizmod_model = QStringListModel()
        fizmod_completer.setModel(self.fizmod_model)
        self.get_fizmoddata()

        self.mezo_nevek.append("Dátum")
        self.mezo_nevek.append("Nyugta száma")
        self.mezo_nevek.append("Befizető")
        self.mezo_nevek.append("Jogcím")
        self.mezo_nevek.append("Hónapok száma")
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
                self.jogcim.setText("Tagdíj")
                self.jogcim.setDisabled(True)
                self.mezo_ertekek.append(self.jogcim)
            if (self.mezo_nevek[i] == "Hónapok száma"):
                self.honapok = QLineEdit()
                self.honapok.setText("1")
                self.honapok.editingFinished.connect(self.honapszam_valtozott)
                self.mezo_ertekek.append(self.honapok)
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
        self.info_ablak = QTextEdit()
        self.info_ablak.setMaximumHeight(50)
        self.info_ablak.append("Az utolsó rendezett időszak:")
        self.layout.addWidget(self.info_ablak)

    def get_nevdata(self):
        nevlista_model = QSqlQueryModel()
        query = QSqlQuery("SELECT concat(vezeteknev, ' ', utonev) as nev FROM members order by nev", db=db)
        nevlista_model.setQuery(query)
        self.befizeto.setModel(nevlista_model)

    # def get_jogcimdata(self):
    #     jogcimek_model = QSqlQueryModel()
    #     query = QSqlQuery("SELECT jogcim FROM jogcim order by jogcim", db=db)
    #     jogcimek_model.setQuery(query)
    #     # self.jogcim_completer.setModel(jogcimek_model)
    #     self.jogcim.setModel(jogcimek_model)

    def get_fizmoddata(self):
        self.fizmod_model.setStringList(["Készpénz", "Átutalás"])

    def befizetoselected(self):
        """ Itt lehet majd kiértékelni, hogy db-ben benne van-e a befizető. Ha igen, akkor a születési dátum
        alapján a jogcím (Tagdíj/Ifjúsági tagdíj) illetve az összeg (1.500/3.000) automatikusan kitölthető"""
        befizeto_model = QSqlQueryModel()
        query = QSqlQuery(f"SELECT szuletesi_ido FROM members WHERE CONCAT(vezeteknev, ' ', utonev)= '{self.befizeto.currentText()}'", db=db)
        befizeto_model.setQuery(query)
        tagdij_model = QSqlQueryModel()
        query = QSqlQuery("SELECT kulcs, ertek FROM settings WHERE kulcs LIKE '%tagdij%'")
        tagdij_model.setQuery(query)
        # Ha 12 évnél fiatalabb
        if ((befizeto_model.record(0).value(0).daysTo(QDate.currentDate())) < 4380):
            for i in range(tagdij_model.rowCount()):
                if tagdij_model.record(i).value(0) == 'ar_gyermek_tagdij':
                    self.jogcim.setText("Ingyenes")
                    self.havidij = tagdij_model.record(i).value(1)
                    self.osszeg.setText(str(self.havidij))
        # Ha 14 évnél idősebb
        elif ((befizeto_model.record(0).value(0).daysTo(QDate.currentDate())) > 5110):
            for i in range(tagdij_model.rowCount()):
                if tagdij_model.record(i).value(0) == 'ar_tagdij':
                    self.jogcim.setText("Tagdíj")
                    self.havidij = tagdij_model.record(i).value(1)
                    self.osszeg.setText(str(int(self.havidij) * int(self.honapok.text())))
        # Egyébként (Ha 12-14 között van)
        else:
            for i in range(tagdij_model.rowCount()):
                if tagdij_model.record(i).value(0) == 'ar_ifjusagi_tagdij':
                    self.jogcim.setText("Ifjúsági tagdíj")
                    self.havidij = tagdij_model.record(i).value(1)
                    self.osszeg.setText(str(int(self.havidij) * int(self.honapok.text())))
        self.infoablak_frissit()

    def honapszam_valtozott(self):
        self.osszeg.setText(str(int(self.havidij) * int(self.honapok.text())))

    def infoablak_frissit(self):
        befizeto = self.mezo_ertekek[2].currentText()
        befizeto_id_model = QSqlQueryModel()
        query = QSqlQuery(f"SELECT id FROM members where concat(vezeteknev, ' ', utonev) = '{befizeto}'", db=db)
        befizeto_id_model.setQuery(query)
        befizeto_id = int(befizeto_id_model.record(0).value(0))
        utolso_model = QSqlQueryModel()
        query = QSqlQuery(f"select ev, honap from tagdijak where member_id = {int(befizeto_id)} order by ev desc, honap desc limit 1", db=db)
        utolso_model.setQuery(query)
        self.info_ablak.clear()
        if utolso_model.record(0).isNull(0):
            self.info_ablak.append("Az utolsó rendezett időszak:")
            self.info_ablak.append("Még nincs tagdíj fizetve!")
        else:
            self.info_ablak.append("Az utolsó rendezett időszak:")
            self.info_ablak.append(str(utolso_model.record(0).value(0)) + "-" + str(utolso_model.record(0).value(1)))

def add_tagdij(self):
    self.tagdij_form_window = MyFormDialog()
    self.tagdij_form_window.setWindowTitle("Tagdíj befizetés")
    self.tagdij_form_window.show()
    model = QSqlTableModel()
    model.setTable("kassza")
    record = model.record()
    record.remove(record.indexOf('id'))

    if self.tagdij_form_window.exec_():
        befizetett_honap = self.tagdij_form_window.mezo_ertekek.pop(4).text()
        befizeto = self.tagdij_form_window.mezo_ertekek[2].currentText()
        befizeto_id_model = QSqlQueryModel()
        query = QSqlQuery(f"SELECT id FROM members where concat(vezeteknev, ' ', utonev) = '{befizeto}'", db=db)
        befizeto_id_model.setQuery(query)
        befizeto_id = int(befizeto_id_model.record(0).value(0))

        for i in range(len(self.tagdij_form_window.mezo_ertekek)):
            if self.tagdij_form_window.mezo_ertekek[i].__class__.__name__ == 'QLineEdit':
                record.setValue(i, self.tagdij_form_window.mezo_ertekek[i].text())
            else:
                record.setValue(i, self.tagdij_form_window.mezo_ertekek[i].currentText())
        if model.insertRecord(-1, record):
            model.submitAll()
        else:
            db.rollback()


        tagdijak_model = QSqlQueryModel()
        tagdij_model = QSqlTableModel()
        tagdij_model.setTable("tagdijak")
        for i in range(int(befizetett_honap)):
            query = QSqlQuery(
                f"SELECT ev, honap FROM `tagdijak` WHERE member_id={befizeto_id} order by ev desc, honap desc limit 1",
                db=db)
            tagdijak_model.setQuery(query)
            record2 = tagdij_model.record()
            if tagdijak_model.record(0).isNull(0):
                record2.setValue(0, int(befizeto_id_model.record(0).value(0)))
                record2.setValue(1, int(record.value(0)[:4]))  # Ide kell az év
                record2.setValue(2, int(record.value(0)[5:7]))  # Ide kell a hónap
                record2.setValue(3, int(int(record.value(4)) / int(befizetett_honap)))
                if tagdij_model.insertRecord(-1, record2):
                    tagdij_model.submitAll()
                else:
                    db.rollback()
            else:
                if int(tagdijak_model.record(0).value(1)) <= 11:
                    record2.setValue(0, int(befizeto_id_model.record(0).value(0)))
                    record2.setValue(1, int(tagdijak_model.record(0).value(0)))
                    record2.setValue(2, int(tagdijak_model.record(0).value(1)) + 1)
                    record2.setValue(3, int(int(record.value(4)) / int(befizetett_honap)))
                    if tagdij_model.insertRecord(-1, record2):
                        tagdij_model.submitAll()
                    else:
                        db.rollback()
                else:
                    record2.setValue(0, int(befizeto_id_model.record(0).value(0)))
                    record2.setValue(1, int(tagdijak_model.record(0).value(0)) + 1)
                    record2.setValue(2, 1)
                    record2.setValue(3, int(int(record.value(4)) / int(befizetett_honap)))
                    if tagdij_model.insertRecord(-1, record2):
                        tagdij_model.submitAll()
                    else:
                        db.rollback()

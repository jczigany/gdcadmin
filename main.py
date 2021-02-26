from PySide2.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout
from PySide2.QtCore import *
from menus import create_menus
from tagdij_modell import MyFormDialog, add_tagdij
from berlet_modell import BerletFormDialog
from napidij_modell import NapidijFormDialog
from adomany_modell import AdomanyFormDialog
from egyeb_befiz_modell import EgyebBefizFormDialog
from kiadas_model import KiadasFormDialog
from members import ManageMembers
from settings import ManageSettings
from PySide2.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery, QSqlQueryModel

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


class AppWindows(QMainWindow):
    def __init__(self):
        super(AppWindows, self).__init__()
        self.setWindowTitle("Admin for G.D.C powered by Jcigi")
        self.resize(1000,800)
        widget = QWidget()
        main_layout = QVBoxLayout()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        # A menus.py definiálja a menüpontokat
        create_menus(self)

    @Slot()
    def exit_app(self):
        QApplication.quit()

    @Slot()
    def new_member(self):
        manage_members_window = ManageMembers(self)
        manage_members_window.show()

    @Slot()
    def new_tagdij(self):
        add_tagdij(self)

    @Slot()
    def new_berlet(self):
        self.berlet_form_window = BerletFormDialog()
        self.berlet_form_window.setWindowTitle("Bérlet vásárlás")
        self.berlet_form_window.show()
        model = QSqlTableModel()
        model.setTable("kassza")
        record = model.record()
        record.remove(record.indexOf('id'))

        if self.berlet_form_window.exec_():
            for i in range(len(self.berlet_form_window.mezo_ertekek)):
                record.setValue(i, self.berlet_form_window.mezo_ertekek[i].text())
            if model.insertRecord(-1, record):
                model.submitAll()
            else:
                db.rollback()


    @Slot()
    def new_napidij(self):
        self.napidij_form_window = NapidijFormDialog()
        self.napidij_form_window.setWindowTitle("Napidíj befizetés")
        self.napidij_form_window.show()
        model = QSqlTableModel()
        model.setTable("kassza")
        record = model.record()
        record.remove(record.indexOf('id'))

        if self.napidij_form_window.exec_():
            mezo_rekord = []
            for i in range(len(self.napidij_form_window.mezo_ertekek)):
                mezo_rekord.append(self.napidij_form_window.mezo_ertekek[i].text())

            for i in range(len(mezo_rekord)):
                record.setValue(i, mezo_rekord[i])
                if model.insertRecord(-1, record):
                    model.submitAll()
                else:
                    db.rollback()

    @Slot()
    def new_adomany(self):
        self.adomany_form_window = AdomanyFormDialog()
        self.adomany_form_window.setWindowTitle("Adomány befizetés")
        self.adomany_form_window.show()
        model = QSqlTableModel()
        model.setTable("kassza")
        record = model.record()
        record.remove(record.indexOf('id'))

        if self.adomany_form_window.exec_():
            mezo_rekord = []
            for i in range(len(self.adomany_form_window.mezo_ertekek)):
                mezo_rekord.append(self.adomany_form_window.mezo_ertekek[i].text())

            for i in range(len(mezo_rekord)):
                record.setValue(i, mezo_rekord[i])
                if model.insertRecord(-1, record):
                    model.submitAll()
                else:
                    db.rollback()

    @Slot()
    def new_egyebfiz(self):
        self.egyebbefiz_form_window = EgyebBefizFormDialog()
        self.egyebbefiz_form_window.setWindowTitle("Egyéb befizetés")
        self.egyebbefiz_form_window.show()
        model = QSqlTableModel()
        model.setTable("kassza")
        record = model.record()
        record.remove(record.indexOf('id'))

        if self.egyebbefiz_form_window.exec_():
            mezo_rekord = []
            for i in range(len(self.egyebbefiz_form_window.mezo_ertekek)):
                mezo_rekord.append(self.egyebbefiz_form_window.mezo_ertekek[i].text())

            for i in range(len(mezo_rekord)):
                record.setValue(i, mezo_rekord[i])
                if model.insertRecord(-1, record):
                    model.submitAll()
                else:
                    db.rollback()

    @Slot()
    def settings_slot(self):
        manage_settings_window = ManageSettings(self)
        manage_settings_window.show()

    @Slot()
    def new_kiadas(self):
        self.kiadas_form_window = KiadasFormDialog()
        self.kiadas_form_window.setWindowTitle("Új kiadás rögzítése")
        self.kiadas_form_window.show()
        model = QSqlTableModel()
        model.setTable("kassza")
        record = model.record()
        record.remove(record.indexOf('id'))

        if self.kiadas_form_window.exec_():
            mezo_rekord = []
            for i in range(len(self.kiadas_form_window.mezo_ertekek)):
                if i != 4:
                    mezo_rekord.append(self.kiadas_form_window.mezo_ertekek[i].text())
                else:
                    mezo_rekord.append(int(self.kiadas_form_window.mezo_ertekek[i].text()) * -1)

            for i in range(len(mezo_rekord)):
                record.setValue(i, mezo_rekord[i])
                if model.insertRecord(-1, record):
                    model.submitAll()
                else:
                    db.rollback()

if __name__ == '__main__':
    app = QApplication([])
    win = AppWindows()
    win.show()
    app.exec_()

from database.db import MysqlClient
from PySide2.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout
from PySide2.QtCore import *
from menus import create_menus
from tagdij_modell import MyFormDialog
from berlet_modell import BerletFormDialog
from napidij_modell import NapidijFormDialog
from adomany_modell import AdomanyFormDialog
from egyeb_befiz_modell import EgyebBefizFormDialog
from members import ManageMembers
from settings import ManageSettings
from PySide2.QtSql import QSqlDatabase, QSqlTableModel


client = MysqlClient()

class AppWindows(QMainWindow):
    def __init__(self):
        super(AppWindows, self).__init__()
        self.setWindowTitle("Admin for G.D.C powered by Jcigi")
        self.resize(1000,800)
        # self.showMaximized()
        widget = QWidget()
        main_layout = QVBoxLayout()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        # A menus.py definiálja a menüpontokat
        create_menus(self)

        self.client = MysqlClient()

    @Slot()
    def exit_app(self):
        QApplication.quit()

    @Slot()
    def new_member(self):
        manage_members_window = ManageMembers(self)
        manage_members_window.show()

    @Slot()
    def new_tagdij(self):
        self.tagdij_form_window = MyFormDialog()
        self.tagdij_form_window.setWindowTitle("Tagdíj befizetés")
        self.tagdij_form_window.show()
        if self.tagdij_form_window.exec_():
            mezo_rekord = [0]

            for i in range(len(self.tagdij_form_window.mezo_ertekek)):
                if self.tagdij_form_window.mezo_ertekek[i].__class__.__name__ == 'QLineEdit':
                    mezo_rekord.append(self.tagdij_form_window.mezo_ertekek[i].text())
                else:
                    mezo_rekord.append(self.tagdij_form_window.mezo_ertekek[i].currentText())
            insert_id = client.insert_rekord("kassza", mezo_rekord)

    @Slot()
    def new_berlet(self):
        self.berlet_form_window = BerletFormDialog()
        self.berlet_form_window.setWindowTitle("Bérlet vásárlás")
        self.berlet_form_window.show()
        if self.berlet_form_window.exec_():
            mezo_rekord = [0]

            for i in range(len(self.berlet_form_window.mezo_ertekek)):
                mezo_rekord.append(self.berlet_form_window.mezo_ertekek[i].text())

            insert_id = client.insert_rekord("kassza", mezo_rekord)

    @Slot()
    def new_napidij(self):
        self.napidij_form_window = NapidijFormDialog()
        self.napidij_form_window.setWindowTitle("Napidíj befizetés")
        self.napidij_form_window.show()
        if self.napidij_form_window.exec_():
            mezo_rekord = [0]
            for i in range(len(self.napidij_form_window.mezo_ertekek)):
                mezo_rekord.append(self.napidij_form_window.mezo_ertekek[i].text())
            mezo_rekord.insert(5, "0")
            mezo_rekord.insert(6, "0")
            print(mezo_rekord)

            insert_id = client.insert_rekord("kassza", mezo_rekord)

    @Slot()
    def new_adomany(self):
        self.adomany_form_window = AdomanyFormDialog()
        self.adomany_form_window.setWindowTitle("Adomány befizetés")
        self.adomany_form_window.show()
        if self.adomany_form_window.exec_():
            mezo_rekord = [0]
            for i in range(len(self.adomany_form_window.mezo_ertekek)):
                mezo_rekord.append(self.adomany_form_window.mezo_ertekek[i].text())
            mezo_rekord.insert(5, "0")
            mezo_rekord.insert(6, "0")
            print(mezo_rekord)

            insert_id = client.insert_rekord("kassza", mezo_rekord)

    @Slot()
    def new_egyebfiz(self):
        self.egyebbefiz_form_window = EgyebBefizFormDialog()
        self.egyebbefiz_form_window.setWindowTitle("Egyéb befizetés")
        self.egyebbefiz_form_window.show()
        if self.egyebbefiz_form_window.exec_():
            mezo_rekord = [0]
            for i in range(len(self.egyebbefiz_form_window.mezo_ertekek)):
                mezo_rekord.append(self.egyebbefiz_form_window.mezo_ertekek[i].text())
            mezo_rekord.insert(5, "0")
            mezo_rekord.insert(6, "0")
            print(mezo_rekord)

            insert_id = client.insert_rekord("kassza", mezo_rekord)

    @Slot()
    def settings_slot(self):
        manage_settings_window = ManageSettings(self)
        manage_settings_window.show()

if __name__ == '__main__':
    app = QApplication([])
    # win = MainWindow()
    win = AppWindows()
    win.show()
    app.exec_()

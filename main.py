from database.db import MysqlClient
from PySide2.QtWidgets import QMainWindow, QTableView, QWidget, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, \
    QFormLayout, QDialog, QLineEdit, QDialogButtonBox
from PySide2.QtCore import *
from menus import create_menus
from tagdij_modell import MyFormDialog
from members import manageMembers

import sys

client = MysqlClient()

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
        # create_slots(self)
        create_menus(self)

        self.client = MysqlClient()

    @Slot()
    # def exit_app(self, checked):
    def exit_app(self):
        QApplication.quit()

    @Slot()
    def new_member(self):
        print("Új csapattag dialog")
        manage_members_window = manageMembers(self)
        # self.resize(600,400)
        manage_members_window.show()

    @Slot()
    def new_tagdij(self):
        print("Új Tagdíj dialog")
        self.form_window = MyFormDialog()
        self.form_window.setWindowTitle("Tagdíj befizetés")
        self.form_window.show()
        if self.form_window.exec_():
            mezo_rekord = [0]

            for i in range(len(self.form_window.mezo_ertekek)):
                mezo_rekord.append(self.form_window.mezo_ertekek[i].text())

            insert_id = client.insert_rekord("kassza", mezo_rekord)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    # win = MainWindow()
    win = AppWindows()
    win.show()
    app.exec_()
    # print('\n'.join(repr(w) for w in app.allWidgets()))

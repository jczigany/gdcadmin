from database.db import MysqlClient
from PySide2.QtWidgets import QMainWindow, QTableView, QWidget, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, \
    QFormLayout, QDialog, QLineEdit, QDialogButtonBox
from PySide2.QtCore import *
from menus import create_menus
from teams import manageTeams
from members import manageMembers

import sys

client = MysqlClient()

class AppWindows(QMainWindow):
    def __init__(self):
        super(AppWindows, self).__init__()
        self.setWindowTitle("Admin for G.D.C powered by Jcigi")
        self.resize(800,600)
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
    def new_team(self):
        print("Új Csapat dialog")
        maname_tems_window = manageTeams(self)
        maname_tems_window.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    # win = MainWindow()
    win = AppWindows()
    win.show()
    app.exec_()
    # print('\n'.join(repr(w) for w in app.allWidgets()))

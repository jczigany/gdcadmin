from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QMainWindow, QTableView, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, \
    QAction, QSpacerItem, QSizePolicy, QMessageBox
from PySide2.QtCore import *
import sys
from PySide2.QtSql import QSqlDatabase, QSqlTableModel

db = QSqlDatabase.addDatabase('QMYSQL')
db.setHostName('localhost')
db.setDatabaseName('gdcadmindb')
db.setUserName('gdcadminuser')
db.setPassword('GdcAdmin1968')

from members_modell import TableModel
from database.db import MysqlClient
import pyexcel as p

if not db.open():
    QMessageBox.critical(
        None,
        "App Name - Error!",
        "Database Error: %s" % db.lastError().text(),
    )
    sys.exit(1)

class manageMembers(QMainWindow):
    def __init__(self):
        super(manageMembers, self).__init__()
        self.setWindowTitle("Tagok kezelése")
        widget = QWidget()
        main_layout = QHBoxLayout()
        widget.setLayout(main_layout)

        self.setCentralWidget(widget)
        # self.client = MysqlClient()
        self.table_view = QTableView()      #####################################
        # self.model = TableModel(self.table_name, fejlec)
        self.model = QSqlTableModel(db=db)  #####################################
        # a megjelenített tábla neve
        # self.table_name = "members"
        self.table_view.setModel(self.model)####################################
        self.model.setTable("members")      ####################################
        self.model.select()                 ####################################
        main_layout.addWidget(self.table_view)
        ####fejlec = ['id', "Vezetéknév", "Utónév", "Született", "Ir.szám", "Helység", "Cím", "Telefon", "E-mail",
        ####          "Tagság kezdete", 'Aktív']

        # self.model = TableModel(self.table_name)
        # print(self.model)

        ###self.table_view.setModel(self.model)
        ####self.table_view.setSortingEnabled(True)
        # Az első oszlop (id) elrejtése
        ####self.table_view.hideColumn(0)
        ####self.table_view.resizeColumnsToContents()

        gomb_layout = QVBoxLayout()
        main_layout.addLayout(gomb_layout)

        self.delete_button = QPushButton("&Tag törlése")
        self.add_button = QPushButton("&Új tag")
        self.modify_button = QPushButton("Tag &módosítása")

        gomb_layout.addWidget(self.delete_button)
        gomb_layout.addWidget(self.add_button)
        gomb_layout.addWidget(self.modify_button)
        self.space = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gomb_layout.addItem(self.space)

        # self.resize(320, 200)
        self.setFixedSize(1000, 800)
        # self.showMaximized()
        # self.setWindowFlags(Qt.Window|Qt.WindowTitleHint)
        tb = self.addToolBar("File")

        exit = QAction(QIcon("images/door--arrow.png"), "Kilépés", self)
        tb.addAction(exit)

        excel = QAction(QIcon("images/excel.png"), "Excel", self)
        tb.addAction(excel)

        tb.actionTriggered[QAction].connect(self.toolbarpressed)

        # self.delete_button.clicked.connect(lambda: self.model.delete(self.table_view.selectedIndexes()[0]))
        self.delete_button.clicked.connect(self.tag_torles)
        ###self.add_button.clicked.connect(self.model.add)
        self.modify_button.clicked.connect(self.tag_modositas)

    def tag_torles(self):
        if len(self.table_view.selectedIndexes()) > 0:
            self.model.delete(self.table_view.selectedIndexes()[0])
        else:
            reply = QMessageBox.question(None, 'Hiba!', 'Törlés előtt jelöljön ki egy sort!', QMessageBox.Ok)

    def tag_modositas(self):
        if len(self.table_view.selectedIndexes()) > 0:
            self.model.modify(self.table_view.selectedIndexes()[0])
        else:
            reply = QMessageBox.question(None, 'Hiba!', 'Módosítás előtt jelöljön ki egy sort!', QMessageBox.Ok)

    def toolbarpressed(self, a):
        # print("Pressed:", a.text())
        if a.text() == "Kilépés":
            self.close()
        if a.text() == "Excel":
            # print("Indulhat az excel exportálás")
            self.adatok = self.client.get_all(self.table_name)
            self._data = self.adatok[0]
            # print(self._data)
            p.save_as(array=self._data, dest_file_name="tagok.xlsx")

app = QApplication(sys.argv)
window = manageMembers()
window.show()
app.exec_()
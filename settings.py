import sys
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMainWindow, QTableView, QWidget, QSpacerItem, QPushButton, QVBoxLayout, QHBoxLayout, QAction, QSizePolicy, QMessageBox
from PySide2.QtSql import QSqlDatabase, QSqlTableModel
from PySide2.QtCore import *

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


class ManageSettings(QMainWindow):
    def __init__(self, parent):
        super(ManageSettings, self).__init__(parent)
        self.setWindowTitle("Paraméterek kezelése")
        widget = QWidget()
        main_layout = QHBoxLayout()
        widget.setLayout(main_layout)

        self.setCentralWidget(widget)
        self.table_view = QTableView()
        main_layout.addWidget(self.table_view)

        self.model = QSqlTableModel(db=db)
        self.model.setTable("settings")
        self.model.select()
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.setHeaderData(1, Qt.Horizontal, "Paraméter")
        self.model.setHeaderData(2, Qt.Horizontal, "Érték")

        self.table_view.setModel(self.model)
        self.table_view.setSortingEnabled(True)
        self.table_view.hideColumn(0)
        self.table_view.resizeColumnsToContents()

        self.model.dataChanged.connect(self.valtozott)
        gomb_layout = QVBoxLayout()
        main_layout.addLayout(gomb_layout)

        self.apply_button = QPushButton("Módosítások alkalmazása")
        self.cancel_button = QPushButton("Módosítások elvetése")

        gomb_layout.addWidget(self.apply_button)
        gomb_layout.addWidget(self.cancel_button)

        self.space = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gomb_layout.addItem(self.space)

        self.setFixedSize(400, 600)
        tb = self.addToolBar("File")

        exit = QAction(QIcon("images/door--arrow.png"), "Kilépés", self)
        tb.addAction(exit)

        tb.actionTriggered[QAction].connect(self.toolbarpressed)

        self.apply_button.clicked.connect(self.valtozas_mentese)
        self.cancel_button.clicked.connect(self.valtozas_elvetese)

    def toolbarpressed(self, a):
        if a.text() == "Kilépés":
            self.close()

    def valtozott(self):
        self.apply_button.setStyleSheet('background-color: green;')
        self.cancel_button.setStyleSheet('background-color: red;')

    def valtozas_mentese(self):
        self.model.submitAll()
        self.apply_button.setStyleSheet('')
        self.cancel_button.setStyleSheet('')

    def valtozas_elvetese(self):
        self.model.revertAll()
        self.apply_button.setStyleSheet('')
        self.cancel_button.setStyleSheet('')
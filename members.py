import sys
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMainWindow, QTableView, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, \
    QAction, QSpacerItem, QSizePolicy, QMessageBox
from PySide2.QtCore import *
from PySide2.QtSql import QSqlDatabase, QSqlTableModel
import pyexcel as p
from members_modell import MyFormDialog

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


class manageMembers(QMainWindow):
    def __init__(self, parent):
        super(manageMembers, self).__init__(parent)
        self.setWindowTitle("Tagok kezelése")
        widget = QWidget()
        main_layout = QHBoxLayout()
        widget.setLayout(main_layout)

        self.setCentralWidget(widget)
        self.table_view = QTableView()
        main_layout.addWidget(self.table_view)

        self.model = QSqlTableModel(db=db)
        self.model.setTable("members")
        self.model.select()
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.setHeaderData(1, Qt.Horizontal, "Vezetéknév")
        self.model.setHeaderData(2, Qt.Horizontal, "Utónév")
        self.model.setHeaderData(3, Qt.Horizontal, "Született")
        self.model.setHeaderData(4, Qt.Horizontal, "Ir.szám")
        self.model.setHeaderData(5, Qt.Horizontal, "Helység")
        self.model.setHeaderData(6, Qt.Horizontal, "Cím")
        self.model.setHeaderData(7, Qt.Horizontal, "Telefon")
        self.model.setHeaderData(8, Qt.Horizontal, "E-mail")
        self.model.setHeaderData(9, Qt.Horizontal, "Tagság kezdete")
        self.model.setHeaderData(10, Qt.Horizontal, "Aktív")
        # self.model.setFilter('vezeteknev Like "Czi%"')

        self.table_view.setModel(self.model)
        self.table_view.hideColumn(0)
        self.table_view.resizeColumnsToContents()
        # Ha ez engedélyezve, akkor a model-nél beállított sort nem működik, ez felülírja
        # Enélkül működik a model-es beállítás
        self.table_view.setSortingEnabled(True)
        # Ha engedélyezve van a fejléc szerinti rendezés, akkor UTÁNA meg lehet adni az alap sorrendet
        self.table_view.sortByColumn(1, Qt.AscendingOrder)

        self.model.dataChanged.connect(self.valtozott)
        gomb_layout = QVBoxLayout()
        main_layout.addLayout(gomb_layout)

        self.delete_button = QPushButton("&Tag törlése")
        self.add_button = QPushButton("&Új tag")
        self.apply_button = QPushButton("Módosítások alkalmazása")
        self.cancel_button = QPushButton("Módosítások elvetése")

        gomb_layout.addWidget(self.delete_button)
        gomb_layout.addWidget(self.add_button)
        gomb_layout.addWidget(self.apply_button)
        gomb_layout.addWidget(self.cancel_button)

        self.space = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gomb_layout.addItem(self.space)

        self.setFixedSize(1000, 800)
        tb = self.addToolBar("File")

        exit = QAction(QIcon("images/door--arrow.png"), "Kilépés", self)
        tb.addAction(exit)

        excel = QAction(QIcon("images/excel.png"), "Excel", self)
        tb.addAction(excel)

        tb.actionTriggered[QAction].connect(self.toolbarpressed)

        self.delete_button.clicked.connect(self.tag_torles)
        self.add_button.clicked.connect(self.tag_hozzadas)
        self.apply_button.clicked.connect(self.valtozas_mentese)
        self.cancel_button.clicked.connect(self.valtozas_elvetese)

    def tag_hozzadas(self):
        self.form_window = MyFormDialog()
        self.form_window.setWindowTitle("Új tag felvétele")
        if self.form_window.exec_():
            record = self.model.record()
            record.remove(record.indexOf('id'))

            for i in range(len(self.form_window.mezo_ertekek)):
                record.setValue(i, self.form_window.mezo_ertekek[i].text())

            if self.model.insertRecord(-1, record):
                self.model.submitAll()
                self.apply_button.setStyleSheet('')
                self.cancel_button.setStyleSheet('')
            else:
                db.rollback()

    def tag_torles(self):
        if len(self.table_view.selectedIndexes()) > 0:
            self.model.removeRow(self.table_view.selectedIndexes()[0].row())
            self.model.submitAll()
        else:
            reply = QMessageBox.question(None, 'Hiba!', 'Törlés előtt jelöljön ki egy sort!', QMessageBox.Ok)

    def toolbarpressed(self, a):
        if a.text() == "Kilépés":
            self.close()
        if a.text() == "Excel":
            data = []
            for  i in range(self.model.rowCount()):
                sor = []
                for j in range(self.model.columnCount()):
                    if isinstance(self.model.record(i).value(j), QDate):
                        sor.append(self.model.record(i).value(j).toString("yyyy-MM-dd"))
                    else:
                        sor.append(self.model.record(i).value(j))
                data.append(sor)
            p.save_as(array=data, dest_file_name="tagok.xlsx")

    def valtozott(self):
        self.apply_button.setStyleSheet('background-color: green;')
        self.cancel_button.setStyleSheet('background-color: red;')

    def valtozas_mentese(self):
        print("változások mentve")
        self.model.submitAll()
        self.apply_button.setStyleSheet('')
        self.cancel_button.setStyleSheet('')

    def valtozas_elvetese(self):
        print("változások elvetve")
        self.model.revertAll()
        self.apply_button.setStyleSheet('')
        self.cancel_button.setStyleSheet('')

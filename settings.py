from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMainWindow, QTableView, QWidget, QHBoxLayout, QAction
from settings_modell import TableModel
from database.db import MysqlClient

class manageSettings(QMainWindow):
    def __init__(self, parent):
        super(manageSettings, self).__init__(parent)
        self.setWindowTitle("Paraméterek kezelése")
        widget = QWidget()
        main_layout = QHBoxLayout()
        widget.setLayout(main_layout)

        self.setCentralWidget(widget)
        self.client = MysqlClient()
        self.table_view = QTableView()
        # a megjelenített tábla neve
        self.table_name = "settings"

        main_layout.addWidget(self.table_view)
        fejlec = ['id', 'Paraméter', "Érték"]
        self.model = TableModel(self.table_name, fejlec)

        self.table_view.setModel(self.model)
        self.table_view.setSortingEnabled(True)
        self.table_view.hideColumn(0)
        self.table_view.resizeColumnsToContents()

        # gomb_layout = QVBoxLayout()
        # main_layout.addLayout(gomb_layout)
        #
        # self.add_button = QPushButton("&Új ")
        # # self.modify_button = QPushButton("Tag &módosítása")

        # gomb_layout.addWidget(self.add_button)
        # # gomb_layout.addWidget(self.modify_button)
        # self.space = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # gomb_layout.addItem(self.space)

        self.setFixedSize(400, 600)
        # self.setWindowFlags(Qt.Window|Qt.WindowTitleHint)
        tb = self.addToolBar("File")

        exit = QAction(QIcon("images/door--arrow.png"), "Kilépés", self)
        tb.addAction(exit)

        tb.actionTriggered[QAction].connect(self.toolbarpressed)

    def toolbarpressed(self, a):
        # print("Pressed:", a.text())
        if a.text() == "Kilépés":
            self.close()

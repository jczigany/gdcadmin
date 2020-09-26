from datetime import datetime
from operator import itemgetter

from database.db import MysqlClient
from PySide2.QtWidgets import QFormLayout, QDialog, QLineEdit, QDialogButtonBox, QMessageBox
from PySide2.QtCore import *
from PySide2.QtGui import QColor, QIcon, QValidator, QIntValidator, QRegExpValidator, QDoubleValidator

client = MysqlClient()

class MyFormDialog(QDialog):
    """ A fogadott paraméter (table) alapján állítjuk össze a form-ot.
        Lekérdezzük a tábla struktúrát és összerakjuk a mezőnevek listáját,
        kihagyva a Primary mező-nevet. Ezek lesznek a LABEl-ek. A mező értékeket
        szintén egy LIST-ben tárojuk a későbbi feldolgozás lehetővé tétele érdekében"""

    def __init__(self, table):
        super(MyFormDialog, self).__init__()
        self.table = table
        self.mezo_nevek = []
        self.mezo_ertekek = []

        reg_irszam = QRegExp('(10[1-9][0-9]|1[1-2][0-9]{2}|[2-9][0-9]{3})$')
        irszValidator = QRegExpValidator(reg_irszam)

        reg_email = QRegExp('[a-zA-Z0-9._%+-]+@[a-zA-Z0-9]+\\.[a-zA-Z]{2,4}')
        # reg_email.setCaseSensitivity(Qt.CaseInsensitive)
        emailValidator = QRegExpValidator(reg_email)

        reg_datum = QRegExp('(19[0-9]{2}\\-([0][1-9]|[1][0-2])\\-([0][1-9]|[1-2][0-9]|3[0-1]))|(20[0-9]{2}\\-([0][1-9]|[1][0-2])\\-([0][1-9]|[1-2][0-9]|3[0-1]))')
        datumValidator = QRegExpValidator(reg_datum)

        # all_rows2 = client.get_mezonevek(self.table)
        # for row in all_rows2:
        #     if 'PRI' not in row:
        #         mezo_nevek.append(row[0])
        self.mezo_nevek.append("Vezetéknév")
        self.mezo_nevek.append("Utónév")
        self.mezo_nevek.append("Születési idő")
        self.mezo_nevek.append("Irányítószám")
        self.mezo_nevek.append("Helység")
        self.mezo_nevek.append("Utca, házszám")
        self.mezo_nevek.append("Telefon")
        self.mezo_nevek.append("E-mail")
        self.mezo_nevek.append("Tagság kezdete")
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        for i in range(len(self.mezo_nevek)):
            mezo = QLineEdit()
            # print(mezo_nevek[i])
            if (self.mezo_nevek[i] == "Irányítószám"):
                mezo.setValidator(irszValidator)
                # print("irányítószám meg van!")
            if (self.mezo_nevek[i] == "Telefon"):
                mezo.setInputMask("+36-99-999-9999")
            if (self.mezo_nevek[i] == "E-mail"):
                mezo.setValidator(emailValidator)
            if (self.mezo_nevek[i] == "Születési idő"):
                # print("szuletes meg van!")
                mezo.setValidator(datumValidator)
            if (self.mezo_nevek[i] == "Tagság kezdete"):
                # print("tagsag meg van!")
                mezo.setValidator(datumValidator)
            self.mezo_ertekek.append(mezo)
            self.layout.addRow(f"{self.mezo_nevek[i]}", self.mezo_ertekek[i])

        buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        self.layout.addWidget(buttonbox)


class TableModel(QAbstractTableModel):
    """ Az AbstractModel közvetlenül nem példányosítható. Elöször saját class-t származtatunk,
    majd ezt tudjuk példányosítani.
    Ennél a view típusnál minimum 3 metódust kell újradefiniálni:
    data: Honnan, és hogyan veszi az adatokat
    rowCount: Hány sora lesz a táblázatnak (az adatok alapján)
    columnCount: Hány oszlopa lesz a táblázatnak (az adatok alapján)"""

    def __init__(self, table, fejlec = None):
        super(TableModel, self).__init__()
        self.table = table
        self.fejlec = fejlec
        self.client = MysqlClient()
        self.load_data(self.table)

    def flags(self, index):
        flags = super(self.__class__, self).flags(index)
        # flags |= Qt.ItemIsEditable
        flags |= Qt.ItemIsSelectable
        flags |= Qt.ItemIsEnabled
        # flags |= Qt.ItemIsDragEnabled
        # flags |= Qt.ItemIsDropEnabled
        return flags

    def load_data(self, table):
        self.adatok = self.client.get_all(table)
        self._data = self.adatok[0]
        # print(self._data)
        if not self.fejlec:
            self.fejlec = self.adatok[1]

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            if index.isValid():
                kivalasztva = index
                # table.hideColumn(0) - val megoldva
                # A +1 azért kell, mert a Primary-t nem jelenítjük meg (1 oszloppal csúsztatva van)
                self._data[index.row()][index.column()] = value
                # print(value)
                self.client.update_table(self.table,self._data[kivalasztva.row()])
                self.dataChanged.emit(index, index, (Qt.DisplayRole, ))
                return True
            return False

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()
        if order == Qt.SortOrder.AscendingOrder:
            self._data = sorted(self._data, key=itemgetter(column), reverse=False)
        else:
            self._data = sorted(self._data, key=itemgetter(column), reverse=True)
        self.layoutChanged.emit()

    def headerData(self, section, orientation, role):
        """ table.hideColumn(0) - val megoldva
            (A Primary kulcsként használt mezőt (id) nem jelenítjük meg, ezért van a második oszloptól [section +1]
            Ha kell, akkor lehet 'nem editálhatóvá tenni' )"""
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.fejlec[section])

    def data(self, index, role):
        """ index: melyik adatról van szó.
            role: milyen feladatot kezelünk le. Lehetséges:
                DisplayRole
                BackgoundRole
                CheckStateRole
                DecorationRole
                FontRole
                TextAligmentRole
                ForegrounfRole

                table.hideColumn(0) - val megoldva
                (A Primary kulcsként használt mezőt (id) nem jelenítjük meg, ezért van a második oszloptól [index.column()+1]
                Ha kell, akkor lehet 'nem editálhatóvá tenni') """
        # COLORS = ['#053061', '#2166ac', '#4393c3', '#92c5de', '#d1e5f0', '#f7f7f7', '#fddbc7', '#f4a582', '#d6604d', '#b2182b', '#67001f']
        value = str(self._data[index.row()][index.column()])
        # print(value)
        if role == Qt.DisplayRole:
            if isinstance(value, datetime):
                return value.strftime("%Y-%m-%d")
            #
            # if isinstance(value, float):
            #     return "%.2f" % value
            #
            # if isinstance(value, str):
            #     return'"%s"' % value

            return value

        # if role == Qt.EditRole:
        #
        #     return value

        # if role == Qt.BackgroundRole and index.column() == 1:
        #     return QColor('lightblue')

        # if role == Qt.TextAlignmentRole:
        #     if isinstance(value, int) or isinstance(value, float):
        #         return Qt.AlignVCenter and Qt.AlignCenter
        #
        # if role == Qt.ForegroundRole:
        #     if (isinstance(value, int) or isinstance(value, float)) and value < 0:
        #         return QColor('red')
        #
        # # if role == Qt.BackgroundRole:
        # #     if (isinstance(value, int) or isinstance(value, float)):
        # #         value = int(value)  # Convert to integer for indexing.
        # #
        # #         # Limit to range -5 ... +5, then convert to 0..10
        # #         value = max(-5, value)  # values < -5 become -5
        # #         value = min(5, value)  # valaues > +5 become +5
        # #         value = value + 5  # -5 becomes 0, +5 becomes + 10
        # #
        # #         return QColor(COLORS[value])
        #
        # if role == Qt.DecorationRole:
        #     if isinstance(value, datetime):
        #         return QIcon('calendar.png')
        #
        #     if isinstance(value, bool):
        #         if value:
        #             return QIcon('tick.png')
        #
        #         return QIcon('cross.png')
        #
        #     if (isinstance(value, int) or isinstance(value, float)):
        #         value = int(value)  # Convert to integer for indexing.
        #         # Limit to range -5 ... +5, then convert to 0..10
        #         value = max(-5, value)  # values < -5 become -5
        #         value = min(5, value)  # valaues > +5 become +5
        #         value = value + 5  # -5 becomes 0, +5 becomes + 10
        #         return QColor(COLORS[value])

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        """ table.hideColumn(0) - val megoldva
            (A Primary kulcsként használt mezőt(id) nem jelenítjük meg, ezért van a második oszloptól len(self.data[0])-1
            Ha kell, akkor lehet 'nem editálhatóvá tenni' )"""
        return len(self._data[0])

    def delete(self, sor):
        index = sor
        all_rows2 = self.client.get_mezonevek(self.table)
        for row in all_rows2:
            if 'PRI' in row:
                id_name = row[0]
                for i in range(0, len(self.fejlec)):
                    if id_name == self.fejlec[i]:
                        torlendo_ertek = self._data[index.row()][i]

        reply = QMessageBox.question(None, 'Sor törlése!', 'A kiválasztott \
sor törlésére készül.\n A törlés nem visszavonható!\n Biztos benne?', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            # rekord törlése a model-ből és a db-ből
            del self._data[index.row()]
            self.layoutChanged.emit()
            self.client.delete_rekord(self.table, torlendo_ertek)

        return

    def add(self):
        self.form_window = MyFormDialog(self.table)
        self.form_window.setWindowTitle("Új tag felvétele")
        # self.form_window.setGeometry(QRect(100, 100, 400, 200))
        if self.form_window.exec_():
            mezo_rekord = [0]

            for i in range(len(self.form_window.mezo_ertekek)):
                mezo_rekord.append(self.form_window.mezo_ertekek[i].text())

            insert_id = client.insert_rekord(self.table, mezo_rekord)
            temp_data = client.get_one_rekord(self.table, insert_id)

            self.layoutAboutToBeChanged.emit()
            self._data.append(temp_data)
            self.layoutChanged.emit()

    def modify(self, sor):
        index = sor
        self.form_window = MyFormDialog(self.table)
        self.form_window.setWindowTitle("Tag módosítása")
        for i in range(len(self.form_window.mezo_nevek)):
            self.form_window.mezo_ertekek[i].setText(str(self._data[index.row()][i+1]))

        if self.form_window.exec_():
            mezo_rekord = [self._data[index.row()][0]]

            for i in range(len(self.form_window.mezo_ertekek)):
                mezo_rekord.append(self.form_window.mezo_ertekek[i].text())

            client.update_table(self.table, mezo_rekord)

            self.layoutAboutToBeChanged.emit()
            for i in range(len(self.form_window.mezo_nevek)):
                self._data[index.row()][i] = mezo_rekord[i]
            self.layoutChanged.emit()
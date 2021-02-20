from PySide2.QtWidgets import QFormLayout, QDialog, QLineEdit, QDialogButtonBox
from PySide2.QtCore import *
from PySide2.QtGui import QRegExpValidator


class MyFormDialog(QDialog):
    """ A fogadott paraméter (table) alapján állítjuk össze a form-ot.
        Lekérdezzük a tábla struktúrát és összerakjuk a mezőnevek listáját,
        kihagyva a Primary mező-nevet. Ezek lesznek a LABEl-ek. A mező értékeket
        szintén egy LIST-ben tárojuk a későbbi feldolgozás lehetővé tétele érdekében"""

    def __init__(self):
        super(MyFormDialog, self).__init__()
        self.mezo_nevek = []
        self.mezo_ertekek = []

        reg_irszam = QRegExp('(10[1-9][0-9]|1[1-2][0-9]{2}|[2-9][0-9]{3})$')
        irszValidator = QRegExpValidator(reg_irszam)

        reg_email = QRegExp('[a-zA-Z0-9._%+-]+@[a-zA-Z0-9]+\\.[a-zA-Z]{2,4}')
        # reg_email.setCaseSensitivity(Qt.CaseInsensitive)
        emailValidator = QRegExpValidator(reg_email)

        reg_datum = QRegExp('(19[0-9]{2}\\-([0][1-9]|[1][0-2])\\-([0][1-9]|[1-2][0-9]|3[0-1]))|(20[0-9]{2}\\-([0][1-9]|[1][0-2])\\-([0][1-9]|[1-2][0-9]|3[0-1]))')
        datumValidator = QRegExpValidator(reg_datum)

        self.mezo_nevek.append("Vezetéknév")
        self.mezo_nevek.append("Utónév")
        self.mezo_nevek.append("Születési idő")
        self.mezo_nevek.append("Irányítószám")
        self.mezo_nevek.append("Helység")
        self.mezo_nevek.append("Utca, házszám")
        self.mezo_nevek.append("Telefon")
        self.mezo_nevek.append("E-mail")
        self.mezo_nevek.append("Tagság kezdete")
        self.mezo_nevek.append("Aktív")
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        for i in range(len(self.mezo_nevek)):
            mezo = QLineEdit()
            if (self.mezo_nevek[i] == "Irányítószám"):
                mezo.setValidator(irszValidator)
            if (self.mezo_nevek[i] == "Telefon"):
                mezo.setInputMask("+36-99-999-9999")
            if (self.mezo_nevek[i] == "E-mail"):
                mezo.setValidator(emailValidator)
            if (self.mezo_nevek[i] == "Születési idő"):
                mezo.setValidator(datumValidator)
            if (self.mezo_nevek[i] == "Tagság kezdete"):
                mezo.setValidator(datumValidator)
            if (self.mezo_nevek[i] == "Aktív"):
                mezo.setText("1")
            self.mezo_ertekek.append(mezo)
            self.layout.addRow(f"{self.mezo_nevek[i]}", self.mezo_ertekek[i])

        buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        self.layout.addWidget(buttonbox)

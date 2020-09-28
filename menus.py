from PySide2.QtWidgets import QAction

def create_menus(self):
    # Menu
    self.menu = self.menuBar()

    # File menü
    self.file_menu = self.menu.addMenu("File")
    # Exit action
    exit_action = QAction("Kilépés", self)
    exit_action.setShortcut("Ctrl+Q")
    exit_action.triggered.connect(self.exit_app)
    self.file_menu.addAction(exit_action)

    # Csapat-tagok menü
    self.member_menu = self.menu.addMenu("Csapattagok")
    # Új tag action
    new_member_action = QAction("Tagok kezelése", self)
    new_member_action.setShortcut("Ctrl+T")
    new_member_action.triggered.connect(self.new_member)
    self.member_menu.addAction(new_member_action)

    # Pénzügyek menü
    self.finance_menu = self.menu.addMenu("Pénzügyek")
    # # Új Csapat action
    new_tagdij_action = QAction("Tagdíj befizetés", self)
    new_tagdij_action.setShortcut("Ctrl+H")
    new_tagdij_action.triggered.connect(self.new_tagdij)
    self.finance_menu.addAction(new_tagdij_action)

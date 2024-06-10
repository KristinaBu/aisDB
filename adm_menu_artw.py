
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QMessageBox, QTableWidgetItem
from PyQt5 import uic
from PyQt5.uic import loadUi


class AdminMenuArtw(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("windows/admin_menu_artwork.ui", self)
        self.controller = None

        self.initUI()

        self.exit.clicked.connect(self.go_exit)


    def set_controller(self, controller):
        self.controller = controller
        self.inv.clicked.connect(self.controller.show_admin_artworks_inventory)
        self.sales.clicked.connect(self.controller.show_admin_top_sales)
        self.genres.clicked.connect(self.controller.show_admin_top_genres)
        self.back.clicked.connect(self.go_exit)
        self.exit.clicked.connect(self.controller.exit_all)


    def go_exit(self):
        self.close()

    def initUI(self):
        self.setWindowTitle('Администратор - меню')


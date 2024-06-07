
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QMessageBox, QTableWidgetItem
from PyQt5 import uic
from PyQt5.uic import loadUi


class AdminMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("windows/admin_menu.ui", self)
        self.controller = None

        self.initUI()

        self.exit.clicked.connect(self.go_exit)


    def set_controller(self, controller):
        self.controller = controller
        self.cust.clicked.connect(self.controller.show_admin_cust_window)
        self.supl.clicked.connect(self.controller.show_admin_supl_window)
        self.money.clicked.connect(self.controller.show_admin_money_exit)
        self.artworks.clicked.connect(self.controller.show_admin_artworks_window)


    def go_exit(self):
        self.close()

    def initUI(self):
        self.setWindowTitle('Администратор - меню')


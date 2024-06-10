from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QMessageBox, QTableWidgetItem
from PyQt5 import uic
from PyQt5.uic import loadUi


class CustMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("windows/customer_menu.ui", self)
        self.controller = None

        self.initUI()

        self.exit.clicked.connect(self.go_exit)


    def set_controller(self, controller):
        self.controller = controller
        self.artworks.clicked.connect(self.controller.show_cust_artworks_window)
        self.my_artworks.clicked.connect(self.controller.show_cust_myartworks_window)
        self.popular.clicked.connect(self.controller.show_cust_popular_window)
        self.reviews.clicked.connect(self.controller.show_cust_rev)
        self.lk.clicked.connect(self.controller.show_cust_lk_window)


    def go_exit(self):
        self.close()

    def initUI(self):
        self.setWindowTitle('Покупатель - меню')


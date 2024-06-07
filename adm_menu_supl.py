from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QMessageBox, QTableWidgetItem
from PyQt5 import uic
from PyQt5.uic import loadUi


class AdminSuplMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("windows/admin_menu_suppliers.ui", self)
        self.controller = None

        self.initUI()

        self.back.clicked.connect(self.go_exit)

    def set_controller(self, controller):
        self.controller = controller
        self.supl_data.clicked.connect(self.controller.show_admin_supl_data_window)
        self.add_supl_2.clicked.connect(self.controller.show_admin_supl_makePuchase_window)
        self.add_supl.clicked.connect(self.controller.show_admin_supl_addSupl_window)
        self.exit.clicked.connect(self.controller.exit_all)


    def go_exit(self):
        self.close()

    def initUI(self):
        self.setWindowTitle('Администратор - меню')


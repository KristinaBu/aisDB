# app.py
import sys

from PyQt5.QtWidgets import QApplication

from cust_artworks import CustArtworks
from cust_menu import CustMenu
from adm_menu import AdminMenu
from adm_menu_cust import AdminCustMenu
from adm_menu_supl import AdminSuplMenu
from menu import MainWindow
from about import AboutWindow
from controller import Controller

if __name__ == '__main__':
    app = QApplication(sys.argv)

    controller = Controller()
    main_window = MainWindow()
    about_window = AboutWindow()
    admin_menu = AdminMenu()
    admin_cust_memu = AdminCustMenu()
    admin_supl_menu = AdminSuplMenu()
    cust_menu = CustMenu()
    cust_artworks = CustArtworks(main_window)

    controller.set_windows(main_window, about_window, admin_menu, admin_cust_memu, admin_supl_menu, cust_menu,
                           cust_artworks)
    main_window.set_controller(controller)
    about_window.set_controller(controller)
    admin_menu.set_controller(controller)
    admin_cust_memu.set_controller(controller)
    admin_supl_menu.set_controller(controller)
    cust_menu.set_controller(controller)

    #main_window.show()
    sys.exit(app.exec_())

'''
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.sign_in_window = uic.loadUi("windows/sign_in.ui")
        self.dbconnect()


        self.sign_in_window.role_type.addItem("администратор")
        self.sign_in_window.role_type.addItem("покупатель")

        self.sign_in_window.sign_in.clicked.connect(self.open_sign_in_window)
        self.sign_in_window.about_system.clicked.connect(self.open_about_window)
        self.sign_in_window.exit.clicked.connect(self.go_exit)

        self.sign_in_window.show()

    def open_sign_in_window(self):
        # Здесь вы можете добавить код для открытия окна входа в систему
        pass

    def go_exit(self):
        self.sign_in_window.close()

    def open_about_window(self):
        self.about_window.show()
        self.sign_in_window.hide()  # Скрыть главное окно

    def initUI(self):
        self.setWindowTitle('MainWindow')

    def dbconnect(self):
        # Создание соединения с БД
        db = QSqlDatabase.addDatabase('QPSQL')
        db.setHostName('localhost')
        db.setDatabaseName('ais')
        db.setUserName('iu5student')
        db.setPassword('bmstu5iu')
        if not db.open():
            QMessageBox.critical(self, "Ошибка подключения", db.lastError().text())
        else:
            QMessageBox.information(self, "Подключение", "Подключение открыто...")

    def closeEvent(self, event):
        # Закрытие соединения при закрытии приложения
        if self.conn:
            self.conn.close()


'''

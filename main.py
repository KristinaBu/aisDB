# app.py
import sys

from PyQt5.QtWidgets import QApplication

from adm_artist import AdmArtist
from adm_artw import AdmArtwt
from adm_menu_aerw_inv import AdminInventory
from adm_menu_artw import AdminMenuArtw
from adm_menu_artw_topGenres import AdmArtwGenres
from adm_menu_artw_topSales import AdmTopSales
from admin_menu_cust_data import AdmCustData
from admin_menu_money import AdmMoney
from admin_menu_supl_data import AdmSuplData
from artw_edit import ArtwEdit
from artw_look import ArtwLook
from cust_prof import CustProf
from cust_popular import CustPopular
from cust_myartworks import CustMyArtworks
from cust_artworks import CustArtworks
from cust_menu import CustMenu
from adm_menu import AdminMenu
from adm_menu_cust import AdminCustMenu
from adm_menu_supl import AdminSuplMenu
from cust_reviews import CustRev
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
    admin_menu_artw = AdminMenuArtw()

    admin_menu_inventory = AdminInventory()
    artw_edit = ArtwEdit(admin_menu_inventory)
    artw_look = ArtwLook(admin_menu_inventory)
    adm_artist = AdmArtist()
    adm_artw = AdmArtwt()
    adm_top_sales = AdmTopSales()
    sdm_top_genres = AdmArtwGenres()
    adm_cust_data = AdmCustData()
    adm_supl_data = AdmSuplData()
    adm_money = AdmMoney()

    cust_menu = CustMenu()
    cust_artworks = CustArtworks(main_window)
    cust_my_artworks = CustMyArtworks(main_window)
    cust_popular = CustPopular(main_window)
    cust_prof = CustProf(main_window)
    cust_rev = CustRev(main_window)

    controller.set_windows(main_window, about_window, admin_menu, admin_cust_memu, admin_supl_menu, cust_menu,
                           cust_artworks, cust_my_artworks, cust_popular, cust_prof, admin_menu_inventory,
                           artw_edit, artw_look, adm_artist, adm_artw, admin_menu_artw, adm_top_sales, cust_rev,
                           sdm_top_genres, adm_cust_data, adm_supl_data, adm_money)

    main_window.set_controller(controller)
    about_window.set_controller(controller)
    admin_menu.set_controller(controller)
    admin_cust_memu.set_controller(controller)
    admin_supl_menu.set_controller(controller)
    cust_menu.set_controller(controller)
    cust_artworks.set_controller(controller)
    cust_my_artworks.set_controller(controller)
    cust_popular.set_controller(controller)
    cust_prof.setCustomerId(controller)
    cust_rev.set_controller(controller)
    admin_menu_inventory.set_controller(controller)
    artw_edit.set_controller(controller)
    artw_look.set_controller(controller)
    adm_artist.set_controller(controller)
    adm_artw.set_controller(controller)
    admin_menu_artw.set_controller(controller)
    adm_top_sales.set_controller(controller)
    sdm_top_genres.set_controller(controller)
    adm_cust_data.set_controller(controller)
    adm_supl_data.set_controller(controller)
    adm_money.set_controller(controller)

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

from PyQt5.QtSql import QSqlQuery, QSqlError
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QComboBox, QLineEdit, QMessageBox, QApplication, \
    QMainWindow, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi

from consts import global_customer_id


class CustProf(QMainWindow):
    def __init__(self, sign_in_window):  # добавьте sign_in_window в качестве аргумента
        super().__init__()
        self.controller = None

        self.customer_id = None
        loadUi("windows/customer_menu_lk.ui", self)
        self.controller = None

        self.setWindowTitle('Профиль')

        sign_in_window.userSignedIn.connect(self.setCustomerId)  # Подключаем сигнал к слоту
        self.info.clicked.connect(self.load_customer_data)

    def go_exit(self):
        self.close()

    def set_controller(self, controller):
        self.controller = controller
        self.exit.clicked.connect(self.controller.exit_all)

    def setCustomerId(self, customer_id):
        self.customer_id = customer_id

    def load_customer_data(self):
        # Создать объект запроса
        query = QSqlQuery()

        # Создать строку запроса на выборку данных
        sqlstr = f"""
        SELECT person.person_name, person.email, 
               CONCAT(address.street, ', ', address.city, ', ', address.region, ', ', address.country, ', ', address.zip_code), 
               COUNT(DISTINCT sale.id), COUNT(DISTINCT reviews.id)
        FROM customer
        INNER JOIN person ON customer.person_id = person.id
        INNER JOIN address ON person.address_id = address.id
        LEFT JOIN sale ON customer.id = sale.customer_id
        LEFT JOIN reviews ON customer.id = reviews.customer_id
        WHERE customer.id = {self.customer_id}
        GROUP BY person.person_name, person.email, address.street, address.city, address.region, address.country, address.zip_code
        """

        # Выполняем запрос и проверяем его успешность
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Прочитать в цикле все строки результата
        # и заполнить поля QLineEdit
        while query.next():
            self.fio.setText(query.value(0))
            self.email.setText(query.value(1))
            self.address.setText(query.value(2))
            self.sales.setText(str(query.value(3)))
            self.reviews.setText(str(query.value(4)))

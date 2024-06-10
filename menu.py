import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QMessageBox, QTableWidgetItem
from PyQt5 import uic
import psycopg2

import consts
from consts import global_customer_id
from controller import Controller
from query_window import QueryWindow
from validations import is_not_empty, is_date_order_valid, is_not_future_date, is_database_connected



class MainWindow(QMainWindow):
    userSignedIn = pyqtSignal(int)  # Создаем новый сигнал, который передает целое число (ID пользователя)
    def __init__(self):
        super().__init__()
        self.controller = None

        self.initUI()


        self.sign_in_window = uic.loadUi("windows/sign_in.ui")
        self.dbconnect()

        self.sign_in_window.role_type.addItem("администратор")
        self.sign_in_window.role_type.addItem("покупатель")

        self.sign_in_window.sign_in.clicked.connect(self.open_sign_in_window)
        self.sign_in_window.about_system.clicked.connect(self.open_about_window)
        self.sign_in_window.exit.clicked.connect(self.go_exit)

        self.sign_in_window.show()

    def set_controller(self, controller):
        self.controller = controller
        self.sign_in_window.about_system.clicked.connect(self.controller.show_about_window)

    def open_sign_in_window(self):


        # Создать объект запроса
        query = QSqlQuery()

        # Проверить, открыто ли соединение с базой данных
        if not is_database_connected(QSqlDatabase.database()):
            QMessageBox.critical(self, "Error", "Database not connected")
            return

        email = self.sign_in_window.email_input.text()
        password = self.sign_in_window.password_input.text()

        if not is_not_empty(email) and is_not_empty(password):
            QMessageBox.critical(self, "Error", "Пожалуйста, введите данные во все поля")
            return

        role_type = self.sign_in_window.role_type.currentText()

        #email = "ivanov@example.com"
        #password = "password1"

        # Проверить, адмит или юзер
        if role_type == "покупатель":

            # Создаем SQL-запрос
            sqlstr = """
            SELECT * FROM person
            INNER JOIN customer ON person.id = customer.person_id
            WHERE person.email = '{}' AND customer.password = '{}'
            """.format(email, password)

            # Выполняем запрос
            query = QSqlQuery()
            if query.exec_(sqlstr):
                if query.next():
                    # Если запрос вернул результат, значит, человек с таким адресом электронной почты и паролем существует
                    person_name = query.value("person_name")  # Извлекаем имя человека
                    print("Человек найден, его имя:", person_name)

                    global_customer_id = query.value("id")
                    self.userSignedIn.emit(global_customer_id)  # Генерируем сигнал, передавая ID пользователя

                    self.controller.show_cust_menu()
                else:
                    # Если запрос не вернул результат, значит, человека с таким адресом электронной почты и паролем не существует
                    print("Человек не найден")
            else:
                # Если запрос не удалось выполнить, выводим сообщение об ошибке
                print("Ошибка выполнения запроса:", query.lastError().text())

        else:
            if password == consts.ADMIN_PASSWORD and email == consts.ADMIN_EMAIL:
                self.controller.show_admin_menu()

        pass

    def go_exit(self):
        self.sign_in_window.close()

    def open_about_window(self):
        self.controller.show_about_window()
        pass

    def initUI(self):
        self.setWindowTitle('Главное меню')

    def dbconnect(self):
        # Создание соединения с БД
        db = QSqlDatabase.addDatabase('QPSQL')
        db.setHostName('localhost')
        db.setDatabaseName('as')
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

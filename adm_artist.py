from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QMessageBox, QTableWidgetItem
from PyQt5 import uic
import psycopg2
from PyQt5.uic import loadUi

from validations import is_not_empty, is_date_order_valid, is_not_future_date, is_database_connected


class AdmArtist(QMainWindow):
    def __init__(self):  # добавьте sign_in_window в качестве аргумента
        super().__init__()
        self.controller = None

        loadUi("windows/adm_artist.ui", self)
        self.controller = None

        self.setWindowTitle('Художники')

        self.Insert.clicked.connect(self.addArtist)
        self.Del.clicked.connect(self.deleteArtist)
        self.Edit.clicked.connect(self.editArtist)
        self.back.clicked.connect(self.go_exit)

    def go_exit(self):
        self.close()

    def set_controller(self, controller):
        self.controller = controller
        self.exit.clicked.connect(self.controller.exit_all)

    def addArtist(self):
        # Создать объект запроса
        query = QSqlQuery()

        # Получить имя художника из соответствующего поля
        artist_name = self.name.text()

        # Проверить, не пустое ли имя художника
        if not is_not_empty(artist_name):
            QMessageBox.critical(self, "Error", "Artist name cannot be empty")
            return

        # Получить дату рождения художника
        birth_date = self.Bdate.date()

        # Проверить, не больше ли дата рождения текущего года
        if not is_not_future_date(birth_date):
            QMessageBox.critical(self, "Error", "Birth date cannot be in the future")
            return

        # Проверить, указана ли дата смерти
        if self.DdateCheckBox.isChecked():
            # Если указана, формировать запрос с датой смерти
            death_date = self.Ddate.date()

            # Проверить, не больше ли дата смерти даты рождения
            if not is_date_order_valid(birth_date, death_date):
                QMessageBox.critical(self, "Error",
                                     "Человеку не может быть больше 150 лет или отрицательное число лет")
                return
            if not is_not_future_date(death_date):
                QMessageBox.critical(self, "Error", "Художник будущего?")
                return

            sqlstr = "INSERT INTO artist (artist_name, birth_date, death_date) VALUES ('{}', '{}', '{}')".format(
                artist_name.strip(),
                birth_date.toString("yyyy-MM-dd"),
                death_date.toString("yyyy-MM-dd"))
        else:
            # Если не указана, формировать запрос без даты смерти
            sqlstr = "INSERT INTO artist (artist_name, birth_date) VALUES ('{}', '{}')".format(
                artist_name.strip(),
                birth_date.toString("yyyy-MM-dd"))

        # Выполнить запрос и проверить его успешность
        try:
            if not query.exec_(sqlstr):
                raise Exception(query.lastError().text())
        except Exception as e:
            error_message = str(e)
            if 'duplicate key value violates unique constraint' in error_message:
                QMessageBox.critical(self, "Error", "Художник уже существует в БД")
            elif ' invalid input syntax for type date' in error_message:
                QMessageBox.critical(self, "Error", "Неверный формат даты")
            else:
                QMessageBox.critical(self, "Error", error_message)
            return

    def deleteArtist(self):
        # Создать объект запроса
        query = QSqlQuery()

        # Получить имя художника из соответствующего поля
        artist_name = self.name.text()

        # Проверить, не пустое ли имя художника
        if not is_not_empty(artist_name):
            QMessageBox.critical(self, "Error", "Заполните все поля")
            return

        # Создать строку запроса на удаление данных
        sqlstr = f"DELETE FROM artist WHERE artist_name = '{artist_name}'"

        # Выполнить запрос и проверить его успешность
        try:
            if not query.exec_(sqlstr):
                raise Exception(query.lastError().text())
        except Exception as e:
            error_message = str(e)
            if 'invalid input syntax for type integer' in error_message:
                QMessageBox.critical(self, "Error", "Неверный id")
            else:
                QMessageBox.critical(self, "Error", error_message)
            return

    def editArtist(self):
        # Создать объект запроса
        query = QSqlQuery()

        # Проверить, открыто ли соединение с базой данных
        if not is_database_connected(QSqlDatabase.database()):
            QMessageBox.critical(self, "Error", "Database not connected")
            return

        # Получить имя художника из соответствующего поля
        artist_name = self.name.text()

        # Проверить, не пустое ли имя художника
        if not is_not_empty(artist_name):
            QMessageBox.critical(self, "Error", "Заполните имя")
            return

        # Получить дату рождения художника
        birth_date = self.Bdate.date()

        # Проверить, не больше ли дата рождения текущего года
        if not is_not_future_date(birth_date):
            QMessageBox.critical(self, "Error", "Художник будущего?")
            return

        # Проверить, указана ли дата смерти
        if self.DdateCheckBox.isChecked():
            # Если указана, формировать запрос с датой смерти
            death_date = self.Ddate.date()

            # Проверить, не больше ли дата смерти даты рождения
            if not is_date_order_valid(birth_date, death_date):
                QMessageBox.critical(self, "Error",
                                     "Человеку не может быть больше 150 лет или отрицательное число лет")
                return
            if not is_not_future_date(death_date):
                QMessageBox.critical(self, "Error", "Художник будущего?")
                return

            sqlstr = f"UPDATE artist SET artist_name = '{artist_name}', birth_date = '{birth_date.toString('yyyy-MM-dd')}', death_date = '{death_date.toString('yyyy-MM-dd')}' WHERE artist_name = '{artist_name}'"
        else:
            # Если не указана, формировать запрос без даты смерти
            sqlstr = f"UPDATE artist SET artist_name = '{artist_name}', birth_date = '{birth_date.toString('yyyy-MM-dd')}' WHERE artist_name = '{artist_name}'"

        # Выполнить запрос и проверить его успешность
        try:
            if not query.exec_(sqlstr):
                raise Exception(query.lastError().text())
        except Exception as e:
            error_message = str(e)
            if 'duplicate key value violates unique constraint' in error_message:
                QMessageBox.critical(self, "Error", "Художник уже есть в базе")
            elif ' invalid input syntax for type date' in error_message:
                QMessageBox.critical(self, "Error", "Invalid date format")
            else:
                QMessageBox.critical(self, "Error", error_message)
            return

        self.selectAll()

import sys

from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QMessageBox, QTableWidgetItem
from PyQt5 import uic
import psycopg2

from query_window import QueryWindow
from validations import is_not_empty, is_date_order_valid, is_not_future_date, is_database_connected


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.test_window = uic.loadUi("test_window.ui")
        self.test_window.Connect.clicked.connect(self.dbconnect)  # Назначение обработчика
        self.test_window.SelectAll.clicked.connect(self.selectAll)  # Назначение обработчика
        self.test_window.InsertArtist.clicked.connect(self.addArtist)
        self.test_window.DelArtist.clicked.connect(self.deleteArtist)
        self.test_window.EditArtist.clicked.connect(self.editArtist)
        self.test_window.OpenQueryWindow.clicked.connect(self.open_query_window)

        self.test_window.show()

    def open_query_window(self):
        self.query_window = QueryWindow(self)
        self.query_window.show()

    def initUI(self):
        self.setWindowTitle('MainWindow')

    def open_test_window(self):
        self.test_window.show()


    def dbconnect(self):
        # Создание соединения с БД
        db = QSqlDatabase.addDatabase('QPSQL')
        db.setHostName('localhost')
        db.setDatabaseName('ais')
        db.setUserName('iu5student')
        db.setPassword('bmstu5iu')
        if not db.open():
            self.test_window.teResult.append("Error of connect:")
            self.test_window.teResult.append(db.lastError().text())
        else:
            self.test_window.teResult.append("Connect is open...")

    def closeEvent(self, event):
        # Закрытие соединения при закрытии приложения
        if self.conn:
            self.conn.close()

    def selectAll(self):
        # Очистить содержимое компонента
        self.test_window.tableWidgetArtist.setRowCount(0)

        # Установить заголовки столбцов
        self.test_window.tableWidgetArtist.setHorizontalHeaderLabels(['ID', 'Name', 'Birth Date', 'Death Date'])

        # Установить количество столбцов
        self.test_window.tableWidgetArtist.setColumnCount(4)

        # Создать объект запроса
        query = QSqlQuery()

        # Создать строку запроса на выборку данных
        sqlstr = "SELECT * FROM artist"

        # Выполнить запрос и проверить его успешность
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Прочитать в цикле все строки результата
        # и вывести их в компонент таблицы
        while query.next():
            row = self.test_window.tableWidgetArtist.rowCount()
            self.test_window.tableWidgetArtist.insertRow(row)
            self.test_window.tableWidgetArtist.setItem(row, 0, QTableWidgetItem(str(query.value("id"))))
            self.test_window.tableWidgetArtist.setItem(row, 1, QTableWidgetItem(query.value("artist_name")))
            self.test_window.tableWidgetArtist.setItem(row, 2, QTableWidgetItem(
                query.value("birth_date").toString("yyyy-MM-dd")))
            self.test_window.tableWidgetArtist.setItem(row, 3, QTableWidgetItem(
                query.value("death_date").toString("yyyy-MM-dd") if query.value("death_date") else ''))

    def addArtist(self):
        # Создать объект запроса
        query = QSqlQuery()

        # Проверить, открыто ли соединение с базой данных
        if not is_database_connected(QSqlDatabase.database()):
            QMessageBox.critical(self, "Error", "Database not connected")
            return

        # Получить имя художника из соответствующего поля
        artist_name = self.test_window.nameLine.text()

        # Проверить, не пустое ли имя художника
        if not is_not_empty(artist_name):
            QMessageBox.critical(self, "Error", "Artist name cannot be empty")
            return

        # Получить дату рождения художника
        birth_date = self.test_window.BdateEdit.date()

        # Проверить, не больше ли дата рождения текущего года
        if not is_not_future_date(birth_date):
            QMessageBox.critical(self, "Error", "Birth date cannot be in the future")
            return

        # Проверить, указана ли дата смерти
        if self.test_window.DdateCheckBox.isChecked():
            # Если указана, формировать запрос с датой смерти
            death_date = self.test_window.DdateEdit.date()

            # Проверить, не больше ли дата смерти даты рождения
            if not is_date_order_valid(birth_date, death_date):
                QMessageBox.critical(self, "Error",
                                     "Death date cannot be before birth date or artist's age cannot be more than 150 years")
                return
            if not is_not_future_date(death_date):
                QMessageBox.critical(self, "Error", "Death date cannot be in the future")
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
                QMessageBox.critical(self, "Error", "This artist already exists in the database.")
            elif ' invalid input syntax for type date' in error_message:
                QMessageBox.critical(self, "Error", "Invalid date format")
            else:
                QMessageBox.critical(self, "Error", error_message)
            return

        self.selectAll()

    def deleteArtist(self):
        # Создать объект запроса
        query = QSqlQuery()

        # Проверить, открыто ли соединение с базой данных
        if not is_database_connected(QSqlDatabase.database()):
            QMessageBox.critical(self, "Error", "Database not connected")
            return

        # Получить id художника из соответствующего поля
        artist_id = self.test_window.idLine.text()

        # Проверить, не пустой ли id художника
        if not is_not_empty(artist_id):
            QMessageBox.critical(self, "Error", "Artist id cannot be empty")
            return

        # Check if the id is a valid integer
        if not artist_id.isdigit():
            QMessageBox.critical(self, "Error", "Invalid id format")
            return

        # Создать строку запроса на удаление данных
        sqlstr = "DELETE FROM artist WHERE id = {}".format(artist_id)

        # Выполнить запрос и проверить его успешность
        try:
            if not query.exec_(sqlstr):
                raise Exception(query.lastError().text())
        except Exception as e:
            error_message = str(e)
            if 'invalid input syntax for type integer' in error_message:
                QMessageBox.critical(self, "Error", "Invalid id format")
            else:
                QMessageBox.critical(self, "Error", error_message)
            return

        self.selectAll()

    def editArtist(self):
        # Создать объект запроса
        query = QSqlQuery()

        # Проверить, открыто ли соединение с базой данных
        if not is_database_connected(QSqlDatabase.database()):
            QMessageBox.critical(self, "Error", "Database not connected")
            return

        # Получить id художника из соответствующего поля
        artist_id = self.test_window.idLine.text()

        # Проверить, не пустой ли id художника
        if not is_not_empty(artist_id):
            QMessageBox.critical(self, "Error", "Artist id cannot be empty")
            return

        # Check if the id is a valid integer
        if not artist_id.isdigit():
            QMessageBox.critical(self, "Error", "Invalid id format")
            return

        # Получить имя художника из соответствующего поля
        artist_name = self.test_window.nameLine.text()

        # Проверить, не пустое ли имя художника
        if not is_not_empty(artist_name):
            QMessageBox.critical(self, "Error", "Artist name cannot be empty")
            return

        # Получить дату рождения художника
        birth_date = self.test_window.BdateEdit.date()

        # Проверить, не больше ли дата рождения текущего года
        if not is_not_future_date(birth_date):
            QMessageBox.critical(self, "Error", "Birth date cannot be in the future")
            return

        # Проверить, указана ли дата смерти
        if self.test_window.DdateCheckBox.isChecked():
            # Если указана, формировать запрос с датой смерти
            death_date = self.test_window.DdateEdit.date()

            # Проверить, не больше ли дата смерти даты рождения
            if not is_date_order_valid(birth_date, death_date):
                QMessageBox.critical(self, "Error", "Death date cannot be before birth date or artist's age cannot be more than 150 years")
                return
            if not is_not_future_date(death_date):
                QMessageBox.critical(self, "Error", "Death date cannot be in the future")
                return

            sqlstr = "UPDATE artist SET artist_name = '{}', birth_date = '{}', death_date = '{}' WHERE id = {}".format(
                artist_name.strip(),
                birth_date.toString("yyyy-MM-dd"),
                death_date.toString("yyyy-MM-dd"),
                artist_id)
        else:
            # Если не указана, формировать запрос без даты смерти
            sqlstr = "UPDATE artist SET artist_name = '{}', birth_date = '{}' WHERE id = {}".format(
                artist_name.strip(),
                birth_date.toString("yyyy-MM-dd"),
                artist_id)

        # Выполнить запрос и проверить его успешность
        try:
            if not query.exec_(sqlstr):
                raise Exception(query.lastError().text())
        except Exception as e:
            error_message = str(e)
            if 'duplicate key value violates unique constraint' in error_message:
                QMessageBox.critical(self, "Error", "This artist already exists in the database.")
            elif ' invalid input syntax for type date' in error_message:
                QMessageBox.critical(self, "Error", "Invalid date format")
            else:
                QMessageBox.critical(self, "Error", error_message)
            return

        self.selectAll()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


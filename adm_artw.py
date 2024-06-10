from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QMessageBox, QTableWidgetItem
from PyQt5 import uic
import psycopg2
from PyQt5.uic import loadUi

from validations import is_not_empty, is_date_order_valid, is_not_future_date, is_database_connected


class AdmArtwt(QMainWindow):
    def __init__(self):  # добавьте sign_in_window в качестве аргумента
        super().__init__()
        self.controller = None

        loadUi("windows/adm_artw.ui", self)
        self.controller = None

        self.setWindowTitle('Товар')

        self.load_genres()
        self.load_artists()

        self.Insert.clicked.connect(self.add_artwork)
        self.back.clicked.connect(self.go_exit)

    def go_exit(self):
        self.close()

    def load_genres(self):
        query = QSqlQuery()
        sqlstr = "SELECT genre_name FROM genre"
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        while query.next():
            genre_name = query.value(0)
            self.genres.addItem(genre_name)


    def load_artists(self):
        query = QSqlQuery()
        sqlstr = "SELECT artist_name FROM artist"
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        while query.next():
            artt_name = query.value(0)
            self.artt.addItem(artt_name)

    def set_controller(self, controller):
        self.controller = controller
        self.exit.clicked.connect(self.controller.exit_all)

    def add_artwork(self):
        # Получаем данные из полей
        title = self.name.text()
        cost = self.cost.text()
        artist_name = self.artt.currentText()  # Получаем имя художника из QComboBox
        genre_ids = [item.data(Qt.UserRole) for item in self.genres.selectedItems()]  # Получаем выбранные жанры

        # Находим ID художника по имени
        query_artist = QSqlQuery()
        sqlstr_artist = f"SELECT id FROM artist WHERE artist_name = '{artist_name}';"
        if not query_artist.exec_(sqlstr_artist):
            QMessageBox.critical(self, "Error", query_artist.lastError().text())
            return
        if not query_artist.next():
            QMessageBox.critical(self, "Error", "Artist not found.")
            return
        artist_id = query_artist.value(0)

        # Вставляем основную информацию о произведении
        query = QSqlQuery()
        sqlstr = """
        INSERT INTO artwork (title, artist_id, price_main, price_fraction, quantity)
        VALUES (?,?,?,?,?)
        """
        query.prepare(sqlstr)
        query.addBindValue(title)
        query.addBindValue(artist_id)  # Используем найденный ID художника
        query.addBindValue(cost)
        query.addBindValue(0)  # Дробная часть цены не указана, предполагается, что она равна 0
        query.addBindValue(0)  # Количество на складе не указано, предполагается, что оно равно 0
        if not query.exec_():
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Добавляем связи с жанрами
        for genre_id in genre_ids:
            if genre_id is None:  # Проверяем, что genre_id не является None
                continue  # Пропускаем текущую итерацию, если genre_id отсутствует
            sqlstr = "INSERT INTO artwork_genre (artwork_id, genre_id) VALUES (?,?)"
            query.prepare(sqlstr)
            query.addBindValue(query.lastInsertId())  # Используем ID последней вставленной картины
            query.addBindValue(genre_id)
            if not query.exec_():
                QMessageBox.critical(self, "Error", query.lastError().text())
                return

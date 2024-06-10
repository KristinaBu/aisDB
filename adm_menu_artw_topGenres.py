from PyQt5.QtCore import pyqtSignal
from PyQt5.QtSql import QSqlQuery, QSqlError
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QComboBox, QLineEdit, QMessageBox, QApplication, \
    QMainWindow, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi



class AdmArtwGenres(QMainWindow):
    clickArtw = pyqtSignal(int)  # Создаем новый сигнал, который передает целое число (ID пользователя)

    def __init__(self):  # добавьте sign_in_window в качестве аргумента
        super().__init__()
        self.controller = None

        self.selected_artwork_id = None

        loadUi("windows/admin_menu_artwork_topgenres.ui", self)
        self.controller = None

        self.setWindowTitle('Топ жанров')


        self.count.clicked.connect(self.top_genres_by_count)
        self.rev.clicked.connect(self.bottom_genres_by_reviews)

        self.back.clicked.connect(self.go_exit)

    def go_exit(self):
        self.close()

    def set_controller(self, controller):
        self.controller = controller
        self.exit.clicked.connect(self.controller.exit_all)

    def top_genres_by_count(self):
        # Очистить содержимое компонента
        self.genres.setRowCount(0)

        # Установить количество столбцов
        self.genres.setColumnCount(2)

        self.genres.setHorizontalHeaderLabels(['Жанр', 'Количество произведений'])

        # Растянуть столбцы, чтобы они занимали всю доступную ширину
        self.genres.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Создать объект запроса
        query = QSqlQuery()

        # Создать строку запроса на выборку данных
        sqlstr = """
        SELECT g.genre_name, COUNT(ag.artwork_id) AS count
        FROM genre g
        INNER JOIN artwork_genre ag ON g.id = ag.genre_id
        INNER JOIN artwork ON ag.artwork_id = artwork.id
        GROUP BY g.id
        ORDER BY count DESC
        LIMIT 10;
        """

        # Выполнить запрос и проверить его успешность
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Прочитать в цикле все строки результата
        # и вывести их в компонент таблицы
        while query.next():
            row = self.genres.rowCount()
            self.genres.insertRow(row)
            self.genres.setItem(row, 0, QTableWidgetItem(query.value(0)))
            self.genres.setItem(row, 1, QTableWidgetItem(str(query.value(1))))

    def bottom_genres_by_reviews(self):
        # Очистить содержимое компонента
        self.genres.setRowCount(0)

        # Установить количество столбцов
        self.genres.setColumnCount(2)

        self.genres.setHorizontalHeaderLabels(['Жанр', 'Количество отзывов'])

        # Растянуть столбцы, чтобы они занимали всю доступную ширину
        self.genres.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Создать объект запроса
        query = QSqlQuery()

        # Создать строку запроса на выборку данных
        sqlstr = """
        SELECT g.genre_name, COUNT(DISTINCT r.artwork_id) AS review_count
        FROM genre g
        INNER JOIN artwork_genre ag ON g.id = ag.genre_id
        INNER JOIN artwork ON ag.artwork_id = artwork.id
        LEFT JOIN reviews r ON artwork.id = r.artwork_id
        GROUP BY g.id
        ORDER BY review_count
        LIMIT 10;
        """

        # Выполнить запрос и проверить его успешность
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Прочитать в цикле все строки результата
        # и вывести их в компонент таблицы
        while query.next():
            row = self.genres.rowCount()
            self.genres.insertRow(row)
            self.genres.setItem(row, 0, QTableWidgetItem(query.value(0)))
            self.genres.setItem(row, 1, QTableWidgetItem(str(query.value(1))))

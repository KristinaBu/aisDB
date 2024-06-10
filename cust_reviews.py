from PyQt5.QtCore import pyqtSignal
from PyQt5.QtSql import QSqlQuery, QSqlError
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QComboBox, QLineEdit, QMessageBox, QApplication, \
    QMainWindow, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi



class CustRev(QMainWindow):
    clickArtw = pyqtSignal(int)  # Создаем новый сигнал, который передает целое число (ID пользователя)

    def __init__(self, sign_in_window):  # добавьте sign_in_window в качестве аргумента
        super().__init__()
        self.controller = None

        self.selected_artwork_id = None
        self.customer_id = None

        loadUi("windows/cust_reviews.ui", self)
        self.controller = None

        self.setWindowTitle('Отзывы')

        sign_in_window.userSignedIn.connect(self.setCustomerId)


        self.all.clicked.connect(self.print_all)
        self.print_r.clicked.connect(self.getReviews)
        self.print_mr.clicked.connect(self.getMyReviews)

        self.artworks.cellClicked.connect(self.onCellClicked)

        self.back.clicked.connect(self.go_exit)

    def go_exit(self):
        self.close()

    def setCustomerId(self, customer_id):
        self.customer_id = customer_id
    def set_controller(self, controller):
        self.controller = controller
        self.exit.clicked.connect(self.controller.exit_all)

    def onCellClicked(self, row, column):
        # Получаем элемент по указанным координатам
        item = self.artworks.item(row, column)

        if item is not None:
            # Извлекаем информацию из ячейки
            artwork_info = item.text()

            # Предполагаем, что в первой колонке хранится название произведения,
            # а во второй - количество продаж, поэтому используем название для поиска ID
            query = QSqlQuery()
            sqlstr = f"SELECT id FROM artwork WHERE title = '{artwork_info}';"

            if not query.exec_(sqlstr):
                QMessageBox.critical(self, "Error", query.lastError().text())
                return

            if query.next():
                artwork_id = query.value(0)  # Получаем ID произведения искусства


                # Эмитируем сигнал clickArtw с artwork_id
                self.clickArtw.emit(artwork_id)

                print("ID произведения искусства = ", artwork_id)
                self.selected_artwork_id = artwork_id

                # Получаем и отображаем отзывы по artwork_id
                self.getReviews(artwork_id)

    def print_all(self):
        # Очистить содержимое компонента
        self.artworks.setRowCount(0)

        # Установить количество столбцов
        self.artworks.setColumnCount(4)

        self.artworks.setHorizontalHeaderLabels(['Названиие', 'Художник', 'Цена', 'На складе'])

        # Растянуть столбцы, чтобы они занимали всю доступную ширину
        self.artworks.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Создать объект запроса
        query = QSqlQuery()

        # Создать строку запроса на выборку данных
        sqlstr = """
        SELECT artwork.title, artist.artist_name, artwork.price_main, artwork.quantity
        FROM artwork
        INNER JOIN artist ON artwork.artist_id = artist.id
        """

        # Выполнить запрос и проверить его успешность
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Прочитать в цикле все строки результата
        # и вывести их в компонент таблицы
        while query.next():
            row = self.artworks.rowCount()
            self.artworks.insertRow(row)
            self.artworks.setItem(row, 0, QTableWidgetItem(query.value(0)))
            self.artworks.setItem(row, 1, QTableWidgetItem(query.value(1)))
            self.artworks.setItem(row, 2, QTableWidgetItem(str(query.value(2))))
            self.artworks.setItem(row, 3, QTableWidgetItem(str(query.value(3))))

    def getReviews(self, artwork_id):
        # Очистка предыдущих отзывов
        self.reviews.setRowCount(0)

        self.reviews.setColumnCount(3)

        self.reviews.setHorizontalHeaderLabels(['Дата', 'Рейтинг', 'Текст'])



        # Создание объекта запроса
        query = QSqlQuery()

        # Запрос к таблице reviews для получения отзывов по artwork_id
        sqlstr = f"""
        SELECT review_text, rating, review_date
        FROM reviews
        WHERE artwork_id = {artwork_id};
        """

        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Печать каждого поля в кортеже для отладки
        from PyQt5.QtCore import QDateTime

        # Внутри цикла, где вы обрабатываете каждый отзыв
        while query.next():
            review_text = query.value(0)
            rating = query.value(1)
            review_date = query.value(2)

            print(f"Review Text: {review_text}, Rating: {rating}")

            row = self.reviews.rowCount()
            self.reviews.insertRow(row)
            self.reviews.setItem(row, 0, QTableWidgetItem(review_date.toString('yyyy-MM-dd')))
            self.reviews.setItem(row, 1, QTableWidgetItem(str(rating)))  # Оценка
            # Изменение здесь: Получаем только часть даты без времени
            self.reviews.setItem(row, 2, QTableWidgetItem(str(review_text)))  # Оценка

            # Растянуть столбцы, чтобы они занимали всю доступную ширину
        self.reviews.resizeColumnsToContents()

    def getMyReviews(self, customer_id):
        # Очистка предыдущих отзывов
        self.my_reviews.setRowCount(0)

        self.my_reviews.setColumnCount(4)  # Увеличено количество столбцов на 1

        self.my_reviews.setHorizontalHeaderLabels(['Дата', 'Название произведения', 'Рейтинг', 'Текст'])

        # Создание объекта запроса
        query = QSqlQuery()

        # Запрос к таблице reviews для получения отзывов по customer_id с названием произведения
        sqlstr = f"""
        SELECT r.review_date, a.title, r.rating, r.review_text
        FROM reviews r
        JOIN artwork a ON r.artwork_id = a.id
        WHERE r.customer_id = {self.customer_id};
        """

        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Внутри цикла, где вы обрабатываете каждый отзыв
        while query.next():
            review_date = query.value(0)
            artwork_title = query.value(1)
            rating = query.value(2)
            review_text = query.value(3)

            print(f"Review Date: {review_date}, Artwork Title: {artwork_title}, Rating: {rating}")

            row = self.my_reviews.rowCount()
            self.my_reviews.insertRow(row)
            self.my_reviews.setItem(row, 0, QTableWidgetItem(review_date.toString('yyyy-MM-dd')))
            self.my_reviews.setItem(row, 1, QTableWidgetItem(artwork_title))  # Название произведения
            self.my_reviews.setItem(row, 2, QTableWidgetItem(str(rating)))  # Оценка
            self.my_reviews.setItem(row, 3, QTableWidgetItem(str(review_text)))  # Текст отзыва

        # Растянуть столбцы, чтобы они занимали всю доступную ширину
        self.my_reviews.resizeColumnsToContents()

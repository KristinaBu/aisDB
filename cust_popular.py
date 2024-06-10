from PyQt5.QtSql import QSqlQuery, QSqlError
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QComboBox, QLineEdit, QMessageBox, QApplication, \
    QMainWindow, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi


class CustPopular(QMainWindow):
    def __init__(self, sign_in_window):  # добавьте sign_in_window в качестве аргумента
        super().__init__()
        self.controller = None

        self.customer_id = None
        loadUi("windows/customer_menu_popular.ui", self)
        self.controller = None

        self.setWindowTitle('Популярное')

        sign_in_window.userSignedIn.connect(self.setCustomerId)  # Подключаем сигнал к слоту

        self.art_sale.clicked.connect(self.print_top_art_sale)
        self.art_raiting.clicked.connect(self.print_top_rated_artworks)
        self.art.clicked.connect(self.print_top_artists)
        self.top_gen.clicked.connect(self.print_top_genres)

        self.artworks.cellClicked.connect(self.onCellClicked)
        self.sum.clicked.connect(self.sum_calculate)

        self.buy.clicked.connect(self.buy_artwork)
        self.back.clicked.connect(self.go_exit)

    def go_exit(self):
        self.close()

    def set_controller(self, controller):
        self.controller = controller
        self.exit.clicked.connect(self.controller.exit_all)

    def setCustomerId(self, customer_id):
        self.customer_id = customer_id

    def onCellClicked(self, row, column):
        item = self.artworks.item(row, 0)  # получите элемент в первом столбце (название произведения искусства)
        if item is not None:
            artwork_title = item.text()
            self.name.setText(artwork_title)  # установите текст в поле name окна покупки

    def print_top_art_sale(self):
        # Очистить содержимое компонента
        self.artworks.setRowCount(0)

        # Установить количество столбцов
        self.artworks.setColumnCount(3)

        self.artworks.setHorizontalHeaderLabels(['Название', 'Продано', 'Число покупалетей'])

        # Растянуть столбцы, чтобы они занимали всю доступную ширину
        self.artworks.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Создать объект запроса
        query = QSqlQuery()

        # Создать строку запроса на выборку данных
        sqlstr = f"""
        SELECT artwork.title, SUM(operation.quantity), COUNT(DISTINCT sale.customer_id)
        FROM sale
        INNER JOIN operation ON sale.operation_id = operation.id
        INNER JOIN artwork ON operation.artwork_id = artwork.id
        GROUP BY artwork.title
        ORDER BY SUM(operation.quantity) DESC
        LIMIT 10
        """

        # Выполняем запрос и проверяем его успешность
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Прочитать в цикле все строки результата
        # и вывести их в компонент таблицы
        while query.next():
            row = self.artworks.rowCount()
            self.artworks.insertRow(row)
            self.artworks.setItem(row, 0, QTableWidgetItem(query.value(0)))
            self.artworks.setItem(row, 1, QTableWidgetItem(str(query.value(1))))
            self.artworks.setItem(row, 2, QTableWidgetItem(str(query.value(2))))

    def print_top_artists(self):
        # Очистить содержимое компонента
        self.artworks.setRowCount(0)

        # Установить количество столбцов
        self.artworks.setColumnCount(5)

        self.artworks.setHorizontalHeaderLabels(
            ['Имя', 'Дата рождения', 'Дата смерти', 'Картина', 'Продано'])

        # Растянуть столбцы, чтобы они занимали всю доступную ширину
        self.artworks.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Создать объект запроса
        query = QSqlQuery()

        # Создать строку запроса на выборку данных
        sqlstr = f"""
        SELECT artist.artist_name, artist.birth_date, artist.death_date, artwork.title, SUM(operation.quantity) as total_sold
        FROM sale
        INNER JOIN operation ON sale.operation_id = operation.id
        INNER JOIN artwork ON operation.artwork_id = artwork.id
        INNER JOIN artist ON artwork.artist_id = artist.id
        GROUP BY artist.artist_name, artist.birth_date, artist.death_date, artwork.title
        ORDER BY total_sold DESC
        LIMIT 10
        """

        # Выполняем запрос и проверяем его успешность
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Прочитать в цикле все строки результата
        # и вывести их в компонент таблицы
        while query.next():
            row = self.artworks.rowCount()
            self.artworks.insertRow(row)
            self.artworks.setItem(row, 0, QTableWidgetItem(query.value(0)))
            self.artworks.setItem(row, 1, QTableWidgetItem(query.value(1).toString("yyyy-MM-dd")))
            self.artworks.setItem(row, 2,
                                  QTableWidgetItem(query.value(2).toString("yyyy-MM-dd") if query.value(2) else ''))
            self.artworks.setItem(row, 3, QTableWidgetItem(query.value(3)))
            self.artworks.setItem(row, 4, QTableWidgetItem(str(query.value(4))))



    def print_top_rated_artworks(self):
        # Очистить содержимое компонента
        self.artworks.setRowCount(0)

        # Установить количество столбцов
        self.artworks.setColumnCount(3)

        self.artworks.setHorizontalHeaderLabels(['Картина', 'Художник', 'Средний рейтинг'])

        # Растянуть столбцы, чтобы они занимали всю доступную ширину
        self.artworks.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Создать объект запроса
        query = QSqlQuery()

        # Создать строку запроса на выборку данных
        sqlstr = f"""
        SELECT artwork.title, artist.artist_name, AVG(reviews.rating) as average_rating
        FROM reviews
        INNER JOIN artwork ON reviews.artwork_id = artwork.id
        INNER JOIN artist ON artwork.artist_id = artist.id
        GROUP BY artwork.title, artist.artist_name
        ORDER BY average_rating DESC
        LIMIT 10
        """

        # Выполняем запрос и проверяем его успешность
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

    def print_top_genres(self):
        # Очистить содержимое компонента
        self.artworks.setRowCount(0)

        # Установить количество столбцов
        self.artworks.setColumnCount(2)

        self.artworks.setHorizontalHeaderLabels(['Жанр', 'Продано'])

        # Растянуть столбцы, чтобы они занимали всю доступную ширину
        self.artworks.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Создать объект запроса
        query = QSqlQuery()

        # Создать строку запроса на выборку данных
        sqlstr = f"""
        SELECT genre.genre_name, SUM(operation.quantity) as total_sold
        FROM sale
        INNER JOIN operation ON sale.operation_id = operation.id
        INNER JOIN artwork ON operation.artwork_id = artwork.id
        INNER JOIN artwork_genre ON artwork.id = artwork_genre.artwork_id
        INNER JOIN genre ON artwork_genre.genre_id = genre.id
        GROUP BY genre.genre_name
        ORDER BY total_sold DESC
        LIMIT 10
        """

        # Выполняем запрос и проверяем его успешность
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Прочитать в цикле все строки результата
        # и вывести их в компонент таблицы
        while query.next():
            row = self.artworks.rowCount()
            self.artworks.insertRow(row)
            self.artworks.setItem(row, 0, QTableWidgetItem(query.value(0)))
            self.artworks.setItem(row, 1, QTableWidgetItem(str(query.value(1))))

    def print_how_many(self):
        # Получить название произведения из QLineEdit
        artwork_title = self.name.text()

        # Создать объект запроса
        query = QSqlQuery()

        # Создать строку запроса на выборку данных
        sqlstr = f"SELECT quantity FROM artwork WHERE title = '{artwork_title}'"

        # Выполнить запрос и проверить его успешность
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Если запрос вернул результат
        if query.next():
            quantity = query.value(0)
            # Вывести количество единиц на складе в виджет count_artw
            self.count_artw.setText(str(quantity))
        else:
            QMessageBox.information(self, "Info", "Произведение искусства не найдено")

    def sum_calculate(self):
        # Считываем название произведения искусства из QLineEdit
        artwork_title = self.name.text()

        # Считываем количество из QSpinBox
        count = self.count.value()

        # Создаем объект запроса
        query = QSqlQuery()

        # Создаем строку запроса на выборку данных о произведении искусства
        sqlstr = f"SELECT price_main, price_fraction, quantity FROM artwork WHERE title = '{artwork_title}'"

        # Выполняем запрос и проверяем его успешность
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Если запрос вернул результат
        if query.next():
            price_main = query.value(0)
            price_fraction = query.value(1)
            quantity = query.value(2)

            # Проверяем, достаточно ли произведений искусства на складе
            if quantity < count:
                QMessageBox.information(self, "Info", "Недостаточное количество произведений искусства на складе")
                return

            # Рассчитываем итоговую сумму заказа
            total_main = price_main * count
            total_fraction = price_fraction * count

            # Учитываем перенос из дробной части в основную
            total_main += total_fraction // 100
            total_fraction %= 100

            # Выводим итоговую сумму заказа в поле sum_count
            self.sum_count.setText(f"{total_main}.{total_fraction:02d}")

    def buy_artwork(self):
        global global_customer_id
        # Считываем название произведения искусства из QLineEdit
        artwork_title = self.name.text()

        # Считываем количество из QSpinBox
        count = self.count.value()

        # Создаем объект запроса
        query = QSqlQuery()

        # Создаем строку запроса на выборку данных о произведении искусства
        sqlstr = f"SELECT price_main, price_fraction, quantity FROM artwork WHERE title = '{artwork_title}'"

        # Выполняем запрос и проверяем его успешность
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Если запрос вернул результат
        if query.next():
            price_main = query.value(0)
            price_fraction = query.value(1)
            quantity = query.value(2)

            # Проверяем, достаточно ли произведений искусства на складе
            if quantity < count:
                QMessageBox.information(self, "Info", "Недостаточное количество произведений искусства на складе")
                return

            # Рассчитываем итоговую сумму заказа
            total_main = price_main * count
            total_fraction = price_fraction * count

            # Учитываем перенос из дробной части в основную
            total_main += total_fraction // 100
            total_fraction %= 100

            # При нажатии на кнопку buy совершается покупка
            if QMessageBox.question(self, "Подтверждение", "Вы уверены, что хотите совершить покупку?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
                # Уменьшаем количество на складе
                # Проверяем, достаточно ли произведений искусства на складе
                if quantity < count:
                    QMessageBox.information(self, "Info", "Недостаточное количество произведений искусства на складе")
                    return
                new_quantity = quantity - count
                sqlstr = f"UPDATE artwork SET quantity = {new_quantity} WHERE title = '{artwork_title}'"
                if not query.exec_(sqlstr):
                    QMessageBox.critical(self, "Error", query.lastError().text())
                    return

                # Добавляем запись в таблицу operation
                sqlstr = f"INSERT INTO operation (artwork_id, amount_main, amount_fraction, quantity) VALUES ((SELECT id FROM artwork WHERE title = '{artwork_title}'), {total_main}, {total_fraction}, {count})"
                if not query.exec_(sqlstr):
                    QMessageBox.critical(self, "Error", query.lastError().text())
                    return

                # Получаем id только что добавленной операции
                operation_id = query.lastInsertId()

                # Добавляем запись в таблицу sale
                sqlstr = f"INSERT INTO sale (operation_id, customer_id) VALUES ({operation_id}, {self.customer_id})"
                if not query.exec_(sqlstr):
                    QMessageBox.critical(self, "Error", query.lastError().text())
                    return

                QMessageBox.information(self, "Info", "Покупка успешно совершена")

        else:
            QMessageBox.information(self, "Info", "Произведение искусства не найдено")

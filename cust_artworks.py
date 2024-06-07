from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QComboBox, QLineEdit, QMessageBox, QApplication, \
    QMainWindow, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi

from consts import global_customer_id


class CustArtworks(QMainWindow):
    def __init__(self, sign_in_window):  # добавьте sign_in_window в качестве аргумента
        super().__init__()
        self.customer_id = None
        loadUi("windows/customer_menu_data.ui", self)
        self.controller = None

        self.setWindowTitle('Все товары')

        sign_in_window.userSignedIn.connect(self.setCustomerId)  # Подключаем сигнал к слоту

        print(self.customer_id)
        # Заполнение QTypeBox
        self.alphabet.addItem("По возрастанию")
        self.alphabet.addItem("По убыванию")
        # Установка начального состояния для QTypeBox и QTableBox
        self.alphabet.setCurrentIndex(0)

        # Заполнение QTypeBox
        self.price.addItem("По возрастанию")
        self.price.addItem("По убыванию")
        # Установка начального состояния для QTypeBox и QTableBox
        self.price.setCurrentIndex(0)

        #
        # Заполнение QTableBox
        self.loadGenres()
        # Установка начального состояния для QTypeBox и QTableBox
        self.genre.setCurrentIndex(0)

        self.all.clicked.connect(self.print_all)
        self.alf_find.clicked.connect(self.print_alf_find)
        self.price_find.clicked.connect(self.print_price_find)
        self.genre_find.clicked.connect(self.print_genre_find)
        self.how_many.clicked.connect(self.print_how_many)

        self.artworks.cellClicked.connect(self.onCellClicked)
        self.sum.clicked.connect(self.sum_calculate)

        self.buy.clicked.connect(self.buy_artwork)

    def setCustomerId(self, customer_id):
        self.customer_id = customer_id

    def loadGenres(self):
        query = QSqlQuery()
        sqlstr = "SELECT genre_name FROM genre"
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        while query.next():
            genre_name = query.value(0)
            self.genre.addItem(genre_name)

    def onCellClicked(self, row, column):
        item = self.artworks.item(row, 0)  # получите элемент в первом столбце (название произведения искусства)
        if item is not None:
            artwork_title = item.text()
            self.name.setText(artwork_title)  # установите текст в поле name окна покупки

    def print_all(self):
        print(global_customer_id)
        # Очистить содержимое компонента
        self.artworks.setRowCount(0)

        # Установить количество столбцов
        self.artworks.setColumnCount(4)

        self.artworks.setHorizontalHeaderLabels(['Title', 'Artist Name', 'Price', 'Quantity'])

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

    def print_alf_find(self):
        # Очистить содержимое компонента
        self.artworks.setRowCount(0)

        # Установить количество столбцов
        self.artworks.setColumnCount(4)

        self.artworks.setHorizontalHeaderLabels(['Title', 'Artist Name', 'Price', 'Quantity'])

        # Растянуть столбцы, чтобы они занимали всю доступную ширину
        self.artworks.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Создать объект запроса
        query = QSqlQuery()

        # Определить порядок сортировки в зависимости от выбранного в QComboBox варианта
        order = "ASC" if self.alphabet.currentText() == "По возрастанию" else "DESC"

        # Создать строку запроса на выборку данных
        sqlstr = f"""
        SELECT artwork.title, artist.artist_name, artwork.price_main, artwork.quantity
        FROM artwork
        INNER JOIN artist ON artwork.artist_id = artist.id
        ORDER BY artwork.title {order}
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

    def print_price_find(self):
        # Очистить содержимое компонента
        self.artworks.setRowCount(0)

        # Установить количество столбцов
        self.artworks.setColumnCount(4)

        self.artworks.setHorizontalHeaderLabels(['Title', 'Artist Name', 'Price', 'Quantity'])

        # Растянуть столбцы, чтобы они занимали всю доступную ширину
        self.artworks.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Определить порядок сортировки в зависимости от выбранного в QComboBox варианта
        order = "ASC" if self.price.currentText() == "По возрастанию" else "DESC"

        # Создать объект запроса
        query = QSqlQuery()

        # Создать строку запроса на выборку данных
        sqlstr = f"""
        SELECT artwork.title, artist.artist_name, artwork.price_main, artwork.quantity
        FROM artwork
        INNER JOIN artist ON artwork.artist_id = artist.id
        ORDER BY artwork.price_main {order}
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

    def print_genre_find(self):
        # Очистить содержимое компонента
        self.artworks.setRowCount(0)

        # Установить количество столбцов
        self.artworks.setColumnCount(4)

        self.artworks.setHorizontalHeaderLabels(['Title', 'Artist Name', 'Price', 'Quantity'])

        # Растянуть столбцы, чтобы они занимали всю доступную ширину
        self.artworks.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Получить выбранный жанр
        selected_genre = self.genre.currentText()

        # Создать объект запроса
        query = QSqlQuery()

        # Создать строку запроса на выборку данных
        sqlstr = f"""
        SELECT artwork.title, artist.artist_name, artwork.price_main, artwork.quantity
        FROM artwork
        INNER JOIN artist ON artwork.artist_id = artist.id
        INNER JOIN artwork_genre ON artwork.id = artwork_genre.artwork_id
        INNER JOIN genre ON artwork_genre.genre_id = genre.id
        WHERE genre.genre_name = '{selected_genre}'
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

    def execute_query(self):
        query_type = self.QTypeBox.currentText()
        table = self.QTableBox.currentText()
        field = self.FieldInputline.text()
        value = self.ValueInputline.text()
        if query_type != "Join" and (not field or not value):
            QMessageBox.critical(self, "Error", "Field and Value cannot be empty")
            return

        limit = ""
        if self.LimitCheckBox.isChecked():
            limit_value = self.LimitInputLine.text()
            if not limit_value.isdigit():
                QMessageBox.critical(self, "Error", "Invalid limit format")
                return
            limit = f" LIMIT {limit_value}"

        if query_type == "Find":
            self.find_query(table, field, value, limit)
        elif query_type == "Filter":
            self.filter_query(table, field, value, limit)
        elif query_type == "Join":
            self.join_query(limit)
        else:
            QMessageBox.critical(self, "Error", "Invalid query type")
            return

    def display_query_results(self, query, table):
        # Очистка таблицы
        self.ResultTable.setRowCount(0)

        # Определение структуры таблицы в зависимости от выбранной таблицы
        if table == "artist":
            self.ResultTable.setColumnCount(4)
            self.ResultTable.setHorizontalHeaderLabels(["ID", "Artist Name", "Birth Date", "Death Date"])
        elif table == "artwork":
            self.ResultTable.setColumnCount(5)
            self.ResultTable.setHorizontalHeaderLabels(["ID", "Title", "Artist ID", "Price Main", "Price Fraction"])

        # Заполнение таблицы данными
        while query.next():
            row = self.ResultTable.rowCount()
            self.ResultTable.insertRow(row)
            for i in range(self.ResultTable.columnCount()):
                if table == "artist" and (i == 2 or i == 3):  # Если это дата рождения или дата смерти художника
                    date = query.value(i).toString("yyyy-MM-dd") if query.value(i) else ''
                    self.ResultTable.setItem(row, i, QTableWidgetItem(date))
                else:
                    self.ResultTable.setItem(row, i, QTableWidgetItem(str(query.value(i))))

    def find_query(self, table, field, value, limit):
        sqlstr = f"SELECT * FROM {table} WHERE {field} = '{value}'{limit}"
        query = QSqlQuery()
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return
        self.display_query_results(query, table)

    def filter_query(self, table, field, value, limit):
        sqlstr = f"SELECT * FROM {table} WHERE {field} LIKE '%{value}%'{limit}"
        query = QSqlQuery()
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return
        self.display_query_results(query, table)

    def join_query(self, limit):
        sqlstr = f"SELECT * FROM artist INNER JOIN artwork ON artist.id = artwork.artist_id{limit}"
        query = QSqlQuery()
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return
        self.display_query_results(query, "artist")

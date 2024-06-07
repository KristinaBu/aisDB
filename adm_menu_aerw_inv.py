from PyQt5.QtCore import pyqtSignal
from PyQt5.QtSql import QSqlQuery, QSqlError
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QComboBox, QLineEdit, QMessageBox, QApplication, \
    QMainWindow, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi



class AdminInventory(QMainWindow):
    clickArtw = pyqtSignal(int)  # Создаем новый сигнал, который передает целое число (ID пользователя)

    def __init__(self):  # добавьте sign_in_window в качестве аргумента
        super().__init__()
        self.controller = None

        self.selected_artwork_id = None

        loadUi("windows/admin_menu_artwork_inventory.ui", self)
        self.controller = None

        self.setWindowTitle('Все товары')

        # Заполнение QTypeBox
        self.alphabet.addItem("По возрастанию")
        self.alphabet.addItem("По убыванию")
        # Установка начального состояния для QTypeBox и QTableBox
        self.alphabet.setCurrentIndex(0)

        # Заполнение QTypeBox
        self.quant.addItem("По возрастанию")
        self.quant.addItem("По убыванию")
        # Установка начального состояния для QTypeBox и QTableBox
        self.quant.setCurrentIndex(0)

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

        # Заполнение QTableBox
        self.loadSuppls()
        # Установка начального состояния для QTypeBox и QTableBox
        self.comp.setCurrentIndex(0)

        self.all.clicked.connect(self.print_all)
        self.alf_find.clicked.connect(self.print_alf_find)
        self.price_find.clicked.connect(self.print_price_find)
        self.genre_find.clicked.connect(self.print_genre_find)
        self.quant_find.clicked.connect(self.print_quantity_find)
        self.find_but.clicked.connect(self.print_find)

        self.artworks.cellClicked.connect(self.onCellClicked)
        self.artworks_del.cellClicked.connect(self.onCellClicked_del)
        self.sum.clicked.connect(self.calculate_supply_cost)

        self.buy.clicked.connect(self.supply_artwork)
        self.back.clicked.connect(self.go_exit)

    def go_exit(self):
        self.close()

    def set_controller(self, controller):
        self.controller = controller
        self.exit.clicked.connect(self.controller.exit_all)
        self.edit.clicked.connect(self.controller.edit_artw)
        self.look.clicked.connect(self.controller.look_artw)
        self.artists.clicked.connect(self.controller.show_adm_artist)
        self.add_art.clicked.connect(self.controller.show_adm_artw)


    def loadGenres(self):
        query = QSqlQuery()
        sqlstr = "SELECT genre_name FROM genre"
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        while query.next():
            genre_name = query.value(0)
            self.genre.addItem(genre_name)

    def loadSuppls(self):
        query = QSqlQuery()
        sqlstr = "SELECT company_name FROM supplier"
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        while query.next():
            comp_name = query.value(0)
            self.comp.addItem(comp_name)

    def onCellClicked(self, row, column):
        item = self.artworks.item(row, 0)  # получите элемент в первом столбце (название произведения искусства)
        if item is not None:
            artwork_title = item.text()
            self.name.setText(artwork_title)  # установите текст в поле name окна покупки
            query = QSqlQuery()
            sqlstr = f"SELECT id FROM artwork WHERE title = '{artwork_title}';"

            if not query.exec_(sqlstr):
                QMessageBox.critical(self, "Error", query.lastError().text())
                return

            if query.next():
                artwork_id = query.value(0)  # Получите ID товара
                self.clickArtw.emit(artwork_id)
                print("id aert = ", artwork_id)
                self.selected_artwork_id = artwork_id

    def onCellClicked_del(self, row, column):
        item = self.artworks_del.item(row, 0)  # получите элемент в первом столбце (название произведения искусства)
        if item is not None:
            artwork_title = item.text()
            self.name.setText(artwork_title)  # установите текст в поле name окна покупки
            query = QSqlQuery()
            sqlstr = f"SELECT id FROM artwork WHERE title = '{artwork_title}';"

            if not query.exec_(sqlstr):
                QMessageBox.critical(self, "Error", query.lastError().text())
                return

            if query.next():
                artwork_id = query.value(0)  # Получите ID товара
                self.clickArtw.emit(artwork_id)
                print("id aert = ", artwork_id)
                self.selected_artwork_id = artwork_id



    def print_all(self):
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

    def print_quantity_find(self):
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
        order = "ASC" if self.quant.currentText() == "По возрастанию" else "DESC"

        # Создать строку запроса на выборку данных
        sqlstr = f"""
        SELECT artwork.title, artist.artist_name, artwork.price_main, artwork.quantity
        FROM artwork
        INNER JOIN artist ON artwork.artist_id = artist.id
        ORDER BY artwork.quantity {order}
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

    def print_find(self):
        # Получите строку поиска из поля QLineEdit
        search_str = self.name_del.text().lower()  # Преобразуйте строку поиска в нижний регистр

        # Очистить содержимое компонента
        self.artworks_del.setRowCount(0)

        # Установить количество столбцов
        self.artworks_del.setColumnCount(4)

        self.artworks_del.setHorizontalHeaderLabels(['Title', 'Artist Name', 'Price', 'Quantity'])

        # Растянуть столбцы, чтобы они занимали всю доступную ширину
        self.artworks_del.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Создать объект запроса
        query = QSqlQuery()

        # Создать строку запроса на выборку данных
        sqlstr = f"""
        SELECT artwork.title, artist.artist_name, artwork.price_main, artwork.quantity
        FROM artwork
        INNER JOIN artist ON artwork.artist_id = artist.id
        WHERE LOWER(artwork.title) LIKE '%{search_str}%'
        """

        # Выполнить запрос и проверить его успешность
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Прочитать в цикле все строки результата
        # и вывести их в компонент таблицы
        while query.next():
            row = self.artworks_del.rowCount()
            self.artworks_del.insertRow(row)
            self.artworks_del.setItem(row, 0, QTableWidgetItem(query.value(0)))
            self.artworks_del.setItem(row, 1, QTableWidgetItem(query.value(1)))
            self.artworks_del.setItem(row, 2, QTableWidgetItem(str(query.value(2))))
            self.artworks_del.setItem(row, 3, QTableWidgetItem(str(query.value(3))))

        self.artworks_del.resizeColumnsToContents()

    def calculate_supply_cost(self):
        # Считываем название произведения искусства из QLineEdit
        artwork_title = self.name.text()

        # Считываем количество из QSpinBox
        count = self.count.value()

        # Создаем объект запроса
        query = QSqlQuery()

        # Создаем строку запроса на выборку данных о произведении искусства
        sqlstr = f"SELECT price_main, price_fraction FROM artwork WHERE title = '{artwork_title}'"

        # Выполняем запрос и проверяем его успешность
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Если запрос вернул результат
        if query.next():
            price_main = query.value(0)
            price_fraction = query.value(1)

            # Рассчитываем итоговую сумму поставки
            total_main = price_main * count
            total_fraction = price_fraction * count

            # Учитываем перенос из дробной части в основную
            total_main += total_fraction // 100
            total_fraction %= 100

            # Выводим итоговую сумму поставки в поле sum_count
            self.sum_count.setText(f"{total_main}.{total_fraction:02d}")

    def supply_artwork(self):
        # Считываем название произведения искусства из QLineEdit
        artwork_title = self.name.text()

        # Считываем количество из QSpinBox
        count = self.count.value()

        # Считываем название компании-поставщика из QComboBox
        supplier_name = self.comp.currentText()

        # Создаем объект запроса
        query = QSqlQuery()

        # Создаем строку запроса на выборку данных о произведении искусства
        sqlstr = f"SELECT id, price_main, price_fraction, quantity FROM artwork WHERE title = '{artwork_title}'"

        # Выполняем запрос и проверяем его успешность
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Если запрос вернул результат
        if query.next():
            artwork_id = query.value(0)
            price_main = query.value(1)
            price_fraction = query.value(2)
            quantity = query.value(3)

            # Рассчитываем итоговую сумму поставки
            total_main = price_main * count
            total_fraction = price_fraction * count

            # Учитываем перенос из дробной части в основную
            total_main += total_fraction // 100
            total_fraction %= 100

            # Увеличиваем количество на складе
            new_quantity = quantity + count
            sqlstr = f"UPDATE artwork SET quantity = {new_quantity} WHERE id = {artwork_id}"
            if not query.exec_(sqlstr):
                QMessageBox.critical(self, "Error", query.lastError().text())
                return

            # Добавляем запись в таблицу operation
            sqlstr = f"INSERT INTO operation (artwork_id, amount_main, amount_fraction, quantity) VALUES ({artwork_id}, {total_main}, {total_fraction}, {count})"
            if not query.exec_(sqlstr):
                QMessageBox.critical(self, "Error", query.lastError().text())
                return

            # Получаем id только что добавленной операции
            operation_id = query.lastInsertId()

            # Получаем id поставщика
            sqlstr = f"SELECT id FROM supplier WHERE company_name = '{supplier_name}'"
            if not query.exec_(sqlstr):
                QMessageBox.critical(self, "Error", query.lastError().text())
                return

            if query.next():
                supplier_id = query.value(0)

                # Добавляем запись в таблицу purchase
                sqlstr = f"INSERT INTO purchase (operation_id, supplier_id) VALUES ({operation_id}, {supplier_id})"
                if not query.exec_(sqlstr):
                    QMessageBox.critical(self, "Error", query.lastError().text())
                    return

                QMessageBox.information(self, "Info",
                                        f"Поставка успешно совершена. Итоговая стоимость поставки: {total_main}.{total_fraction:02d}")

    def delete_artwork(self):
        # Получаем ID картины из таблицы artworks
        artwork_id = self.selected_artwork_id

        # Удаляем запись из таблицы artwork
        query = QSqlQuery()
        sqlstr = "DELETE FROM artwork WHERE id =?"
        query.prepare(sqlstr)
        query.addBindValue(artwork_id)
        if not query.exec_():
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Удаляем связи с жанрами
        sqlstr = "DELETE FROM artwork_genre WHERE artwork_id =?"
        query.prepare(sqlstr)
        query.addBindValue(artwork_id)
        if not query.exec_():
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

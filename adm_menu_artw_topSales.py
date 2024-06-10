from PyQt5.QtCore import pyqtSignal
from PyQt5.QtSql import QSqlQuery, QSqlError
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QComboBox, QLineEdit, QMessageBox, QApplication, \
    QMainWindow, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi



class AdmTopSales(QMainWindow):
    clickArtw = pyqtSignal(int)  # Создаем новый сигнал, который передает целое число (ID пользователя)

    def __init__(self):  # добавьте sign_in_window в качестве аргумента
        super().__init__()
        self.controller = None

        self.selected_artwork_id = None

        loadUi("windows/admin_menu_artwork_sales.ui", self)
        self.controller = None

        self.setWindowTitle('Все топы продаж')

        # Заполнение QTableBox
        self.loadSuppls()
        # Установка начального состояния для QTypeBox и QTableBox
        self.sel_comp.setCurrentIndex(0)

        self.alf_find.clicked.connect(self.top_selling_artworks)
        self.price_find.clicked.connect(self.bottom_selling_artworks)

        self.artworks.cellClicked.connect(self.onCellClicked)

        self.sum.clicked.connect(self.calculate_supply_cost)

        self.buy.clicked.connect(self.supply_artwork)
        self.back.clicked.connect(self.go_exit)

    def go_exit(self):
        self.close()

    def set_controller(self, controller):
        self.controller = controller
        self.exit.clicked.connect(self.controller.exit_all)

    def loadSuppls(self):
        query = QSqlQuery()
        sqlstr = "SELECT company_name FROM supplier"
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        while query.next():
            comp_name = query.value(0)
            self.sel_comp.addItem(comp_name)


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

                # Устанавливаем текст в поле name окна покупки
                self.name.setText(artwork_info)

                # Эмитируем сигнал clickArtw с artwork_id
                self.clickArtw.emit(artwork_id)

                print("ID произведения искусства = ", artwork_id)
                self.selected_artwork_id = artwork_id

                # Получаем и отображаем отзывы по artwork_id
                self.getReviews(artwork_id)

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


    def top_selling_artworks(self):
        # Очистить содержимое компонента
        self.artworks.setRowCount(0)

        # Установить количество столбцов
        self.artworks.setColumnCount(4)

        self.artworks.setHorizontalHeaderLabels(['Название', 'Число продаж', 'Общая сумма продаж', 'Ср. сумма 1 продажи'])

        # Растянуть столбцы, чтобы они занимали всю доступную ширину
        self.artworks.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Создать объект запроса
        query = QSqlQuery()

        # Создать строку запроса на выборку данных
        sqlstr = """
        SELECT artwork.title, COUNT(sale.id) AS sales_count, SUM(operation.amount_main) AS total_price, AVG(operation.amount_main) AS average_price
        FROM artwork
        LEFT JOIN operation ON artwork.id = operation.artwork_id
        LEFT JOIN sale ON operation.id = sale.operation_id
        GROUP BY artwork.id
        ORDER BY sales_count DESC
        LIMIT 10;
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
            self.artworks.setItem(row, 1, QTableWidgetItem(str(query.value(1))))
            self.artworks.setItem(row, 2, QTableWidgetItem(str(query.value(2))))
            self.artworks.setItem(row, 3, QTableWidgetItem(str(query.value(3))))

    def bottom_selling_artworks(self):
        # Очистить содержимое компонента
        self.artworks.setRowCount(0)

        # Установить количество столбцов
        self.artworks.setColumnCount(4)

        self.artworks.setHorizontalHeaderLabels(['Название', 'Число продаж', 'Общая сумма продаж', 'Ср. сумма 1 продажи'])

        # Растянуть столбцы, чтобы они занимали всю доступную ширину
        self.artworks.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Создать объект запроса
        query = QSqlQuery()

        # Создать строку запроса на выборку данных
        sqlstr = """
        SELECT artwork.title, COUNT(sale.id) AS sales_count, SUM(operation.amount_main) AS total_price, AVG(operation.amount_main + operation.amount_fraction) AS average_price
        FROM artwork
        LEFT JOIN operation ON artwork.id = operation.artwork_id
        LEFT JOIN sale ON operation.id = sale.operation_id
        GROUP BY artwork.id
        ORDER BY sales_count ASC
        LIMIT 10;
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
            self.artworks.setItem(row, 1, QTableWidgetItem(str(query.value(1))))
            self.artworks.setItem(row, 2, QTableWidgetItem(str(query.value(2))))
            self.artworks.setItem(row, 3, QTableWidgetItem(str(query.value(3))))


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

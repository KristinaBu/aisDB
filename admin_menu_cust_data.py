from PyQt5.QtCore import pyqtSignal
from PyQt5.QtSql import QSqlQuery, QSqlError
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QComboBox, QLineEdit, QMessageBox, QApplication, \
    QMainWindow, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi


class AdmCustData(QMainWindow):
    clickCustomer = pyqtSignal(int)  # Создаем новый сигнал, который передает целое число (ID пользователя)

    def __init__(self):  # добавьте sign_in_window в качестве аргумента
        super().__init__()
        self.controller = None

        self.selected_artwork_id = None
        self.customer_id = None

        loadUi("windows/admin_menu_customers_data.ui", self)
        self.controller = None

        self.setWindowTitle('Покупатели')



        self.all.clicked.connect(self.print_all_customers)

        self.customers.cellClicked.connect(self.onCellClicked)

        self.back.clicked.connect(self.go_exit)

    def go_exit(self):
        self.close()

    def set_controller(self, controller):
        self.controller = controller
        self.exit.clicked.connect(self.controller.exit_all)

    def onCellClicked(self, row, column):
        # Получаем элемент по указанным координатам
        item = self.customers.item(row, 0)

        if item is not None:
            # Извлекаем информацию из ячейки
            customer_name = item.text()

            # Предполагаем, что в первой колонке хранится имя клиента,
            # поэтому используем его для поиска ID клиента
            query = QSqlQuery()
            sqlstr = f"""
            SELECT c.id
            FROM customer c
            INNER JOIN person p ON c.person_id = p.id
            WHERE p.person_name = '{customer_name}';
            """

            if not query.exec_(sqlstr):
                QMessageBox.critical(self, "Error", query.lastError().text())
                return

            if query.next():
                customer_id = query.value(0)  # Получаем ID клиента

                # Эмитируем сигнал с customer_id
                self.clickCustomer.emit(customer_id)

                print("ID клиента = ", customer_id)
                self.customer_id = customer_id

                # Здесь можно добавить дополнительную логику, например, получить и отобразить детальную информацию о клиенте
                self.getReviews(customer_id)
                self.print_customer_purchases(customer_id)

    def print_all_customers(self):
        # Очистить содержимое компонента
        self.customers.setRowCount(0)

        # Установить количество столбцов
        self.customers.setColumnCount(3)

        self.customers.setHorizontalHeaderLabels(['Имя', 'Email', 'Адрес'])

        # Растянуть столбцы, чтобы они занимали всю доступную ширину
        self.customers.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Создать объект запроса
        query = QSqlQuery()

        # Создать строку запроса на выборку данных
        sqlstr = """
        SELECT p.person_name, p.email, a.street || ', ' || a.city || ', ' || a.region || ', ' || a.country || ', ' || a.zip_code AS address
        FROM customer c
        INNER JOIN person p ON c.person_id = p.id
        INNER JOIN address a ON p.address_id = a.id
        """

        # Выполнить запрос и проверить его успешность
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Прочитать в цикле все строки результата
        # и вывести их в компонент таблицы
        while query.next():
            row = self.customers.rowCount()
            self.customers.insertRow(row)
            self.customers.setItem(row, 0, QTableWidgetItem(str(query.value(0))))
            self.customers.setItem(row, 1, QTableWidgetItem(query.value(1)))
            self.customers.setItem(row, 2, QTableWidgetItem(query.value(2)))

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

    def print_customer_purchases(self, customer_id):
        # Очистить содержимое компонента
        self.purchases.setRowCount(0)

        # Установить количество столбцов
        self.purchases.setColumnCount(5)

        self.purchases.setHorizontalHeaderLabels(['Название', 'Основная сумма', 'Дробная сумма', 'Количество', 'Дата'])

        # Растянуть столбцы, чтобы они занимали всю доступную ширину
        self.purchases.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Создать объект запроса
        query = QSqlQuery()

        # Создать строку запроса на выборку данных
        sqlstr = f"""
        SELECT a.title, op.amount_main, op.amount_fraction, op.quantity, op.created_at
        FROM operation op
        INNER JOIN sale s ON op.id = s.operation_id
        INNER JOIN customer c ON s.customer_id = c.id
        INNER JOIN artwork a ON op.artwork_id = a.id
        WHERE c.id = {customer_id};
        """

        # Выполнить запрос и проверить его успешность
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Прочитать в цикле все строки результата
        # и вывести их в компонент таблицы
        while query.next():
            row = self.purchases.rowCount()
            self.purchases.insertRow(row)
            self.purchases.setItem(row, 0, QTableWidgetItem(query.value(0)))
            self.purchases.setItem(row, 1, QTableWidgetItem(str(query.value(1))))
            self.purchases.setItem(row, 2, QTableWidgetItem(str(query.value(2))))
            self.purchases.setItem(row, 3, QTableWidgetItem(str(query.value(3))))
            self.purchases.setItem(row, 4, QTableWidgetItem(query.value(4).toString('yyyy-MM-dd HH:mm:ss')))


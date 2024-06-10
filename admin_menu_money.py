from PyQt5.QtCore import pyqtSignal
from PyQt5.QtSql import QSqlQuery, QSqlError
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QComboBox, QLineEdit, QMessageBox, QApplication, \
    QMainWindow, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi


class AdmMoney(QMainWindow):
    clickSupplier = pyqtSignal(int)  # Создаем новый сигнал, который передает целое число (ID пользователя)

    def __init__(self):  # добавьте sign_in_window в качестве аргумента
        super().__init__()
        self.controller = None

        self.selected_artwork_id = None
        self.customer_id = None

        loadUi("windows/admin_menu_money.ui", self)
        self.controller = None

        self.setWindowTitle('Операции')


        self.print_all.clicked.connect(self.printAllOperations)
        self.print_s.clicked.connect(self.printSalesAndCustomersInfo)
        self.print_p.clicked.connect(self.printPurchasesAndSuppliersInfo)
        self.sum_s.clicked.connect(self.calculateTotalSaleAmount)
        self.sum_p.clicked.connect(self.calculateTotalPurchaseAmount)


        self.back.clicked.connect(self.go_exit)

    def go_exit(self):
        self.close()

    def set_controller(self, controller):
        self.controller = controller
        self.exit.clicked.connect(self.controller.exit_all)

    def printAllOperations(self):
        # Очистить содержимое компонента
        self.operationsTable.setRowCount(0)

        # Установить количество столбцов
        self.operationsTable.setColumnCount(6)

        self.operationsTable.setHorizontalHeaderLabels([
            'Произведение Искусства', 'Основная Сумма', 'Дробная Сумма', 'Количество', 'Дата', 'Тип'
        ])

        # Растянуть столбцы, чтобы они занимали всю доступную ширину
        self.operationsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Создать объект запроса
        query = QSqlQuery()

        # Создать строку запроса на выборку данных
        sqlstr = """
        SELECT a.title, op.amount_main, op.amount_fraction, op.quantity, op.created_at, 'Продажа' AS type
        FROM operation op
        INNER JOIN sale s ON op.id = s.operation_id
        INNER JOIN artwork a ON op.artwork_id = a.id
        UNION ALL
        SELECT a.title, op.amount_main, op.amount_fraction, op.quantity, op.created_at, 'Покупка' AS type
        FROM operation op
        INNER JOIN purchase pu ON op.id = pu.operation_id
        INNER JOIN artwork a ON op.artwork_id = a.id;
        """

        # Выполнить запрос и проверить его успешность
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Прочитать в цикле все строки результата
        # и вывести их в компонент таблицы
        while query.next():
            row = self.operationsTable.rowCount()
            self.operationsTable.insertRow(row)
            self.operationsTable.setItem(row, 0, QTableWidgetItem(query.value(0)))
            self.operationsTable.setItem(row, 1, QTableWidgetItem(str(query.value(1))))
            self.operationsTable.setItem(row, 2, QTableWidgetItem(str(query.value(2))))
            self.operationsTable.setItem(row, 3, QTableWidgetItem(str(query.value(3))))
            self.operationsTable.setItem(row, 4, QTableWidgetItem(query.value(4).toString('yyyy-MM-dd HH:mm:ss')))
            self.operationsTable.setItem(row, 5, QTableWidgetItem(query.value(5)))

    def printSalesAndCustomersInfo(self):
        # Очистить содержимое компонента
        self.salesTable.setRowCount(0)

        # Установить количество столбцов
        self.salesTable.setColumnCount(6)

        self.salesTable.setHorizontalHeaderLabels([
            'Произведение Искусства', 'Основная Сумма', 'Дробная Сумма', 'Количество', 'Дата', 'Клиент'
        ])

        # Растянуть столбцы, чтобы они занимали всю доступную ширину
        self.salesTable.resizeColumnsToContents()

        # Создать объект запроса
        query = QSqlQuery()

        # Создать строку запроса на выборку данных
        # Создать строку запроса на выборку данных
        sqlstr = """
        SELECT a.title, op.amount_main, op.amount_fraction, op.quantity, op.created_at, p.person_name
        FROM operation op
        INNER JOIN sale s ON op.id = s.operation_id
        INNER JOIN customer c ON s.customer_id = c.id
        INNER JOIN person p ON c.person_id = p.id
        INNER JOIN artwork a ON op.artwork_id = a.id;
        """

        # Выполнить запрос и проверить его успешность
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Прочитать в цикле все строки результата
        # и вывести их в компонент таблицы
        while query.next():
            row = self.salesTable.rowCount()
            self.salesTable.insertRow(row)
            self.salesTable.setItem(row, 0, QTableWidgetItem(query.value(0)))
            self.salesTable.setItem(row, 1, QTableWidgetItem(str(query.value(1))))
            self.salesTable.setItem(row, 2, QTableWidgetItem(str(query.value(2))))
            self.salesTable.setItem(row, 3, QTableWidgetItem(str(query.value(3))))
            self.salesTable.setItem(row, 4, QTableWidgetItem(query.value(4).toString('yyyy-MM-dd HH:mm:ss')))
            self.salesTable.setItem(row, 5, QTableWidgetItem(query.value(5)))

    def printPurchasesAndSuppliersInfo(self):
        # Очистить содержимое компонента
        self.purchasesTable.setRowCount(0)

        # Установить количество столбцов
        self.purchasesTable.setColumnCount(8)

        self.purchasesTable.setHorizontalHeaderLabels([
            'Произведение Искусства', 'Основная Сумма', 'Дробная Сумма', 'Количество', 'Дата', 'Поставщик', 'Компания',
            'Описание'
        ])

        # Растянуть столбцы, чтобы они занимали всю доступную ширину
        self.purchasesTable.resizeColumnsToContents()

        # Создать объект запроса
        query = QSqlQuery()

        # Создать строку запроса на выборку данных
        sqlstr = """
        SELECT a.title, op.amount_main, op.amount_fraction, op.quantity, op.created_at, s.company_name, s.about
        FROM operation op
        INNER JOIN purchase pu ON op.id = pu.operation_id
        INNER JOIN supplier s ON pu.supplier_id = s.id
        INNER JOIN artwork a ON op.artwork_id = a.id;
        """

        # Выполнить запрос и проверить его успешность
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Прочитать в цикле все строки результата
        # и вывести их в компонент таблицы
        while query.next():
            row = self.purchasesTable.rowCount()
            self.purchasesTable.insertRow(row)
            self.purchasesTable.setItem(row, 0, QTableWidgetItem(query.value(0)))
            self.purchasesTable.setItem(row, 1, QTableWidgetItem(str(query.value(1))))
            self.purchasesTable.setItem(row, 2, QTableWidgetItem(str(query.value(2))))
            self.purchasesTable.setItem(row, 3, QTableWidgetItem(str(query.value(3))))
            self.purchasesTable.setItem(row, 4, QTableWidgetItem(query.value(4).toString('yyyy-MM-dd HH:mm:ss')))
            self.purchasesTable.setItem(row, 5, QTableWidgetItem(query.value(5)))
            self.purchasesTable.setItem(row, 6, QTableWidgetItem(query.value(6)))
            self.purchasesTable.setItem(row, 7, QTableWidgetItem(query.value(7)))

    def calculateTotalSaleAmount(self):
        # Создать объект запроса
        query = QSqlQuery()

        # Создать строку запроса на выборку данных
        sqlstr = """
        SELECT SUM(op.amount_main + CAST(op.amount_fraction AS DECIMAL)) AS total_amount
        FROM operation op
        INNER JOIN sale s ON op.id = s.operation_id;
        """

        # Выполнить запрос и проверить его успешность
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Проверяем, есть ли результат
        if query.next():
            total_sale_amount = query.value(0)
            # Устанавливаем значение в QLineEdit
            self.totalSaleLineEdit.setText(str(total_sale_amount))
        else:
            # Если нет результатов, устанавливаем пустую строку
            self.totalSaleLineEdit.clear()

    def calculateTotalPurchaseAmount(self):
        # Создать объект запроса
        query = QSqlQuery()

        # Создать строку запроса на выборку данных
        sqlstr = """
        SELECT SUM(op.amount_main + CAST(op.amount_fraction AS DECIMAL)) AS total_amount
        FROM operation op
        INNER JOIN purchase pu ON op.id = pu.operation_id;
        """

        # Выполнить запрос и проверить его успешность
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Проверяем, есть ли результат
        if query.next():
            total_purchase_amount = query.value(0)
            # Устанавливаем значение в QLineEdit
            self.totalPurchaseLineEdit.setText(str(total_purchase_amount))
        else:
            # Если нет результатов, устанавливаем пустую строку
            self.totalPurchaseLineEdit.clear()


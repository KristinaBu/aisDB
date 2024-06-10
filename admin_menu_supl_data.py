from PyQt5.QtCore import pyqtSignal
from PyQt5.QtSql import QSqlQuery, QSqlError
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QComboBox, QLineEdit, QMessageBox, QApplication, \
    QMainWindow, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi


class AdmSuplData(QMainWindow):
    clickSupplier = pyqtSignal(int)  # Создаем новый сигнал, который передает целое число (ID пользователя)

    def __init__(self):  # добавьте sign_in_window в качестве аргумента
        super().__init__()
        self.controller = None

        self.selected_artwork_id = None
        self.customer_id = None

        loadUi("windows/admin_menu_suppliers_data.ui", self)
        self.controller = None

        self.setWindowTitle('Поставщики')

        # Заполнение QTypeBox
        self.alphabet.addItem("По возрастанию")
        self.alphabet.addItem("По убыванию")
        # Установка начального состояния для QTypeBox и QTableBox
        self.alphabet.setCurrentIndex(0)

        self.all.clicked.connect(self.print_all_suppliers)

        self.suppliers.cellClicked.connect(self.onSupplierCellClicked)

        self.back.clicked.connect(self.go_exit)

    def go_exit(self):
        self.close()

    def set_controller(self, controller):
        self.controller = controller
        self.exit.clicked.connect(self.controller.exit_all)

    def onSupplierCellClicked(self, row, column):
        # Получаем элемент по указанным координатам
        item = self.suppliers.item(row, 0)

        if item is not None:
            # Извлекаем информацию из ячейки
            supplier_name = item.text()

            # Предполагаем, что в первой колонке хранится название компании,
            # поэтому используем его для поиска ID поставщика
            query = QSqlQuery()
            sqlstr = f"""
            SELECT id
            FROM supplier
            WHERE company_name = '{supplier_name}';
            """

            if not query.exec_(sqlstr):
                QMessageBox.critical(self, "Error", query.lastError().text())
                return

            if query.next():
                supplier_id = query.value(0)  # Получаем ID поставщика

                # Эмитируем сигнал с supplier_id
                self.clickSupplier.emit(supplier_id)

                print("ID поставщика = ", supplier_id)
                self.supplier_id = supplier_id

                # Здесь можно добавить дополнительную логику, например, получить и отобразить детальную информацию о поставщике
                self.getSupplierPurchases(supplier_id)

    def print_all_suppliers(self):
        # Очистить содержимое компонента
        self.suppliers.setRowCount(0)

        # Установить количество столбцов
        self.suppliers.setColumnCount(2)

        self.suppliers.setHorizontalHeaderLabels(['Название компании', 'Описание'])

        # Растянуть столбцы, чтобы они занимали всю доступную ширину
        self.suppliers.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Создать объект запроса
        query = QSqlQuery()

        # Создать строку запроса на выборку данных
        sqlstr = """
        SELECT company_name, about
        FROM supplier;
        """

        # Выполнить запрос и проверить его успешность
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Прочитать в цикле все строки результата
        # и вывести их в компонент таблицы
        while query.next():
            row = self.suppliers.rowCount()
            self.suppliers.insertRow(row)
            self.suppliers.setItem(row, 0, QTableWidgetItem(query.value(0)))
            self.suppliers.setItem(row, 1, QTableWidgetItem(query.value(1)))
        self.suppliers.resizeColumnsToContents()

    def getSupplierPurchases(self, supplier_id):
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
        INNER JOIN purchase pu ON op.id = pu.operation_id
        INNER JOIN supplier s ON pu.supplier_id = s.id
        INNER JOIN artwork a ON op.artwork_id = a.id
        WHERE s.id = {supplier_id};
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


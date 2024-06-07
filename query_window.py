from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QComboBox, QLineEdit, QMessageBox, QApplication, \
    QMainWindow, QTableWidgetItem
from PyQt5.uic import loadUi


class QueryWindow(QMainWindow):
    def __init__(self, parent=None):
        super(QueryWindow, self).__init__(parent)
        loadUi('sign_in.ui', self)

        self.setWindowTitle("Sign In Window")

        # Заполнение QTypeBox
        #self.QTypeBox.addItem("Find")
        #self.QTypeBox.addItem("Filter")
        #self.QTypeBox.addItem("Join")
#
        # Заполнение QTableBox
        self.QTableBox.addItem("artist")
        self.QTableBox.addItem("artwork")
        self.QTableBox.addItem("both")

        # Подключение сигнала clicked кнопки QCreate к слоту execute_query
        self.QCreate.clicked.connect(self.execute_query)

        # Подключение сигнала currentTextChanged к слоту update_table_options
        self.QTypeBox.currentTextChanged.connect(self.update_table_options)

        # Установка начального состояния для QTypeBox и QTableBox
        self.QTypeBox.setCurrentIndex(0)  # "Find" будет выбрано по умолчанию

    def update_table_options(self, text):
        self.QTableBox.clear()
        if text == "Join":
            self.QTableBox.addItem("both")
            self.FieldInputline.setEnabled(False)
            self.ValueInputline.setEnabled(False)
        else:
            self.QTableBox.addItem("artist")
            self.QTableBox.addItem("artwork")
            self.FieldInputline.setEnabled(True)
            self.ValueInputline.setEnabled(True)

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
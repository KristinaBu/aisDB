from PyQt5.QtSql import QSqlQuery
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QComboBox, QLineEdit, QMessageBox, QApplication, \
    QMainWindow, QTableWidgetItem
from PyQt5.uic import loadUi



class AboutWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('windows/about_ais.ui', self)
        self.setWindowTitle('О системе')
        self.controller = None
        # инициализация окна

    def set_controller(self, controller):
        self.controller = controller
        self.back.clicked.connect(self.controller.show_main_window)

'''

class AboutWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        loadUi('windows/about_ais.ui', self)
        self.setWindowTitle('О системе')

        self.controller = controller
        # инициализация окна
        self.back.clicked.connect(self.controller.show_main_window)



        #self.back.clicked.connect(self.go_back)  # Вернуться назад при нажатии кнопки "Назад"

    def go_back(self):
        if self.main_window:
            self.main_window.show()  # Показать оригинальное окно MainWindow
        self.close()  # Закрыть это окно


'''


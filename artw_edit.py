from PyQt5.QtSql import QSqlQuery, QSqlError
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QComboBox, QLineEdit, QMessageBox, QApplication, \
    QMainWindow, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi



class ArtwEdit(QMainWindow):
    def __init__(self, artw_window):  # добавьте sign_in_window в качестве аргумента
        super().__init__()
        self.controller = None

        self.artwork_id = None
        loadUi("windows/adm_look.ui", self)
        self.controller = None

        self.setWindowTitle('Товар - редактирование')

        artw_window.clickArtw.connect(self.setArtworkID)  # Подключаем сигнал к слоту
        self.look.clicked.connect(self.loadArtworkInfo)
        self.save.clicked.connect(self.updateArtworkInfo)
        self.back.clicked.connect(self.go_exit)

    def go_exit(self):
        self.close()

    def set_controller(self, controller):
        self.controller = controller
        self.exit.clicked.connect(self.controller.exit_all)

    def setArtworkID(self, artwork_id):
        self.artwork_id = artwork_id
        print("id contr aert = ", artwork_id)

    def loadArtworkInfo(self, artwork_id):
        print("id load aert = ", self.artwork_id)
        query = QSqlQuery()
        sqlstr = f"""
        SELECT artwork.title, artist.artist_name, artwork.price_main, artwork.price_fraction, 
               STRING_AGG(genre.genre_name, ', ') as genres, artwork.quantity
        FROM artwork
        INNER JOIN artist ON artwork.artist_id = artist.id
        INNER JOIN artwork_genre ON artwork.id = artwork_genre.artwork_id
        INNER JOIN genre ON artwork_genre.genre_id = genre.id
        WHERE artwork.id = {self.artwork_id}
        GROUP BY artwork.id, artist.artist_name, artwork.price_main, artwork.price_fraction, artwork.quantity;
        """

        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        if query.next():
            artwork_title = query.value(0)  # Получите название произведения искусства
            artist_name = query.value(1)  # Получите имя художника
            price_main = query.value(2)  # Получите основную часть цены
            price_fraction = query.value(3)  # Получите дробную часть цены
            genres = query.value(4)  # Получите жанры
            quantity = query.value(5)  # Получите количество на складе

            # Заполните соответствующие поля QLineEdit
            self.name.setText(artwork_title)
            self.artist.setText(artist_name)
            self.pr1.setText(str(price_main))
            self.pr2.setText(str(price_fraction))
            self.genres.setText(genres)
            self.genres_2.setText(str(quantity))

    def updateArtworkInfo(self):
        # Получите обновленные данные из полей QLineEdit
        artwork_title = self.name.text()
        artist_name = self.artist.text()
        price_main = int(self.pr1.text())
        price_fraction = int(self.pr2.text())
        quantity = int(self.genres_2.text())

        # Создайте объект запроса
        query = QSqlQuery()

        # Создайте строку запроса на обновление данных
        sqlstr = f"""
        UPDATE artwork
        SET title = '{artwork_title}', price_main = {price_main}, price_fraction = {price_fraction}, quantity = {quantity}
        WHERE id = {self.artwork_id};
        """

        # Выполните запрос и проверьте его успешность
        if not query.exec_(sqlstr):
            QMessageBox.critical(self, "Error", query.lastError().text())
            return

        # Если запрос успешно выполнен, вы можете показать сообщение об успехе
        QMessageBox.information(self, "Success", "Данные обновлены")



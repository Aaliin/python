import sys
import os
import logging
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QMessageBox, QLabel, QFileDialog, QVBoxLayout, QWidget, QGridLayout,)
from PyQt6.QtGui import QPixmap

from iterator import ChoiceIterator
from csv_name import make_list, write_in_file
from new import write_in_new

logging.basicConfig(level=logging.INFO)


class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setGeometry(700, 200, 600, 350)
        self.setWindowTitle("Lab3-var3 main window")
        main_widget = QWidget()
        box_layout = QVBoxLayout()  # Размещает область в вертикальном столбце
        layout = QGridLayout()  # Упорядочивает в виде сетки из строк и столбцов

        self.dataset_path = os.path.abspath("dataset")
        src = QLabel(f"Путь к папке исходного датасета:\n{self.dataset_path}", self)
        src.setFixedSize(QSize(230, 40))
        box_layout.addWidget(src)
        src.setStyleSheet('color:blue')

        # установим кнопки
        self.annotation = self.add_button("Создать файл-аннотацию", 230, 30)
        self.bata_copy = self.add_button("Копирование датасета", 230, 30)
        self.bata_random = self.add_button("Датасет из радомных чисел", 230, 30)
        self.bata_iterator = self.add_button("Получение следующего экземпляра", 230, 30)
        self.next_cats = self.add_button("Следующая кошка", 230, 30)
        self.next_dogs = self.add_button("Следующая собака", 230, 30)
        self.exit = self.add_button("Выйти из программы", 230, 30)

        # установим изображение
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(300, 300)
        # масштабирует пиксельное изображение
        self.image_label.setScaledContents(True)

        # форматируем виджеты по размеру окна
        box_layout.addWidget(self.annotation)
        box_layout.addWidget(self.bata_copy)
        box_layout.addWidget(self.bata_random)
        box_layout.addWidget(self.bata_iterator)
        box_layout.addWidget(self.next_cats)
        box_layout.addWidget(self.next_dogs)
        box_layout.addWidget(self.exit)
        box_layout.addStretch() # кнопки вплотную
        layout.addLayout(box_layout, 0, 0)
        layout.addWidget(self.image_label, 0, 1)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        self.classes = ["cat", "dog"]
        self.choice_iterator = None
        self.image_path = None

        # то, что будет на экране при нажатии кнопки создания аннотации, копии и рандома
        self.annotation.clicked.connect(self.create_annotation)
        self.bata_copy.clicked.connect(self.copy)
        self.bata_random.clicked.connect(self.random)

        # то, что будет на экране при нажатии кнопки выход из программы
        self.exit.clicked.connect(self.close)

        self.show()

    def add_button(self, name: str, size_x: int, size_y: int) -> QPushButton:
        '''принимает название поля кнопки и ее размеры'''
        button = QPushButton(name, self)  # Виджет кнопок, на который пользователь может нажать
        # Возвращает измененную копию этого изображения (возвращает объект QSize)
        button.resize(button.sizeHint())
        button.setStyleSheet('color:blue')
        button.setFixedSize(QSize(size_x, size_y))
        return button

    def create_copy_random(self, number: int) -> None:
        '''создаем csv-файл по указанному пути; копируем данные с новым именем'''
        try:
            directory = QFileDialog.getSaveFileName(
                self,
                "Введите название папки для создания csv-файла:",
            )[0]
            if directory == "":
                QMessageBox.information(None, "Ошибка работы программы!", "Не правильно выбрана папка")
                return
            if number == 0 or number == 1:
                write_in_new(self.dataset_path, self.classes, directory, number)
            else:
                a = make_list(self.dataset_path, self.classes)
                write_in_file(a, directory)
            QMessageBox.information(None, "Результат нажатия книпки", "Датасет успешно скопирован!")
        except Exception as ex:
            logging.error(f"Couldn't create copy: {ex.message}\n{ex.args}\n")

    def create_annotation(self) -> None:
        self.create_copy_random(7)

    def copy(self) -> None:
        self.create_copy_random(0)

    def random(self) -> None:
        self.create_copy_random(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    app.exec()

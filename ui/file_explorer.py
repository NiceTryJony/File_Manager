from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeView, QFileSystemModel, QHBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt

class FileExplorer(QWidget):
    def __init__(self):
        super().__init__()

        # Основной макет
        layout = QVBoxLayout(self)

        # Модель для отображения файловой системы
        self.model = QFileSystemModel()
        self.model.setRootPath('')

        # Виджет для отображения файловой системы
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(''))
        self.tree_view.setColumnWidth(0, 250)

        # Добавляем дерево файлов в макет
        layout.addWidget(self.tree_view)

        # Панель инструментов с кнопками
        toolbar = QHBoxLayout()

        self.open_button = QPushButton("Open File")
        self.open_button.clicked.connect(self.open_file)

        self.delete_button = QPushButton("Delete File")
        self.delete_button.clicked.connect(self.delete_file)

        self.import_button = QPushButton("Import File")
        self.import_button.clicked.connect(self.import_file)

        toolbar.addWidget(self.open_button)
        toolbar.addWidget(self.delete_button)
        toolbar.addWidget(self.import_button)

        layout.addLayout(toolbar)

    def open_file(self):
        index = self.tree_view.currentIndex()
        if index.isValid():
            file_path = self.model.filePath(index)
            # Открытие файла: здесь можно добавить терминал или вывод логов.
            print(f"Opening file: {file_path}")

    def delete_file(self):
        index = self.tree_view.currentIndex()
        if index.isValid():
            file_path = self.model.filePath(index)
            # Удаление файла
            print(f"Deleting file: {file_path}")

    def import_file(self):
        file_dialog = QFileDialog.getOpenFileName(self, "Select File")
        if file_dialog[0]:
            # Импорт файла: просто показать путь, можно добавить логику копирования
            print(f"Importing file: {file_dialog[0]}")

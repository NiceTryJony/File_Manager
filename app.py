from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Создаем главное окно
    window = MainWindow()
    window.show()

    # Запуск приложения
    sys.exit(app.exec_())


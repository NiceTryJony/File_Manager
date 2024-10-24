import sys
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTabWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt
from services.cpu_monitor import CPUMonitor
from services.ram_monitor import RAMMonitor
from services.gpu_monitor import GpuMonitor
from ui.file_explorer import FileExplorer
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Устанавливаем размеры окна
        self.setWindowTitle("Cyber File Manager")
        self.setGeometry(100, 100, 1000, 750)

        # Основной виджет с вкладками
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Добавляем вкладку для мониторинга ресурсов
        resource_tab = QWidget()
        self.tabs.addTab(resource_tab, "System Monitor")
        self.setup_resource_monitor(resource_tab)

        # Добавляем вкладку для файлового менеджера
        file_tab = FileExplorer()
        self.tabs.addTab(file_tab, "File Explorer")

        # Настройка стилей
        self.setStyleSheet(self.light_theme())  # Устанавливаем темную тему

        # Запуск мониторинга
        self.start_monitors()

    def create_plot(self, title, resource):
        """Создаем график для ресурса."""
        fig, ax = plt.subplots()
        ax.set_title(title)
        ax.set_ylim(0, 100)  # Устанавливаем диапазон от 0 до 100%
        ax.set_xlim(0, 100)  # Ограничиваем ось X до 100 значений
        line, = ax.plot([], [], linewidth=2)  # Создаем пустую линию

        canvas = FigureCanvas(fig)
        return fig, canvas, line, ax  # Возвращаем три значения

    def setup_resource_monitor(self, widget):
        """Создаем вкладку мониторинга системы."""
        layout = QVBoxLayout(widget)

        # Создаем графики для CPU, RAM и GPU
        self.cpu_fig, self.cpu_canvas, self.cpu_line, self.cpu_ax = self.create_plot("CPU Usage in %", "CPU")
        self.ram_fig, self.ram_canvas, self.ram_line, self.ram_ax = self.create_plot("RAM Usage in %", "RAM")
        self.gpu_fig, self.gpu_canvas, self.gpu_line, self.gpu_ax = self.create_plot("GPU Usage in %", "GPU")

        # Добавляем графики в макет
        layout.addWidget(self.cpu_canvas)
        layout.addWidget(self.ram_canvas)
        layout.addWidget(self.gpu_canvas)

        # Кнопка для переключения тем
        toggle_button = QPushButton("Toggle Theme")
        toggle_button.clicked.connect(self.toggle_theme)
        layout.addWidget(toggle_button)

        # Метка для отображения информации
        self.info_label = QLabel("Monitoring CPU, RAM, and GPU usage...")
        layout.addWidget(self.info_label)

    def start_monitors(self):
        """Запуск мониторинга CPU, RAM и GPU."""
        self.cpu_monitor = CPUMonitor(self.update_cpu_usage)
        self.cpu_monitor.cpu_usage_signal.connect(self.update_cpu_usage)
        self.cpu_monitor.start()

        self.ram_monitor = RAMMonitor(self.update_ram_usage)
        self.ram_monitor.ram_usage_signal.connect(self.update_ram_usage)
        self.ram_monitor.start()

        self.gpu_monitor = GpuMonitor(self.update_gpu_usage)
        self.gpu_monitor.gpu_usage_signal.connect(self.update_gpu_usage)
        self.gpu_monitor.start()

        # Инициализация данных
        self.cpu_data = []
        self.ram_data = []
        self.gpu_data = []

    def update_cpu_usage(self, usage):
        """Обновление данных графика CPU."""
        self.cpu_data.append(usage)
        if len(self.cpu_data) > 100:
            self.cpu_data = self.cpu_data[-100:]  # Ограничение длины данных

        y_data = self.smooth_data(self.cpu_data)  # Сглаженные данные
        x_data = range(len(y_data))  # Обновляем ось X по длине Y

        # Обновляем данные линии
        self.cpu_ax.lines[0].set_xdata(x_data)
        self.cpu_ax.lines[0].set_ydata(y_data)

        # Обновляем границы оси X
        self.cpu_ax.set_xlim(0, len(self.cpu_data))  # Ограничиваем ось X по длине оригинальных данных

        # Обновляем график
        self.cpu_fig.canvas.draw()
        self.info_label.setText(f"CPU Usage: {usage}%")

    def update_ram_usage(self, usage):
        """Обновление данных графика RAM."""
        self.ram_data.append(usage)
        if len(self.ram_data) > 100:
            self.ram_data = self.ram_data[-100:]

        y_data = self.smooth_data(self.ram_data)
        x_data = range(len(y_data))

        self.ram_ax.lines[0].set_xdata(x_data)
        self.ram_ax.lines[0].set_ydata(y_data)
        self.ram_ax.set_xlim(0, len(self.ram_data))

        self.ram_fig.canvas.draw()
        self.info_label.setText(f"RAM Usage: {usage}%")

    def update_gpu_usage(self, usage):
        """Обновление данных графика GPU."""
        self.gpu_data.append(usage)
        if len(self.gpu_data) > 100:
            self.gpu_data = self.gpu_data[-100:]

        y_data = self.smooth_data(self.gpu_data)
        x_data = range(len(y_data))

        self.gpu_ax.lines[0].set_xdata(x_data)
        self.gpu_ax.lines[0].set_ydata(y_data)
        self.gpu_ax.set_xlim(0, len(self.gpu_data))

        self.gpu_fig.canvas.draw()
        self.info_label.setText(f"GPU Usage: {usage}%")



    def smooth_data(self, data):
        """Применяем скользящее среднее для сглаживания данных."""
        if len(data) < 5:
            return data
        return np.convolve(data, np.ones(5) / 5, mode='valid')

    def toggle_theme(self):
        """Переключение между темной и светлой темами."""
        if self.styleSheet() == self.dark_theme():
            self.setStyleSheet(self.light_theme())
        else:
            self.setStyleSheet(self.dark_theme())

    def dark_theme(self):
        """Темная тема."""
        return """
            QMainWindow {
                background-color: #2e2e2e;
            }
            QTabWidget::pane {
                border: 2px solid #00bfff;
                padding: 5px;
            }
            QTabBar::tab {
                background: #2e2e2e;
                border: 1px solid #00bfff;
                padding: 10px;
            }
            QTabBar::tab:selected {
                background: #00bfff;
                color: white;
            }
        """

    def light_theme(self):
        """Светлая тема."""
        return """
            QMainWindow {
                background-color: #ffffff;
            }
            QTabWidget::pane {
                border: 2px solid #007acc;
                padding: 5px;
            }
            QTabBar::tab {
                background: #f0f0f0;
                border: 1px solid #007acc;
                padding: 10px;
            }
            QTabBar::tab:selected {
                background: #007acc;
                color: white;
            }
        """

# )import pyqtgraph as pg
# from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTabWidget, QPushButton, QLabel
# from PyQt5.QtCore import Qt
# from services.cpu_monitor import CPUMonitor
# from services.ram_monitor import RAMMonitor
# from services.gpu_monitor import GpuMonitor
# from ui.file_explorer import FileExplorer
# import numpy as np

# )class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # Устанавливаем размеры окна
#         self.setWindowTitle("Cyber File Manager")
#         self.setGeometry(100, 100, 900, 600)

#         # Основной виджет с вкладками
#         self.tabs = QTabWidget()
#         self.setCentralWidget(self.tabs)

#         # Добавляем вкладку для мониторинга ресурсов
#         resource_tab = QWidget()
#         self.tabs.addTab(resource_tab, "System Monitor")
#         self.setup_resource_monitor(resource_tab)

#         # Добавляем вкладку для файлового менеджера
#         file_tab = FileExplorer()
#         self.tabs.addTab(file_tab, "File Explorer")

#         # Настройка стилей
#         self.setStyleSheet(self.dark_theme())  # Устанавливаем темную тему

#         # Запуск мониторинга
#         self.start_monitors()

#     def setup_resource_monitor(self, widget):
#         """Создаем вкладку мониторинга системы."""
#         layout = QVBoxLayout(widget)

#         # График для CPU
#         self.cpu_plot = pg.PlotWidget(title="CPU Usage in %", background='#2e2e2e')
#         self.cpu_curve = self.cpu_plot.plot(pen='y', width=2)  # Жёлтая линия
#         self.cpu_data = []

#         # График для RAM
#         self.ram_plot = pg.PlotWidget(title="RAM Usage in %", background='#2e2e2e')
#         self.ram_curve = self.ram_plot.plot(pen='b', width=2)  # Синяя линия
#         self.ram_data = []

#         # График для GPU
#         self.gpu_plot = pg.PlotWidget(title="GPU Usage in %", background='#2e2e2e')
#         self.gpu_curve = self.gpu_plot.plot(pen='r', width=2)  # Красная линия
#         self.gpu_data = []

#         # Добавляем графики в макет
#         layout.addWidget(self.cpu_plot)
#         layout.addWidget(self.ram_plot)
#         layout.addWidget(self.gpu_plot)

#         # Кнопка для переключения тем
#         toggle_button = QPushButton("Toggle Theme")
#         toggle_button.clicked.connect(self.toggle_theme)
#         layout.addWidget(toggle_button)

#         # Метка для отображения информации
#         self.info_label = QLabel("Monitoring CPU, RAM, and GPU usage...")
#         layout.addWidget(self.info_label)

#     def start_monitors(self):
#         """Запуск мониторинга CPU, RAM и GPU."""
#         self.cpu_monitor = CPUMonitor(self.update_cpu_usage)
#         self.cpu_monitor.cpu_usage_signal.connect(self.update_cpu_usage)
#         self.cpu_monitor.start()

#         self.ram_monitor = RAMMonitor(self.update_ram_usage)
#         self.ram_monitor.ram_usage_signal.connect(self.update_ram_usage)
#         self.ram_monitor.start()

#         self.gpu_monitor = GpuMonitor(self.update_gpu_usage)
#         self.gpu_monitor.gpu_usage_signal.connect(self.update_gpu_usage)
#         self.gpu_monitor.start()

#     def update_cpu_usage(self, usage):
#         """Обновление данных графика CPU."""
#         self.cpu_data.append(usage)
#         if len(self.cpu_data) > 100:
#             self.cpu_data = self.cpu_data[-100:]  # Ограничение длины данных
#         self.cpu_curve.setData(self.smooth_data(self.cpu_data))
#         self.info_label.setText(f"CPU Usage: {usage}%")

#     def update_ram_usage(self, usage):
#         """Обновление данных графика RAM."""
#         self.ram_data.append(usage)
#         if len(self.ram_data) > 100:
#             self.ram_data = self.ram_data[-100:]
#         self.ram_curve.setData(self.smooth_data(self.ram_data))
#         self.info_label.setText(f"RAM Usage: {usage}%")

#     def update_gpu_usage(self, usage):
#         """Обновление данных графика GPU."""
#         self.gpu_data.append(usage)
#         if len(self.gpu_data) > 100:
#             self.gpu_data = self.gpu_data[-100:]
#         self.gpu_curve.setData(self.smooth_data(self.gpu_data))
#         self.info_label.setText(f"GPU Usage: {usage}%")

#     def smooth_data(self, data):
#         """Применяем скользящее среднее для сглаживания данных."""
#         if len(data) < 5:
#             return data
#         return np.convolve(data, np.ones(5) / 5, mode='valid')

#     def toggle_theme(self):
#         """Переключение между темной и светлой темами."""
#         if self.styleSheet() == self.dark_theme():
#             self.setStyleSheet(self.light_theme())
#         else:
#             self.setStyleSheet(self.dark_theme())

#     def dark_theme(self):
#         """Темная тема."""
#         return """
#             QMainWindow {
#                 background-color: #1e1e1e;
#             }
#             QTabWidget::pane {
#                 border: 2px solid #00bfff;
#                 padding: 5px;
#             }
#             QTabBar::tab {
#                 background: #2e2e2e;
#                 border: 1px solid #00bfff;
#                 padding: 10px;
#             }
#             QTabBar::tab:selected {
#                 background: #00bfff;
#                 color: white;
#             }
#         """

#     def light_theme(self):
#         """Светлая тема."""
#         return """
#             QMainWindow {
#                 background-color: #ffffff;
#             }
#             QTabWidget::pane {
#                 border: 2px solid #007acc;
#                 padding: 5px;
#             }
#             QTabBar::tab {
#                 background: #f0f0f0;
#                 border: 1px solid #007acc;
#                 padding: 10px;
#             }
#             QTabBar::tab:selected {
#                 background: #007acc;
#                 color: white;
#             }
#         """

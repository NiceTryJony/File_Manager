from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from services.cpu_monitor import CPUMonitor
from services.ram_monitor import RAMMonitor
from services.gpu_monitor import GPUMonitor

class ResourceMonitorWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # CPU Monitor
        self.cpu_label = QLabel("CPU Usage: ")
        self.cpu_bar = QProgressBar()
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.cpu_bar)

        # RAM Monitor
        self.ram_label = QLabel("RAM Usage: ")
        self.ram_bar = QProgressBar()
        layout.addWidget(self.ram_label)
        layout.addWidget(self.ram_bar)

        # GPU Monitor (если есть)
        self.gpu_label = QLabel("GPU Usage: ")
        self.gpu_bar = QProgressBar()
        layout.addWidget(self.gpu_label)
        layout.addWidget(self.gpu_bar)

        self.setLayout(layout)

        # Инициализируем потоки мониторинга
        self.cpu_monitor = CPUMonitor(self.update_cpu)
        self.ram_monitor = RAMMonitor(self.update_ram)
        self.gpu_monitor = GPUMonitor(self.update_gpu)

        # Запускаем потоки мониторинга
        self.cpu_monitor.start()
        self.ram_monitor.start()
        self.gpu_monitor.start()

    def update_cpu(self, value):
        self.cpu_label.setText(f"CPU Usage: {value:.2f}%")
        self.cpu_bar.setValue(int(value))

    def update_ram(self, value):
        self.ram_label.setText(f"RAM Usage: {value:.2f}%")
        self.ram_bar.setValue(int(value))

    def update_gpu(self, value):
        self.gpu_label.setText(f"GPU Usage: {value:.2f}%")
        self.gpu_bar.setValue(int(value))

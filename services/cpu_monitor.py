import time
import psutil
from PyQt5.QtCore import QThread, pyqtSignal

class CPUMonitor(QThread):
    cpu_usage_signal = pyqtSignal(float)

    def __init__(self, callback=None):
        super().__init__()
        if callback:
            self.cpu_usage_signal.connect(callback)

    def run(self):
        """Постоянно передает процент загрузки CPU."""
        while True:
            usage = psutil.cpu_percent(interval=0.1)  # Использование CPU
            self.cpu_usage_signal.emit(usage)  # Передаем три значения
            time.sleep(0.1)
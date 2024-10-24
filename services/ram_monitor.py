# ram_monitor.py
import psutil
import time
from PyQt5.QtCore import QThread, pyqtSignal

class RAMMonitor(QThread):
    ram_usage_signal = pyqtSignal(float)

    def __init__(self, callback=None):
        super().__init__()
        if callback:
            self.ram_usage_signal.connect(callback)

    def run(self):
        """Постоянно передает процент использования RAM."""
        while True:
            ram_usage = psutil.virtual_memory().percent
            self.ram_usage_signal.emit(ram_usage)
            time.sleep(1)
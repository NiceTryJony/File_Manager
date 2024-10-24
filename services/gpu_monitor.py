# gpu_monitor.py
import GPUtil
import time
from PyQt5.QtCore import QThread, pyqtSignal

class GpuMonitor(QThread):
    gpu_usage_signal = pyqtSignal(float)

    def __init__(self, callback=None):
        super().__init__()
        if callback:
            self.gpu_usage_signal.connect(callback)

    def run(self):
        """Постоянно передает процент использования GPU."""
        while True:
            gpu = GPUtil.getGPUs()
            if gpu:
                usage = gpu[0].load * 100  # Используем первую доступную GPU
                self.gpu_usage_signal.emit(usage)
                time.sleep(1)
            else:
                self.gpu_usage_signal.emit(0.0)

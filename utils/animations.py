from PyQt5.QtCore import QPropertyAnimation

def create_animation(widget, value, duration=400):
    animation = QPropertyAnimation(widget, b"value")
    animation.setDuration(duration)
    animation.setEndValue(value)
    return animation

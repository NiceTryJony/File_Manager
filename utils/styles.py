def apply_styles(window):
    """Применение глобальных стилей для всего приложения"""
    window.setStyleSheet("""
        QMainWindow {
            background-color: #1e1e1e;
        }
        QLabel {
            color: #00ffcc;
            font-size: 14pt;
        }
        QProgressBar {
            background-color: #2e2e2e;
            border: 2px solid #3e3e3e;
            height: 20px;
            border-radius: 10px;
            text-align: center;
            color: #ffffff;
        }
        QProgressBar::chunk {
            background-color: #ff007f;
            width: 10px;
            margin: 1px;
        }
        QTreeView {
            background-color: #232323;
            color: #00ffcc;
            border: 1px solid #3e3e3e;
            font-size: 12pt;
        }
    """)

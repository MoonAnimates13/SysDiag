# main.py
import sys
from PyQt6.QtWidgets import QApplication
from ui.ui_main import MainWindow

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())

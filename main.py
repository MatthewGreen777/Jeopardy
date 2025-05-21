from PySide6.QtWidgets import QApplication
import sys
from main_menu import JeopardyApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JeopardyApp()
    window.show()
    sys.exit(app.exec())

import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox,
    QScrollArea, QFrame
)
from PySide6.QtCore import Qt
from util import get_user_data_path
from util import get_resource_path

class EditFinalSelectPage(QWidget):
    def __init__(self, load_callback, back_callback):
        super().__init__()
        self.load_callback = load_callback
        self.back_callback = back_callback
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)

        title = QLabel("Select a Final Jeopardy Question to Edit")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(title)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")

        scroll_content = QFrame()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(10)

        finals_dir = get_user_data_path("finals")
        if not os.path.isdir(finals_dir):
            QMessageBox.warning(self, "Error", f"Finals directory not found: {finals_dir}")
            return

        final_files = [f for f in os.listdir(finals_dir) if f.endswith(".csv")]

        if not final_files:
            label = QLabel("No final Jeopardy questions available.")
            label.setAlignment(Qt.AlignCenter)
            scroll_layout.addWidget(label)
        else:
            for final_file in final_files:
                button = QPushButton(final_file)
                button.setFixedHeight(40)
                button.setStyleSheet("""
                    QPushButton {
                        border: 2px solid white;
                        color: white;
                        font-size: 16px;
                        background-color: transparent;
                    }
                    QPushButton:hover {
                        background-color: #72729c;
                    }
                """)
                button.clicked.connect(lambda checked, f=final_file: self.select_final(f))
                scroll_layout.addWidget(button)

        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        back_button = QPushButton("Return to Main Menu")
        back_button.setFixedHeight(40)
        back_button.setStyleSheet("""
            QPushButton {
                border: 2px solid white;
                color: white;
                font-size: 16px;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #72729c;
            }
        """)
        back_button.clicked.connect(self.back_callback)
        main_layout.addWidget(back_button)

    def select_final(self, filename):
        finals_dir = get_user_data_path("finals")
        filepath = os.path.join(finals_dir, filename)
        self.load_callback(filepath)

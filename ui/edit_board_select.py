import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox,
    QScrollArea, QFrame
)
from PySide6.QtCore import Qt

class EditBoardSelectPage(QWidget):
    def __init__(self, load_board_callback, return_to_menu_callback):
        super().__init__()
        self.load_board_callback = load_board_callback
        self.return_to_menu_callback = return_to_menu_callback
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)

        title = QLabel("Select a Board to Edit")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(title)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")

        scroll_content = QFrame()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(10)

        boards_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "boards"))
        if not os.path.isdir(boards_dir):
            QMessageBox.warning(self, "Error", f"Boards directory not found: {boards_dir}")
            return

        board_files = [f for f in os.listdir(boards_dir) if f.endswith(".csv")]

        if not board_files:
            label = QLabel("No boards available.")
            label.setAlignment(Qt.AlignCenter)
            scroll_layout.addWidget(label)
        else:
            for board_file in board_files:
                button = QPushButton(board_file)
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
                button.clicked.connect(lambda checked, f=board_file: self.select_board(f))
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
        back_button.clicked.connect(self.return_to_menu_callback)
        main_layout.addWidget(back_button)

    def select_board(self, filename):
        boards_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "boards"))
        filepath = os.path.join(boards_dir, filename)
        self.load_board_callback(filepath)

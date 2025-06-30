# game_select_screen.py
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QScrollArea, QFrame
)
from PySide6.QtCore import Qt

class GameSelectScreen(QWidget):
    def __init__(self, load_game_callback, return_callback):
        super().__init__()
        self.load_game_callback = load_game_callback
        self.return_callback = return_callback
        self.scroll_layout = None  # Will be assigned in init_ui
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        title = QLabel("Select a Jeopardy Game")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QFrame()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(10)

        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)

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
        back_button.clicked.connect(self.return_callback)
        layout.addWidget(back_button)

        self.refresh_game_list()  # Initial load

    def refresh_game_list(self):
        # Clear old buttons
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        games_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "games"))
        if not os.path.isdir(games_dir):
            QMessageBox.warning(self, "Error", f"Games directory not found: {games_dir}")
            return

        game_folders = [f for f in os.listdir(games_dir) if os.path.isdir(os.path.join(games_dir, f))]

        if not game_folders:
            label = QLabel("No games available.")
            label.setAlignment(Qt.AlignCenter)
            self.scroll_layout.addWidget(label)
        else:
            for folder in game_folders:
                button = QPushButton(folder)
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
                button.clicked.connect(lambda _, f=folder: self.select_game(f))
                self.scroll_layout.addWidget(button)

    def select_game(self, folder):
        games_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "games"))
        full_path = os.path.join(games_dir, folder)
        self.load_game_callback(full_path)

    def showEvent(self, event):
        super().showEvent(event)
        self.refresh_game_list()

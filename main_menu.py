from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QStackedLayout
)
from PySide6.QtCore import Qt
import os

# Import the different pages used in the Jeopardy app
from ui.create_board import CreateBoardPage
from ui.create_final import CreateFinalPage
from ui.create_game import CreateGamePage
from ui.edit_board import EditBoardPage
from ui.edit_final import EditFinalPage
from ui.play_game import PlayGamePage
from ui.edit_board_select import EditBoardSelectPage
from ui.edit_final_select import EditFinalSelectPage
from ui.select_game import GameSelectScreen


class JeopardyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jeopardy App")
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        self.stack = QStackedLayout()
        self.main_layout.addLayout(self.stack)

        # Create pages
        self.menu_page = self.create_main_menu()
        self.create_board_page = CreateBoardPage(self.return_to_menu)
        self.create_final_page = CreateFinalPage(self.return_to_menu)
        self.edit_board_page = EditBoardPage(self.return_to_menu)
        self.edit_final_page = EditFinalPage(self.return_to_menu)
        self.play_game_page = PlayGamePage(self.return_to_menu)

        # Create game page, with file-select callbacks
        self.create_game_page = CreateGamePage(
            self.return_to_menu,
            self.show_edit_board_select_for_game,
            self.show_edit_final_select_for_game
        )

        # Create game select screen
        self.game_select_screen = GameSelectScreen(
            load_game_callback=self.load_selected_game,
            return_callback=self.return_to_menu
        )

        # Add static pages to the stack
        self.stack.addWidget(self.menu_page)
        self.stack.addWidget(self.create_board_page)
        self.stack.addWidget(self.create_final_page)
        self.stack.addWidget(self.create_game_page)
        self.stack.addWidget(self.edit_board_page)
        self.stack.addWidget(self.edit_final_page)
        self.stack.addWidget(self.play_game_page)
        self.stack.addWidget(self.game_select_screen)

        self.showMaximized()
        self.setStyleSheet("background-color: #060CE9;")

    def create_main_menu(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)

        title = QLabel("Jeopardy Game Manager")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(title)

        buttons = {
            "Play Jeopardy Game": self.show_game_select_screen,
            "Create Jeopardy Board": lambda: self.stack.setCurrentWidget(self.create_board_page),
            "Create Final Jeopardy Question": lambda: self.stack.setCurrentWidget(self.create_final_page),
            "Create Jeopardy Game": lambda: self.stack.setCurrentWidget(self.create_game_page),
            "Edit Jeopardy Board": self.show_edit_board_select_page,
            "Edit Final Jeopardy Question": self.show_edit_final_select_page,
        }

        for label, action in buttons.items():
            button = QPushButton(label)
            button.setFixedHeight(50)
            button.clicked.connect(action)
            button.setStyleSheet("""
                QPushButton {
                    border: 2px solid white;
                    color: white;
                    font-size: 18px;
                    background-color: transparent;
                }
                QPushButton:hover {
                    background-color: #72729c;
                }
            """)
            layout.addWidget(button)

        creator_label = QLabel("Application by Matthew Green")
        creator_label.setAlignment(Qt.AlignCenter)
        creator_label.setStyleSheet("font-size: 12px; color: gray;")
        layout.addWidget(creator_label)

        return widget

    def return_to_menu(self):
        self.stack.setCurrentWidget(self.menu_page)

    # ==== Edit Board Selection ====
    def show_edit_board_select_page(self):
        self.load_edit_board_selector(self.load_selected_board)

    def show_edit_board_select_for_game(self, set_path_callback):
        def wrapped_callback(path):
            set_path_callback(path)
            self.stack.setCurrentWidget(self.create_game_page)

        self.load_edit_board_selector(wrapped_callback)

    def load_edit_board_selector(self, callback):
        # Remove old instance
        for i in range(self.stack.count()):
            if self.stack.widget(i).__class__.__name__ == "EditBoardSelectPage":
                old_widget = self.stack.widget(i)
                self.stack.removeWidget(old_widget)
                old_widget.deleteLater()
                break

        new_page = EditBoardSelectPage(callback, self.return_to_menu)
        self.stack.addWidget(new_page)
        self.stack.setCurrentWidget(new_page)

    def load_selected_board(self, filepath):
        self.edit_board_page.clear_board()
        self.edit_board_page.load_board_from_file(filepath)
        self.stack.setCurrentWidget(self.edit_board_page)

    # ==== Edit Final Selection ====
    def show_edit_final_select_page(self):
        self.load_edit_final_selector(self.load_selected_final)

    def show_edit_final_select_for_game(self, set_path_callback):
        def wrapped_callback(path):
            set_path_callback(path)
            self.stack.setCurrentWidget(self.create_game_page)

        self.load_edit_final_selector(wrapped_callback)

    def load_edit_final_selector(self, callback):
        # Remove old instance
        for i in range(self.stack.count()):
            if self.stack.widget(i).__class__.__name__ == "EditFinalSelectPage":
                old_widget = self.stack.widget(i)
                self.stack.removeWidget(old_widget)
                old_widget.deleteLater()
                break

        new_page = EditFinalSelectPage(callback, self.return_to_menu)
        self.stack.addWidget(new_page)
        self.stack.setCurrentWidget(new_page)

    def load_selected_final(self, filepath):
        self.edit_final_page.load_question_from_file(filepath)
        self.stack.setCurrentWidget(self.edit_final_page)

    # ==== Game Select ====
    def show_game_select_screen(self):
        self.stack.setCurrentWidget(self.game_select_screen)

    def load_selected_game(self, game_path):
        print(f"Selected game folder: {game_path}")
        self.play_game_page.load_game(game_path)  # Load the selected game data
        self.stack.setCurrentWidget(self.play_game_page)  # Switch to the game screen

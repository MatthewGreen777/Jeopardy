import os
import shutil
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QInputDialog
)
from PySide6.QtCore import Qt
from util import get_user_data_path
from util import get_resource_path

class CreateGamePage(QWidget):
    def __init__(self, return_to_menu_callback, edit_board_select_callback, edit_final_select_callback):
        super().__init__()
        self.return_to_menu_callback = return_to_menu_callback
        self.edit_board_select_callback = edit_board_select_callback
        self.edit_final_select_callback = edit_final_select_callback

        self.jeopardy_path = None
        self.double_jeopardy_path = None
        self.final_path = None

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Top bar with Save and Return
        top_bar = QHBoxLayout()
        save_button = QPushButton("Save Game")
        save_button.setStyleSheet("QPushButton { border: 2px solid white; } QPushButton:hover { border: 3px solid blue; }")
        save_button.clicked.connect(self.save_game)
        top_bar.addWidget(save_button)

        return_button = QPushButton("Return to Main Menu")
        return_button.setStyleSheet("QPushButton { border: 2px solid white; } QPushButton:hover { border: 3px solid blue; }")
        return_button.clicked.connect(self.return_to_menu_callback)
        top_bar.addWidget(return_button)

        layout.addLayout(top_bar)

        # Center buttons
        center_layout = QHBoxLayout()
        self.jeopardy_button = QPushButton("Normal Jeopardy")
        self.jeopardy_button.setFixedSize(200, 150)
        self.jeopardy_button.setStyleSheet(self.round_button_style())
        self.jeopardy_button.clicked.connect(self.select_jeopardy)
        center_layout.addWidget(self.jeopardy_button)

        self.double_button = QPushButton("Double Jeopardy")
        self.double_button.setFixedSize(200, 150)
        self.double_button.setStyleSheet(self.round_button_style())
        self.double_button.clicked.connect(self.select_double_jeopardy)
        center_layout.addWidget(self.double_button)

        self.final_button = QPushButton("Final Jeopardy")
        self.final_button.setFixedSize(200, 150)
        self.final_button.setStyleSheet(self.round_button_style())
        self.final_button.clicked.connect(self.select_final_jeopardy)
        center_layout.addWidget(self.final_button)

        layout.addStretch()
        layout.addLayout(center_layout)
        layout.addStretch()

        self.setLayout(layout)

    def round_button_style(self):
        return """
        QPushButton {
            background-color: #444;
            color: white;
            font-weight: bold;
            font-size: 16px;
            border: 2px solid #000;
        }
        QPushButton:hover {
            border: 3px solid blue;
        }
        """

    def select_jeopardy(self):
        self.edit_board_select_callback(self.set_jeopardy_path)

    def select_double_jeopardy(self):
        self.edit_board_select_callback(self.set_double_jeopardy_path)

    def select_final_jeopardy(self):
        self.edit_final_select_callback(self.set_final_path)

    def set_jeopardy_path(self, path):
        self.jeopardy_path = path
        self.jeopardy_button.setText(f"Normal Jeopardy\n{os.path.basename(path)}")

    def set_double_jeopardy_path(self, path):
        self.double_jeopardy_path = path
        self.double_button.setText(f"Double Jeopardy\n{os.path.basename(path)}")

    def set_final_path(self, path):
        self.final_path = path
        self.final_button.setText(f"Final Jeopardy\n{os.path.basename(path)}")

    def save_game(self):
        if not (self.jeopardy_path and self.double_jeopardy_path and self.final_path):
            QMessageBox.warning(self, "Incomplete", "All three rounds must be selected before saving.")
            return

        game_name, ok = QInputDialog.getText(self, "Save Jeopardy Game", "Enter a name for this game:")
        if not ok or not game_name.strip():
            return

        game_name = game_name.strip()
        base_dir = get_user_data_path("games")
        game_folder = os.path.join(base_dir, game_name)
        os.makedirs(game_folder, exist_ok=True)

        try:
            def copy_round(path, dest_name):
                dest_csv = os.path.join(game_folder, f"{dest_name}.csv")
                shutil.copy2(path, dest_csv)

                base_name = os.path.splitext(os.path.basename(path))[0]
                original_subfolder = os.path.join(os.path.dirname(path), base_name)
                if os.path.exists(original_subfolder) and os.path.isdir(original_subfolder):
                    dest_subfolder = os.path.join(game_folder, dest_name)
                    if os.path.exists(dest_subfolder):
                        shutil.rmtree(dest_subfolder)
                    shutil.copytree(original_subfolder, dest_subfolder)

            copy_round(self.jeopardy_path, "jeopardy")
            copy_round(self.double_jeopardy_path, "double")
            copy_round(self.final_path, "final")

            with open(os.path.join(game_folder, "order.csv"), "w", encoding="utf-8") as f:
                f.write("jeopardy.csv\ndouble.csv\nfinal.csv\n")

            QMessageBox.information(self, "Saved", f"Game saved successfully to:\n{game_folder}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save game:\n{str(e)}")

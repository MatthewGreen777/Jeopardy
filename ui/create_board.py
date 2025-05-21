import os
import csv
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QGridLayout,
    QMessageBox, QInputDialog, QDialog, QLineEdit, QLabel, QFileDialog
)
from PySide6.QtCore import Qt

class QuestionDialog(QDialog):
    def __init__(self, existing_text="", existing_media_path=""):
        super().__init__()
        self.setWindowTitle("Enter Question")
        self.question_text = existing_text
        self.media_path = existing_media_path

        self.layout = QVBoxLayout(self)

        self.input = QLineEdit(self)
        self.input.setText(existing_text)
        self.layout.addWidget(QLabel("Enter your question:"))
        self.layout.addWidget(self.input)

        self.media_label = QLabel(self)
        self.update_media_label()

        self.layout.addWidget(self.media_label)

        media_buttons_layout = QHBoxLayout()

        attach_button = QPushButton("Attach Media")
        attach_button.clicked.connect(self.attach_media)
        media_buttons_layout.addWidget(attach_button)

        remove_button = QPushButton("Remove Media")
        remove_button.clicked.connect(self.remove_media)
        media_buttons_layout.addWidget(remove_button)

        self.layout.addLayout(media_buttons_layout)

        button_box = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_box.addWidget(save_button)
        button_box.addWidget(cancel_button)

        self.layout.addLayout(button_box)

    def update_media_label(self):
        if self.media_path:
            self.media_label.setText(f"Attached: {os.path.basename(self.media_path)}")
        else:
            self.media_label.setText("No media attached")

    def attach_media(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Attach Media",
            filter="Media Files (*.png *.jpg *.jpeg *.bmp *.gif *.mp4 *.mp3 *.wav *.mov *.avi)"
        )
        if file_path:
            self.media_path = file_path
            self.update_media_label()

    def remove_media(self):
        self.media_path = None
        self.update_media_label()

    def get_data(self):
        return self.input.text().strip(), self.media_path


class CreateBoardPage(QWidget):
    def __init__(self, return_to_menu_callback):
        super().__init__()
        self.return_to_menu_callback = return_to_menu_callback
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        top_bar = QHBoxLayout()
        save_button = QPushButton("Save Board")
        save_button.setStyleSheet("QPushButton { border: 2px solid white; } QPushButton:hover { border: 3px solid blue; }")
        save_button.clicked.connect(self.save_board)

        back_button = QPushButton("Return to Main Menu")
        back_button.setStyleSheet("QPushButton { border: 2px solid white; } QPushButton:hover { border: 3px solid blue; }")
        back_button.clicked.connect(self.confirm_back_to_menu)

        top_bar.addWidget(save_button)
        top_bar.addSpacing(10)
        top_bar.addWidget(back_button)
        self.layout.addLayout(top_bar)

        self.category_layout = QHBoxLayout()
        self.categories = []
        for _ in range(6):
            button = QPushButton("Category")
            button.setStyleSheet(self.category_style())
            button.clicked.connect(self.edit_category)
            button.setFixedHeight(80)
            self.categories.append(button)
            self.category_layout.addWidget(button)
        self.layout.addLayout(self.category_layout)

        self.grid_layout = QGridLayout()
        self.buttons = []
        self.questions = [[None for _ in range(6)] for _ in range(5)]
        self.media_files = [[None for _ in range(6)] for _ in range(5)]
        value_row = [200, 400, 600, 800, 1000]

        for r in range(5):
            for c in range(6):
                button = QPushButton(f"${value_row[r]}")
                button.setFixedHeight(80)
                button.setStyleSheet(self.question_style())
                button.clicked.connect(lambda _, row=r, col=c: self.enter_question(row, col))
                self.grid_layout.addWidget(button, r, c)
                self.buttons.append(button)

        self.layout.addLayout(self.grid_layout)

    def category_style(self):
        return """
        QPushButton {
            background-color: #333333;
            color: white;
            border: 2px solid #000;
            font-weight: bold;
        }
        QPushButton:hover {
            border: 3px solid blue;
        }
        """

    def question_style(self):
        return """
        QPushButton {
            background-color: #1E90FF;
            color: white;
            border: 2px solid #000;
            font-size: 16px;
        }
        QPushButton:hover {
            border: 3px solid blue;
        }
        """

    def question_filled_style(self):
        return """
        QPushButton {
            background-color: #1E90FF;
            color: white;
            border: 3px solid red;
            font-size: 16px;
        }
        QPushButton:hover {
            border: 4px solid darkred;
        }
        """

    def edit_category(self):
        sender = self.sender()
        text, ok = QInputDialog.getText(self, "Edit Category", "Enter category name:", text=sender.text())
        if ok and text.strip():
            sender.setText(text.strip())

    def save_board(self):
        filename, ok = QInputDialog.getText(self, "Save Board", "Enter a name for your board (without extension):")
        if not ok or not filename.strip():
            return

        board_name = filename.strip()
        save_dir = os.path.join(os.path.dirname(__file__), "..", "data", "boards")
        save_dir = os.path.abspath(save_dir)
        board_folder = os.path.join(save_dir, board_name)
        os.makedirs(board_folder, exist_ok=True)
        filepath = os.path.join(save_dir, f"{board_name}.csv")

        try:
            with open(filepath, mode="w", newline='', encoding="utf-8") as file:
                writer = csv.writer(file)

                category_titles = [button.text().strip() for button in self.categories]
                writer.writerow(category_titles)

                for row_qs, row_media in zip(self.questions, self.media_files):
                    row_data = []
                    for q, media in zip(row_qs, row_media):
                        if q:
                            entry = q
                            if media:
                                media_filename = os.path.basename(media)
                                entry += f" [media:{media_filename}]"
                                dest_path = os.path.join(board_folder, media_filename)
                                if not os.path.exists(dest_path):
                                    try:
                                        with open(media, "rb") as src, open(dest_path, "wb") as dst:
                                            dst.write(src.read())
                                    except Exception as e:
                                        print(f"Failed to copy media: {e}")
                            row_data.append(entry)
                        else:
                            row_data.append("")
                    writer.writerow(row_data)

            QMessageBox.information(self, "Saved", f"Board saved in '{board_folder}'!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save board: {str(e)}")

    def confirm_back_to_menu(self):
        confirm = QMessageBox.question(
            self,
            "Confirm Return",
            "Are you sure you want to return to the main menu? All progress will be lost.",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.clear_board()
            self.return_to_menu_callback()

    def clear_board(self):
        for button in self.categories:
            button.setText("Category")

        self.questions = [[None for _ in range(6)] for _ in range(5)]
        self.media_files = [[None for _ in range(6)] for _ in range(5)]
        value_row = [200, 400, 600, 800, 1000]
        for i, button in enumerate(self.buttons):
            r = i // 6
            button.setText(f"${value_row[r]}")
            button.setStyleSheet(self.question_style())

    def enter_question(self, row, col):
        existing_question = self.questions[row][col] or ""
        existing_media = self.media_files[row][col]

        dialog = QuestionDialog(existing_question, existing_media)
        if dialog.exec():
            question, media_path = dialog.get_data()
            self.questions[row][col] = question if question else None
            self.media_files[row][col] = media_path if media_path else None

            button = self.buttons[row * 6 + col]
            button.setText(f"${200*(row+1)}")
            button.setStyleSheet(self.question_filled_style() if question else self.question_style())

import os
import csv
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout,
    QMessageBox, QInputDialog, QLineEdit, QLabel, QFileDialog, QDialog
)
from PySide6.QtCore import Qt
from util import get_user_data_path
from util import get_resource_path

class FinalQuestionDialog(QDialog):
    def __init__(self, existing_text="", existing_media=""):
        super().__init__()
        self.setWindowTitle("Enter Final Question")
        self.media_path = existing_media

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Final Question:"))
        self.question_input = QLineEdit(self)
        self.question_input.setText(existing_text)
        layout.addWidget(self.question_input)

        self.media_label = QLabel(self)
        self.update_media_label()
        layout.addWidget(self.media_label)

        media_buttons = QHBoxLayout()
        attach_button = QPushButton("Attach Media")
        attach_button.clicked.connect(self.attach_media)
        media_buttons.addWidget(attach_button)

        remove_button = QPushButton("Remove Media")
        remove_button.clicked.connect(self.remove_media)
        media_buttons.addWidget(remove_button)

        layout.addLayout(media_buttons)

        buttons = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(save_button)
        buttons.addWidget(cancel_button)

        layout.addLayout(buttons)

    def update_media_label(self):
        self.media_label.setText(f"Attached: {os.path.basename(self.media_path)}" if self.media_path else "No media attached")

    def attach_media(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Attach Media",
            filter="Media Files (*.png *.jpg *.jpeg *.bmp *.gif *.mp4 *.mp3 *.wav *.mov *.avi)"
        )
        if path:
            self.media_path = path
            self.update_media_label()

    def remove_media(self):
        self.media_path = None
        self.update_media_label()

    def get_data(self):
        return self.question_input.text().strip(), self.media_path

class EditFinalPage(QWidget):
    def __init__(self, return_to_menu_callback):
        super().__init__()
        self.return_to_menu_callback = return_to_menu_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Top bar
        top_bar = QHBoxLayout()
        save_button = QPushButton("Save Final Question")
        save_button.setStyleSheet("QPushButton { border: 2px solid white; } QPushButton:hover { border: 3px solid blue; }")
        save_button.clicked.connect(self.save_final_question)
        top_bar.addWidget(save_button)

        back_button = QPushButton("Return to Main Menu")
        back_button.setStyleSheet("QPushButton { border: 2px solid white; } QPushButton:hover { border: 3px solid blue; }")
        back_button.clicked.connect(self.confirm_back_to_menu)
        top_bar.addWidget(back_button)

        layout.addLayout(top_bar)

        # Editable category button
        self.category_button = QPushButton("Category")
        self.category_button.setFixedHeight(80)
        self.category_button.setStyleSheet(self.category_style())
        self.category_button.clicked.connect(self.edit_category)
        layout.addWidget(self.category_button)

        # Editable question button
        self.question_button = QPushButton("Enter Final Jeopardy Question")
        self.question_button.setFixedHeight(100)
        self.question_button.setStyleSheet(self.question_style())
        self.question_button.clicked.connect(self.edit_question)
        layout.addWidget(self.question_button)

        self.setLayout(layout)

    def category_style(self):
        return """
        QPushButton {
            background-color: #333333;
            color: white;
            border: 2px solid #000;
            font-weight: bold;
            font-size: 18px;
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

    def edit_category(self):
        text, ok = QInputDialog.getText(self, "Edit Category", "Enter Final Jeopardy category:", text=self.category)
        if ok and text.strip():
            self.category = text.strip()
            self.category_button.setText(self.category)

    def edit_question(self):
        dialog = FinalQuestionDialog(self.question, self.media_path)
        if dialog.exec():
            self.question, self.media_path = dialog.get_data()
            preview = self.question[:50] + ("..." if len(self.question) > 50 else "")
            self.question_button.setText(preview or "Enter Final Jeopardy Question")

    def save_final_question(self):
        if not self.category or not self.question:
            QMessageBox.warning(self, "Incomplete", "Both category and question are required.")
            return

        filename, ok = QInputDialog.getText(self, "Save Final Question", "Enter a name for the final question (without extension):")
        if not ok or not filename.strip():
            return

        final_name = filename.strip()
        save_dir = get_user_data_path("finals")
        os.makedirs(save_dir, exist_ok=True)

        # Save CSV path
        csv_path = os.path.join(save_dir, f"{final_name}.csv")

        # Create dedicated folder for media (named same as file without extension)
        media_folder = os.path.join(save_dir, final_name)
        os.makedirs(media_folder, exist_ok=True)

        try:
            with open(csv_path, mode="w", newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                entry = self.question
                if self.media_path:
                    media_name = os.path.basename(self.media_path)
                    entry += f" [media:{media_name}]"
                    dest_path = os.path.join(media_folder, media_name)
                    if not os.path.exists(dest_path):
                        with open(self.media_path, "rb") as src, open(dest_path, "wb") as dst:
                            dst.write(src.read())
                writer.writerow([self.category])
                writer.writerow([entry])

            QMessageBox.information(self, "Saved", f"Final question saved as '{final_name}.csv'!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")


    def confirm_back_to_menu(self):
        confirm = QMessageBox.question(
            self,
            "Return to Main Menu",
            "Return to menu? Unsaved changes will be lost.",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.return_to_menu_callback()


    def load_question_from_file(self, file_path):
        self.current_file_path = file_path
        try:
            with open(file_path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                if len(rows) < 2:
                    QMessageBox.warning(self, "Invalid File", "The selected file does not contain a valid Final Jeopardy format.")
                    return

                self.category = rows[0][0].strip()
                raw_question = rows[1][0].strip()

                # Handle possible media tag
                media_path = None
                if "[media:" in raw_question and raw_question.endswith("]"):
                    try:
                        question_part, media_tag = raw_question.rsplit(" [media:", 1)
                        media_filename = media_tag[:-1]  # remove trailing ']'

                        # Look for media in folder named after the file (same name as CSV, no extension)
                        final_name = os.path.splitext(os.path.basename(file_path))[0]
                        media_folder = os.path.join(get_user_data_path("finals"), final_name)
                        possible_media_path = os.path.join(media_folder, media_filename)

                        if os.path.exists(possible_media_path):
                            media_path = possible_media_path

                        self.question = question_part.strip()
                    except Exception:
                        self.question = raw_question  # fallback if media tag fails
                        media_path = None
                else:
                    self.question = raw_question
                    media_path = None

                self.media_path = media_path
                self.category_button.setText(self.category)
                preview = self.question[:50] + ("..." if len(self.question) > 50 else "")
                self.question_button.setText(preview or "Enter Final Jeopardy Question")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file:\n{str(e)}")

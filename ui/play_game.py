import os
import csv
import random
import re
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel,
    QStackedLayout, QMessageBox, QSizePolicy
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPixmap, QMovie, QKeyEvent
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget

class PlayGamePage(QWidget):
    def __init__(self, return_callback):
        super().__init__()
        self.return_callback = return_callback
        self.init_ui()
        self.current_round_index = 0
        self.rounds = []
        self.round_data = {}
        self.daily_doubles = []
        self.selected_questions = set()
        self.questions_remaining = 0

        self.setFocusPolicy(Qt.StrongFocus)

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.stack = QStackedLayout()
        self.layout.addLayout(self.stack)

        self.board_widget = QWidget()
        self.board_layout = QGridLayout(self.board_widget)
        self.stack.addWidget(self.board_widget)

        self.question_widget = QWidget()
        self.question_label = QLabel()
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("font-size: 24px; color: white;")
        self.question_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.media_label = QLabel("")
        self.media_label.setAlignment(Qt.AlignCenter)
        question_layout = QVBoxLayout()
        question_layout.setAlignment(Qt.AlignCenter)
        question_layout.addWidget(self.question_label)
        question_layout.addWidget(self.media_label)
        self.question_widget.setLayout(question_layout)
        self.stack.addWidget(self.question_widget)

        self.transition_widget = QWidget()
        self.transition_layout = QVBoxLayout(self.transition_widget)
        self.transition_label = QLabel()
        self.transition_label.setAlignment(Qt.AlignCenter)
        self.transition_label.setStyleSheet("font-size: 32px; color: yellow;")
        self.transition_layout.addWidget(self.transition_label)
        self.stack.addWidget(self.transition_widget)

        self.final_category_widget = QWidget()
        self.final_category_layout = QVBoxLayout(self.final_category_widget)
        self.final_category_label = QLabel()
        self.final_category_label.setAlignment(Qt.AlignCenter)
        self.final_category_label.setStyleSheet("font-size: 28px; color: cyan;")
        self.final_category_layout.addWidget(self.final_category_label)
        self.stack.addWidget(self.final_category_widget)

        self.final_widget = QWidget()
        self.final_layout = QVBoxLayout(self.final_widget)
        self.final_question_label = QLabel()
        self.final_question_label.setAlignment(Qt.AlignCenter)
        self.final_question_label.setWordWrap(True)
        self.final_question_label.setStyleSheet("font-size: 24px; color: white;")
        self.final_layout.addWidget(self.final_question_label)
        self.stack.addWidget(self.final_widget)

        self.video_player = QMediaPlayer()
        self.video_widget = QVideoWidget()
        self.video_player.setVideoOutput(self.video_widget)
        self.stack.addWidget(self.video_widget)

        self.audio_player = QMediaPlayer()

        self.setStyleSheet("background-color: #060CE9;")

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.confirm_exit()

    def confirm_exit(self):
        box = QMessageBox(self)
        box.setWindowTitle("Exit Game")
        box.setText("Are you sure you want to stop the game?")
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        box.setIcon(QMessageBox.Question)
        if box.exec() == QMessageBox.Yes:
            self.return_callback()

    def load_game(self, game_path):
        self.current_game_path = game_path
        order_file = os.path.join(game_path, "order.csv")
        if not os.path.exists(order_file):
            print(f"Missing order.csv in {game_path}")
            return

        with open(order_file, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            self.rounds = [row[0].replace('.csv', '') for row in reader if row]

        self.round_data = {}
        for round_name in self.rounds:
            round_file = os.path.join(game_path, f"{round_name}.csv")
            if not os.path.exists(round_file):
                continue
            with open(round_file, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                if round_name.lower() == 'final':
                    category = rows[0][0] if rows and rows[0] else "Final Jeopardy"
                    question = rows[1][0] if len(rows) > 1 and rows[1] else "No question provided."
                    self.round_data[round_name] = {
                        "categories": [category],
                        "questions": {category: [{"question": question}]}
                    }
                else:
                    categories = rows[0]
                    questions = {cat: [] for cat in categories}
                    for row in rows[1:]:
                        for i, val in enumerate(row):
                            try:
                                q = eval(val) if val.strip().startswith('{') else {"question": val}
                            except:
                                q = {"question": val}
                            questions[categories[i]].append(q)
                    self.round_data[round_name] = {
                        "categories": categories,
                        "questions": questions
                    }

        self.current_round_index = 0
        self.selected_questions.clear()
        self.daily_doubles.clear()
        self.build_board()

    def build_board(self):
        for i in reversed(range(self.board_layout.count())):
            widget = self.board_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        round_name = self.rounds[self.current_round_index]
        data = self.round_data[round_name]
        categories = data['categories']
        questions = data['questions']
        self.questions_remaining = sum(len(questions[cat]) for cat in categories)

        fixed_width = 160
        category_height = 80
        button_height = 80

        for col, category in enumerate(categories):
            label = QLabel(self.wrap_text(category, 15))
            label.setAlignment(Qt.AlignCenter)
            label.setWordWrap(True)
            label.setFixedSize(fixed_width, category_height)
            label.setStyleSheet("""
                font-size: 18px;
                color: white;
                padding: 6px;
                border: 2px solid #ffffff;
                background-color: #000099;
            """)
            self.board_layout.addWidget(label, 0, col)

        for row in range(5):
            for col, category in enumerate(categories):
                q_list = questions.get(category, [])
                if row < len(q_list):
                    value = (row + 1) * 200
                    if self.rounds[self.current_round_index] == "double":
                        value *= 2
                    btn = QPushButton(f"${value}")
                    btn.setFixedSize(fixed_width, button_height)
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #0000cc;
                            color: gold;
                            font-size: 20px;
                            font-weight: bold;
                            border: 2px solid white;
                        }
                        QPushButton:hover {
                            background-color: #0000ff;
                        }
                        QPushButton:disabled {
                            background-color: #222;
                            color: #888;
                            border: 2px solid gray;
                        }
                    """)
                    btn.clicked.connect(lambda _, c=category, r=row: self.show_question(c, r))
                    self.board_layout.addWidget(btn, row + 1, col)
                else:
                    spacer = QLabel("")
                    spacer.setFixedSize(fixed_width, button_height)
                    self.board_layout.addWidget(spacer, row + 1, col)

        self.stack.setCurrentWidget(self.board_widget)

    def wrap_text(self, text, max_chars):
        if len(text) <= max_chars:
            return text

        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + 1 <= max_chars:
                if current_line:
                    current_line += " "
                current_line += word
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return '\n'.join(lines)

    def show_question(self, category, index):
        round_name = self.rounds[self.current_round_index]
        key = (category, index)
        question_data = self.round_data[round_name]["questions"][category][index]

        if key in self.selected_questions:
            return

        self.selected_questions.add(key)
        self.questions_remaining -= 1

        if not self.daily_doubles and self.questions_remaining <= (
            len(self.round_data[round_name]["categories"]) * 5 - 1
        ):
            self.assign_daily_doubles()

        if key in self.daily_doubles:
            self.transition_label.setText("🎯 Daily Double!")
            self.stack.setCurrentWidget(self.transition_widget)

            def proceed():
                self.transition_widget.mousePressEvent = lambda event: None
                self.transition_widget.keyPressEvent = lambda event: None
                self.display_question(category, index)

            self.transition_widget.mousePressEvent = lambda event: (
                proceed() if event.button() == Qt.LeftButton else None
            )
            self.transition_widget.keyPressEvent = lambda event: (
                proceed() if event.key() in (Qt.Key_Return, Qt.Key_Enter) else None
            )

            self.transition_widget.setFocus()
        else:
            self.display_question(category, index)

    def display_question(self, category, index):
        round_name = self.rounds[self.current_round_index]
        question_data = self.round_data[round_name]["questions"][category][index]
        raw_text = question_data.get("question", "")
        media = None

        media_match = re.search(r"\[media:(.+?)\]", raw_text)
        if media_match:
            media = media_match.group(1)
            raw_text = re.sub(r"\[media:.+?\]", "", raw_text).strip()

        self.question_label.setText(raw_text)
        self.media_label.clear()
        
        # Stop any playing media first
        self.video_player.stop()
        self.video_widget.hide()  # hide video widget if visible
        self.audio_player.stop()

        if media:
            media_path = os.path.join(self.current_game_path, round_name, media)
            if os.path.exists(media_path):
                ext = os.path.splitext(media_path)[1].lower()

                if ext in [".png", ".jpg", ".jpeg", ".bmp"]:
                    pixmap = QPixmap(media_path)
                    self.media_label.setPixmap(pixmap.scaledToWidth(400, Qt.SmoothTransformation))

                elif ext == ".gif":
                    movie = QMovie(media_path)
                    self.media_label.setMovie(movie)
                    movie.start()

                elif ext in [".mp4", ".mov", ".avi"]:
                    self.video_player.setSource(QUrl.fromLocalFile(media_path))
                    self.video_widget.show()
                    self.video_player.play()

                elif ext in [".mp3", ".wav"]:
                    self.audio_player.setSource(QUrl.fromLocalFile(media_path))
                    self.audio_player.play()  # <-- Make sure this line is here!

                else:
                    self.media_label.setText(f"⚠️ Unsupported media format: {media}")
            else:
                self.media_label.setText(f"⚠️ Media not found: {media}")

        self.stack.setCurrentWidget(self.question_widget)

        def handle_return():
            self.question_widget.mousePressEvent = lambda event: None
            self.question_widget.keyPressEvent = lambda event: None
            self.video_player.stop()
            self.audio_player.stop()
            self.video_widget.hide()
            self.return_to_board(category, index)

        self.question_widget.mousePressEvent = lambda event: (
            handle_return() if event.button() == Qt.LeftButton else None
        )
        self.question_widget.keyPressEvent = lambda event: (
            handle_return() if event.key() in (Qt.Key_Return, Qt.Key_Enter) else None
        )

        self.question_widget.setFocus()


    def return_to_board(self, category, index):
        for i in range(self.board_layout.count()):
            widget = self.board_layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):
                row, col = self.board_layout.getItemPosition(i)[:2]
                cat = self.round_data[self.rounds[self.current_round_index]]["categories"][col]
                if cat == category and row - 1 == index:
                    widget.setDisabled(True)
                    break

        self.stack.setCurrentWidget(self.board_widget)

        if self.questions_remaining == 0:
            if self.current_round_index + 1 < len(self.rounds):
                self.transition_to_round(self.rounds[self.current_round_index + 1])
            else:
                self.transition_to_final_jeopardy()

    def assign_daily_doubles(self):
        current_data = self.round_data[self.rounds[self.current_round_index]]
        keys = [
            (cat, i)
            for cat in current_data["questions"]
            for i in range(len(current_data["questions"][cat]))
            if (cat, i) not in self.selected_questions
        ]
        self.daily_doubles = random.sample(keys, 2)

    def transition_to_round(self, next_round):
        self.transition_label.setText(f"{next_round.capitalize()} is beginning!")
        self.stack.setCurrentWidget(self.transition_widget)

        def proceed():
            self.start_round(next_round)

        self.wait_for_user_input(proceed)


    def start_round(self, round_name):
        self.current_round_index += 1
        self.selected_questions.clear()
        self.daily_doubles.clear()

        if round_name.lower() == "final":
            self.transition_to_final_jeopardy()
        else:
            self.build_board()


    def transition_to_final_jeopardy(self):
        self.transition_label.setText("Final Jeopardy is beginning!")
        self.stack.setCurrentWidget(self.transition_widget)

        self.wait_for_user_input(self.show_final_category)


    def show_final_category(self):
        final_data = self.round_data["final"]
        category = final_data['categories'][0]
        self.final_category_label.setText(f"Final Jeopardy Category:\n{category}")
        self.stack.setCurrentWidget(self.final_category_widget)

        self.wait_for_user_input(self.show_final_question)


    def show_final_question(self):
        final_data = self.round_data["final"]
        category = final_data['categories'][0]
        question = final_data['questions'][category][0]['question']
        self.final_question_label.setText(question)
        self.stack.setCurrentWidget(self.final_widget)

        # Add this to allow user input to return to main menu
        def finish():
            self.final_widget.mousePressEvent = lambda event: None
            self.final_widget.keyPressEvent = lambda event: None
            self.return_callback()

        self.final_widget.mousePressEvent = lambda event: (
            finish() if event.button() == Qt.LeftButton else None
        )
        self.final_widget.keyPressEvent = lambda event: (
            finish() if event.key() in (Qt.Key_Return, Qt.Key_Enter) else None
        )

        self.final_widget.setFocus()


    def wait_for_user_input(self, callback):
        def mouse_handler(event):
            if event.button() == Qt.LeftButton:
                cleanup()
                callback()

        def key_handler(event):
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                cleanup()
                callback()

        def cleanup():
            self.transition_widget.mousePressEvent = lambda event: None
            self.final_category_widget.mousePressEvent = lambda event: None
            self.transition_widget.keyPressEvent = lambda event: None
            self.final_category_widget.keyPressEvent = lambda event: None

        self.transition_widget.mousePressEvent = mouse_handler
        self.final_category_widget.mousePressEvent = mouse_handler
        self.transition_widget.keyPressEvent = key_handler
        self.final_category_widget.keyPressEvent = key_handler

        self.transition_widget.setFocus()
        self.final_category_widget.setFocus()
**Author: Matthew Green**  
This program is a personal implementation of the game show **Jeopardy!**, created purely for fun and educational purposes. It has **no association** with the official Jeopardy! brand, company, or its original creators. The project was built using **PySide6**, a Python GUI framework based on Qt.

---

## 📖 Overview

This application allows users to **create**, **edit**, and **play** custom Jeopardy games, complete with categories, questions, and multimedia support. The interface is simple and intuitive, designed to make it easy for anyone to build and host a game.

---

## 🚀 Features

Upon launching the program, users are presented with a **main menu** featuring six options:

### 1. **Play Jeopardy Game**
- Play a full Jeopardy game that has been created using the tools provided.
- Games include two Jeopardy rounds and a Final Jeopardy round.
- Compatible with user-created games and sample games included with the program.

### 2. **Create Jeopardy Board**
- Build a traditional Jeopardy round or Double Jeopardy round.
- Each board has **6 categories**, and each category has **5 questions**.
- Each question can optionally include media (images, video, audio).

### 3. **Create Final Jeopardy Question**
- Create a single Final Jeopardy entry with a **category title** and **question**.
- Optional media can also be attached here.

### 4. **Create Jeopardy Game**
- Combine two created Jeopardy boards (Jeopardy and Double Jeopardy) with a Final Jeopardy question to create a complete game.

### 5. **Edit Jeopardy Board**
- Load and modify an existing Jeopardy board.
- Update category names and individual questions easily.

### 6. **Edit Final Jeopardy Question**
- Load and update a Final Jeopardy category or question.

---

## 📁 Supported Media Types

Questions can include optional media of the following file types:

- **Images:** `.png`, `.jpg`, `.jpeg`, `.bmp`
- **GIFs:** `.gif`
- **Audio:** `.mp3`, `.wav`
- **Video:** `.mp4`, `.mov`, `.avi`

These can be embedded into questions using a tag format like `[media:filename.ext]`.

---

## 🛠 Requirements

- Python 3.7+
- PySide6

Install requirements using:

```bash
pip install PySide6
```

---

## 📝 Notes & Licensing

This project is **open to feedback, suggestions, and modification**. If you decide to fork or build upon this codebase, **please give credit to Matthew Green** as the original author.

---

Thank you for checking out the project! If you enjoy it or have ideas for improvements, feel free to contribute or reach out.
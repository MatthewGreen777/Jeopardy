# 🎮 Jeopardy Game Builder & Player

**Author: Matthew Green**  
This program is a personal implementation of the game show **Jeopardy!**, created purely for fun and educational purposes. It has **no association** with the official Jeopardy! brand, company, or its original creators. The project was built using **PySide6**, a Python GUI framework based on Qt.

---

## 📖 Overview

This application allows users to **create**, **edit**, and **play** custom Jeopardy games, complete with categories, questions, and multimedia support. The interface is simple and intuitive, designed to make it easy for anyone to build and host a game.

---

## 🚀 Features

Upon launching the program, users are presented with a **main menu** featuring six options:

### 1. Play Jeopardy Game
- Play a full Jeopardy game that has been created using the tools provided.
- Games include two Jeopardy rounds and a Final Jeopardy round.
- Compatible with user-created games and sample games included with the program.

### 2. Create Jeopardy Board
- Build a traditional Jeopardy round or Double Jeopardy round.
- Each board has **6 categories**, and each category has **5 questions**.
- Each question can optionally include media (images only for now).

### 3. Create Final Jeopardy Question
- Create a single Final Jeopardy entry with a **category title** and **question**.
- Optional image media can also be attached here.

### 4. Create Jeopardy Game
- Combine two created Jeopardy boards (Jeopardy and Double Jeopardy) with a Final Jeopardy question to create a complete game.

### 5. Edit Jeopardy Board
- Load and modify an existing Jeopardy board.
- Update category names and individual questions easily.

### 6. Edit Final Jeopardy Question
- Load and update a Final Jeopardy category or question.

---

## 📁 Supported Media Types

Currently supported:

- **Images:** `.png`, `.jpg`, `.jpeg`, `.bmp`
- **GIFs:** `.gif`

Media is embedded using a tag format like `[media:filename.ext]` in your question text.

---

## 🔮 Future Development

While image support is fully functional, **audio (`.mp3`, `.wav`) and video (`.mp4`, `.mov`, `.avi`) files are not yet supported for playback in-game**.  

✅ These file types **can still be attached** during board creation, but **they will not play during gameplay** — yet!

🎯 Full support for **audio and video playback during questions** is planned for a future release.

---

## 📥 Download

You can download and run the program in two ways:

### ✅ Precompiled Windows Executable (No Python Required)

- **Download the ZIP file directly:**  
  👉 [Jeopardy.zip](https://github.com/MatthewGreen777/Jeopardy/blob/main/Jeopardy.zip)

- **Or visit the project page:**  
  🌐 [www.MatthewGreen777.com/jeopardy.html](http://www.matthewgreen777.com/jeopardy.html)

> Just extract the ZIP file and run `Jeopardy.exe`. No installation needed!

### 🐍 Run from Source (Requires Python)

1. Install Python 3.7 or higher  
2. Install dependencies:

```bash
pip install PySide6
```

3. Run the application:

```bash
python main.py
```

---

## 🛠 Developer Notes

To compile your own .exe file using PyInstaller:

```bash
pyinstaller --noconfirm --windowed --add-data "data;data" --add-data "ui;ui" main.py
```

Make sure your project folder looks like:

```
Jeopardy/
├── data/
│   ├── boards/
│   ├── games/
│   └── finals/
├── ui/
├── main.py
├── main_menu.py
└── ...
```

---

## 📝 Notes & Licensing

This project is **open to feedback, suggestions, and modification**. If you decide to fork or build upon this codebase, **please give credit to Matthew Green** as the original author.

---

## 🔗 Links

- 📂 GitHub Repository: https://github.com/MatthewGreen777/Jeopardy  
- ⬇️ Download ZIP: [Jeopardy.zip](https://github.com/MatthewGreen777/Jeopardy/blob/main/Jeopardy.zip)  
- 🌍 Project Page: [www.MatthewGreen777.com/jeopardy.html](http://www.matthewgreen777.com/jeopardy.html)

Thank you for checking out the project! If you enjoy it or have ideas for improvements, feel free to contribute or reach out.

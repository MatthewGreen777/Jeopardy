from PySide6.QtWidgets import QApplication
import sys
import os

def get_resource_path(relative_path):
    """ Get the absolute path to a resource, whether running as script or bundled with PyInstaller. """
    if getattr(sys, 'frozen', False):  # PyInstaller bundle
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

def get_user_data_path(subfolder):
    """ Get path relative to the main application directory (e.g., Documents/Jeopardy/JeopardyData). """
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)  # Location of the .exe when frozen
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Location of the script

    base = os.path.join(base_dir, "JeopardyData", subfolder)
    os.makedirs(base, exist_ok=True)
    return base

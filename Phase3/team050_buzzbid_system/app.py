import tkinter as tk
import customtkinter as ctk
from gui.login_window import LoginWindow


def main():
    # Set the theme for CustomTkinter
    ctk.set_appearance_mode("Light")  # Can be "System", "Dark", or "Light"
    ctk.set_default_color_theme("dark-blue")  # Check CustomTkinter documentation for themes

    login_window = LoginWindow()
    login_window.mainloop()

if __name__ == "__main__":
    main()

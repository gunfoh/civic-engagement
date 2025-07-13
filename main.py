import tkinter as tk
from app import CivicEngagementApp

def main():
    """
    The main entry point for the application.
    Initializes the tkinter root window and the main application class.
    """
    root = tk.Tk()
    app = CivicEngagementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

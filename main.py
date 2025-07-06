import sys
import platform

# Placeholder for GUI main window
from gui.main_window import run_gui

def main():
    if '--cli' in sys.argv:
        print("CLI mode is not yet implemented. Please use the GUI.")
        sys.exit(0)
    else:
        try:
            run_gui()
        except ImportError:
            print("PySide6 is required for the GUI. Please install dependencies.")
            sys.exit(1)

if __name__ == "__main__":
    main() 
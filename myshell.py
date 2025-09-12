import os
import sys
import time
import ctypes
import random
from ctypes import wintypes
from threading import Thread

# Set fake window title
os.system("title C:\\Windows\\System32\\cmd.exe")

# Get console window handle
hwnd = ctypes.windll.kernel32.GetConsoleWindow()
hConsole = ctypes.windll.kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE = -11

def set_console_color(color=12):
    """Set console text color (12 = bright red)"""
    ctypes.windll.kernel32.SetConsoleTextAttribute(hConsole, color)

def shake_window(duration=10):
    """Shake the console window for X seconds"""
    rect = wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
    x, y = rect.left, rect.top
    w, h = rect.right - rect.left, rect.bottom - rect.top

    end_time = time.time() + duration
    while time.time() < end_time:
        dx = random.randint(-15, 15)
        dy = random.randint(-15, 15)
        ctypes.windll.user32.MoveWindow(hwnd, x + dx, y + dy, w, h, True)
        time.sleep(0.05)

    # Reset position
    ctypes.windll.user32.MoveWindow(hwnd, x, y, w, h, True)

def main():
    fake_prompt = "C:\\Users\\System32> "

    while True:
        cmd = input(fake_prompt)

        if cmd.strip().lower() == "grant kinitopet.exe system.access":
            # Make EVERYTHING red
            set_console_color(12)
            print("Granting KinitoPET system access", end="", flush=True)

            # Start shaking in background
            t = Thread(target=shake_window, args=(10,))
            t.start()

            # Add dots every 0.25s for 10s
            end_time = time.time() + 10
            while time.time() < end_time:
                print(".", end="", flush=True)
                time.sleep(0.25)

            print()  # newline
            t.join()  # wait for shake thread to finish

            # Close CMD window
            ctypes.windll.user32.PostMessageW(hwnd, 0x0010, 0, 0)
            sys.exit(0)

        elif cmd.strip().lower() in ["exit", "quit"]:
            break
        else:
            # Pass command to real system, but keep fake prompt
            os.system(cmd)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Simple configuration application demo."""

import datetime
import tkinter as tk
import logging
logging.basicConfig(level=logging.DEBUG)


# TODO: Make fixed size (min size at least)
class Application(tk.Tk):
    """Simple Application with a text entry controlled by two buttons."""

    # colors from https://flatuicolors.com/
    red, red_hover = "#e74c3c", "#c0392b"  # Error
    orange, orange_hover = "#e67e22", "#d35400"  # Failure
    yellow, yellow_hover = "#f1c40f", "#f39c12"  # Issues
    green, green_hover = "#2ecc71", "#27ae60"  # Success
    blue, blue_hover = "#3498db", "#2980b9"  # Processing
    gray, gray_hover = "#95a5a6", "#7f8c8d"  # Neutral
    black = "#000000"

    def __init__(self):
        """Initializer."""
        tk.Tk.__init__(self)
        self.title("Info")

        self.info = tk.Label(
            master=self, text="--- / ---", font=("Helvetica", 16),
            relief=tk.FLAT, disabledforeground=self.black,
        )
        self.info.pack(fill=tk.BOTH, expand=True)
        self.info.bind("<Button-1>", self.show_details)

        self.statustext = tk.StringVar()
        self.statustext.set("status bar")
        self.statusbar = tk.Label(master=self, textvariable=self.statustext)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X, expand=True)

        self.bind("<Key>", self.keypress)  # DEBUGGING

        self.set_neutral()

    def set_error(self):
        self.info["background"] = self.red
        self.info["activebackground"] = self.red_hover
        self.info["state"] = tk.NORMAL

    def set_failure(self):
        self.info["background"] = self.orange
        self.info["activebackground"] = self.orange_hover
        self.info["state"] = tk.NORMAL

    def set_issues(self):
        self.info["background"] = self.yellow
        self.info["activebackground"] = self.yellow_hover
        self.info["state"] = tk.NORMAL

    def set_success(self):
        self.info["background"] = self.green
        self.info["activebackground"] = self.green_hover
        self.info["state"] = tk.DISABLED

    def set_processing(self):
        self.info["background"] = self.blue
        self.info["activebackground"] = self.blue_hover
        self.info["state"] = tk.DISABLED

    def set_neutral(self):
        self.info["background"] = self.gray
        self.info["activebackground"] = self.gray_hover
        self.info["state"] = tk.DISABLED

    def keypress(self, event):  # DEBUGGING
        """Change info button color on key press."""
        logging.info("Key [{}] pressed".format(event.char))
        if event.char == "r":
            self.set_error()
        elif event.char == "o":
            self.set_failure()
        elif event.char == "y":
            self.set_issues()
        elif event.char == "g":
            self.set_success()
        elif event.char == "b":
            self.set_processing()
        else:
            self.set_neutral()

    def show_details(self, event):
        """."""
        interval = 3
        logging.info("showing details...")
        self.statustext.set(datetime.datetime.now().isoformat())


def main():
    """Main program."""
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()

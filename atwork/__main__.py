"""At Work time counter dialog.

Tool for showing time to end of work.
"""
import tkinter as tk
from datetime import datetime, timedelta
from importlib.resources import files
from os.path import join
from sys import exit as sysexit
from tkinter import ttk

__version__ = "0.2.0"
ZERO_YEAR = 1970
# pylint: disable=too-many-ancestors


class TimeEntry(ttk.Entry):
    """Own Entry for time values."""

    def __init__(self, parent):
        self._emit = lambda: None
        self.value = tk.StringVar(value="0:0")
        self._date = datetime(ZERO_YEAR, 1, 1, 0, 0)
        super().__init__(parent, textvariable=self.value, justify=tk.CENTER)

        self.bind("<Key-Return>", self.on_enter)
        self.bind("<Key-KP_Enter>", self.on_enter)

    def on_enter(self, *_):
        """On Key Enter callback."""
        try:
            self._date = datetime.strptime(self.value.get(), "%H:%M")
            self._emit(self._date)
        except ValueError:
            self.value.set(self._date.strftime("%H:%M"))

    @property
    def date(self):
        """Return internal date value."""
        return self._date

    @date.setter
    def date(self, value):
        self._date = value
        self.value.set(self._date.strftime("%H:%M"))

    def connect(self, fun):
        """Set callback for Key Enter event."""
        self._emit = fun


class Application(tk.Tk):
    """Application window."""

    def __init__(self):
        super().__init__(className="atwork")  # atwork.desktop
        self.title("At Work time counter")
        self.resizable(0, 0)
        photo = tk.PhotoImage(file=join(files(str("atwork")), "atwork.png"))
        self.iconphoto(False, photo)
        self["padx"] = 10

        label = self.label("Start time:")
        label.grid(row=0, column=0, sticky=tk.W)
        self.start = TimeEntry(self)
        self.start.date = datetime(ZERO_YEAR, 1, 1, 7, 30)
        self.start.grid(row=0, column=1)
        self.start.connect(self.recalulate)

        label = self.label("Actual time:")
        label.grid(row=1, column=0, sticky=tk.W)
        self.now = self.label(datetime.now().strftime("%H:%M"))
        self.now.grid(row=1, column=1)

        label = self.label("Pause time:")
        label.grid(row=2, column=0, sticky=tk.W)
        self.lunch = TimeEntry(self)
        self.lunch.date = datetime(ZERO_YEAR, 1, 1, 0, 30)
        self.lunch.grid(row=2, column=1)
        self.lunch.connect(self.recalulate)

        label = self.label("Working time:")
        label.grid(row=3, column=0, sticky=tk.W)
        self.working = TimeEntry(self)
        self.working.date = datetime(ZERO_YEAR, 1, 1, 8, 0)
        self.working.grid(row=3, column=1)
        self.working.connect(self.recalulate)

        tk.Frame(height=5, bd=0).grid(row=4,
                                      column=0,
                                      columnspan=2,
                                      padx=5,
                                      pady=10)

        label = self.label("Worked time:")
        label.grid(row=5, column=0, sticky=tk.W)
        self.worked = self.label("")
        self.worked.grid(row=5, column=1)

        label = self.label("Time to go:")
        label.grid(row=6, column=0, sticky=tk.W)
        self.to_go = self.label("")
        self.to_go.grid(row=6, column=1)

        label = self.label("When to go:")
        label.grid(row=7, column=0, sticky=tk.W)
        self.end = self.label("")
        self.end.grid(row=7, column=1)

        tk.Frame(height=5, bd=0).grid(row=8,
                                      column=0,
                                      columnspan=2,
                                      padx=5,
                                      pady=10)

        status = tk.Label(
            self, text="Fill times and press Enter key to recalulate them.")
        status.grid(row=8, column=0, columnspan=2)

        self.recalulate()

    def label(self, text):
        """ttk.Label factory"""
        return ttk.Label(self, anchor=tk.W, justify=tk.LEFT, text=text)

    def recalulate(self, *_):
        """Recalculate worked time and time to go."""
        start = timedelta(hours=self.start.date.hour,
                          minutes=self.start.date.minute)
        now = datetime.now()
        self.now["text"] = now.strftime("%H:%M")
        now = timedelta(hours=now.hour, minutes=now.minute)

        lunch = timedelta(hours=self.lunch.date.hour,
                          minutes=self.lunch.date.minute)
        diff = now - start - lunch
        if diff.days == 0:
            hour = int(diff.seconds / 3600)
            minute = int((diff.seconds - hour * 3600) / 60)
        else:
            hour = minute = 0
        worked = datetime(ZERO_YEAR, 1, 1, hour, minute)
        self.worked["text"] = worked.strftime("%H:%M")

        working = timedelta(hours=self.working.date.hour,
                            minutes=self.working.date.minute)
        diff = start + lunch + working
        hour = int(diff.seconds / 3600)
        minute = int((diff.seconds - hour * 3600) / 60)
        end = datetime(ZERO_YEAR, 1, 1, hour, minute)

        to_go = end - now

        if to_go.year == ZERO_YEAR:
            self.to_go["foreground"] = "red"
        else:
            now = datetime.now()
            now = datetime(ZERO_YEAR, 1, 1, now.hour, now.minute)
            to_go = now - end
            hour = int(to_go.seconds / 3600)
            minute = int((to_go.seconds - hour * 3600) / 60)
            to_go = datetime(ZERO_YEAR, 1, 1, hour, minute)
            self.to_go["foreground"] = "blue"

        self.to_go["text"] = to_go.strftime("%H:%M")
        self.end["text"] = end.strftime("%H:%M")


def main():
    """Main function."""
    app = Application()
    app.mainloop()
    sysexit(0)


if __name__ == "__main__":
    main()

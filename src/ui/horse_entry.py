from tkinter import *

from src.utils.constants import Color, Misc


class HorseEntry:

    def __init__(self,
                 parent_widget,
                 entries: int,
                 pady: int):
        frame = Frame(parent_widget)

        label_style = 'Times 16 bold'
        entry_style = 'Times 18'
        self.entries = entries
        self.numbers = []

        for i in range(1, entries + 1):
            Label(frame, text=Misc.ORDINALS[i], font=label_style) \
                .grid(row=1, column=i, padx=20, pady=5)

            number = StringVar()
            Entry(frame,
                  textvariable=number,
                  font=entry_style,
                  fg=Color.RED,
                  width=5,
                  borderwidth=5,
                  justify=CENTER) \
                .grid(row=2, column=i, padx=20, pady=5)

            self.numbers.append(number)

        frame.pack(pady=pady)

    def set_values(self, values: [int]):
        if len(values) <= self.entries:
            for i in range(len(values)):
                self.numbers[i].set(values[i])

    def get_values(self) -> [int]:
        strings = [n.get() for n in self.numbers]
        numbers = []

        for s in strings:
            try:
                n = int(s)
                if 0 < n < 15:
                    numbers.append(n)
            except:
                pass

        return numbers

    def clear(self):
        for number in self.numbers:
            number.set('')

from tkinter import *

TAB_WIDTH = 200
TAB_HEIGHT = 50


class Tab:

    def __init__(self, parent, title):
        self.canvas = Canvas(
            parent,
            width=TAB_WIDTH,
            height=TAB_HEIGHT,
            cursor='heart',
        )
        self.canvas.create_polygon(
            self.get_round_rectangle_points(
                30, 3, 3, TAB_WIDTH - 3, TAB_HEIGHT - 3
            ),
            smooth=True,
            fill='',
            outline='black',
            width=2,
        )
        self.canvas.create_text(
            TAB_WIDTH // 2, TAB_HEIGHT // 2,
            text=title,
            font='Times 20 bold',
        )
        self.canvas.pack(
            side=LEFT,
            padx=10,
            pady=15,
        )

    @staticmethod
    def get_round_rectangle_points(radius, x1, y1, x2, y2):
        return [
            x1 + radius, y1,
            x2 - radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1 + radius,
            x1, y1,
        ]

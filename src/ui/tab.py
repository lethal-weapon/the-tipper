from tkinter import *
from src.utils.constants import Style

TAB_WIDTH = 200
TAB_HEIGHT = 50


class Tab:

    def __init__(self, parent, parent_widget, title):
        self.parent = parent
        self.canvas = Canvas(
            parent_widget,
            width=TAB_WIDTH,
            height=TAB_HEIGHT,
        )
        self.rectangle = self.canvas.create_polygon(
            self.get_round_rectangle_points(
                10, 3, 3, TAB_WIDTH - 3, TAB_HEIGHT - 3
            ),
            smooth=True,
            fill='',
            outline='black',
            width=2,
        )
        self.title = self.canvas.create_text(
            TAB_WIDTH // 2, TAB_HEIGHT // 2,
            text=title,
            font='Times 20 bold',
        )
        self.selected = False
        self.canvas.bind('<Enter>', self.toggle_style)
        self.canvas.bind('<Leave>', self.toggle_style)
        self.canvas.bind('<Button-1>', self.select)
        self.canvas.pack(
            side=LEFT,
            padx=10,
            pady=15,
        )

    def toggle_style(self, e):
        # cursor enter/leave event doesn't work on selected tab
        if self.selected:
            return

        curr_fill = self.canvas.itemcget(self.rectangle, Style.FILL)
        if len(curr_fill) == 0:
            self.set_active_style()
        else:
            self.set_inactive_style()

    def select(self, e):
        # cursor press event doesn't work on selected tab
        self.selected = True
        self.set_active_style()
        self.parent.on_tab_clicked(self)

    def deselect(self):
        self.selected = False
        self.set_inactive_style()

    def set_active_style(self):
        self.canvas.itemconfig(self.rectangle, fill='black')
        self.canvas.itemconfig(self.title, fill='white')

    def set_inactive_style(self):
        self.canvas.itemconfig(self.rectangle, fill='')
        self.canvas.itemconfig(self.title, fill='black')

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

from tkinter import *

from src.ui.tab import Tab

APP_NAME = 'The Tipper'
WINDOW_WIDTH = 900
WINDOW_HEIGHT = WINDOW_WIDTH * 5 // 8


class Tipper:
    window = Tk()
    tabs = []

    @classmethod
    def launch(cls):
        cls.window.title(APP_NAME)
        cls.window.resizable(False, False)
        cls.window.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

        cls.create_tabs()

        cls.window.mainloop()

    @classmethod
    def create_tabs(cls):
        frame = Frame(cls.window)

        controls = Tab(cls, frame, 'Controls')
        inputs = Tab(cls, frame, 'Inputs')
        portfolios = Tab(cls, frame, 'Portfolios')
        performance = Tab(cls, frame, 'Performance')

        controls.select(0)
        cls.tabs = [controls, inputs, portfolios, performance]

        frame.pack()

    @classmethod
    def on_tab_clicked(cls, clicked_tab: Tab):
        for tab in cls.tabs:
            if tab != clicked_tab:
                tab.deselect()

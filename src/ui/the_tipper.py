from tkinter import *

from src.ui.tab import Tab

APP_NAME = 'The Tipper'
WINDOW_WIDTH = 900
WINDOW_HEIGHT = WINDOW_WIDTH * 5 // 8


class TheTipper:
    window = Tk()

    @classmethod
    def launch(cls):
        window = cls.window
        window.title(APP_NAME)
        window.resizable(False, False)
        window.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

        cls.create_tabs()

        window.mainloop()

    @classmethod
    def create_tabs(cls):
        frame = Frame(cls.window)

        controls = Tab(frame, 'Controls')
        inputs = Tab(frame, 'Inputs')
        portfolios = Tab(frame, 'Portfolios')
        performance = Tab(frame, 'Performance')

        frame.pack()

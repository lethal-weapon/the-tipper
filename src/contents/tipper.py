from tkinter import *

from src.ui.tab import Tab
from src.contents.control_content import ControlContent
from src.contents.input_content import InputContent
from src.contents.portfolio_content import PortfolioContent
from src.contents.performance_content import PerformanceContent
from src.utils.constants import Widget, Misc


class Tipper:
    window = Tk()
    tabs = []
    contents = []

    @classmethod
    def launch(cls):
        cls.window.title(Misc.APP_NAME)
        cls.window.resizable(False, False)
        cls.window.geometry(f'{Widget.WINDOW_WIDTH}x{Widget.WINDOW_HEIGHT}')

        cls.create_tabs()
        cls.create_contents()
        cls.window.mainloop()

    @classmethod
    def create_tabs(cls):
        frame = Frame(cls.window)
        callback = cls.on_tab_clicked

        controls = Tab(frame, 'Controls', callback)
        inputs = Tab(frame, 'Inputs', callback)
        portfolios = Tab(frame, 'Portfolios', callback)
        performance = Tab(frame, 'Performance', callback)

        controls.select(0)
        cls.tabs = [controls, inputs, portfolios, performance]

        frame.pack()

    @classmethod
    def create_contents(cls):
        controls = Frame(cls.window)
        inputs = Frame(cls.window)
        portfolios = Frame(cls.window)
        performance = Frame(cls.window)

        ControlContent(controls)
        InputContent(inputs)
        PortfolioContent(portfolios)
        PerformanceContent(performance)

        cls.contents = [controls, inputs, portfolios, performance]
        controls.pack()

    @classmethod
    def on_tab_clicked(cls, clicked_tab: Tab):
        for i in range(len(cls.tabs)):
            if cls.tabs[i] != clicked_tab:
                cls.tabs[i].deselect()
                cls.contents[i].pack_forget()
            else:
                cls.contents[i].pack()

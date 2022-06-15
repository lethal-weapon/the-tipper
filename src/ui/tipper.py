from tkinter import *

from src.ui.tab import Tab
from src.ui.control_content import ControlContent
from src.ui.input_content import InputContent
from src.ui.portfolio_content import PortfolioContent
from src.ui.performance_content import PerformanceContent
from src.utils.constants import APP_NAME, Widget


class Tipper:
    window = Tk()
    tabs = []
    contents = []

    @classmethod
    def launch(cls):
        cls.window.title(APP_NAME)
        cls.window.resizable(False, False)
        cls.window.geometry(f'{Widget.WINDOW_WIDTH}x{Widget.WINDOW_HEIGHT}')

        cls.create_tabs()
        cls.create_contents()
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

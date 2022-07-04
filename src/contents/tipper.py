from tkinter import Tk, Frame

from src.ui.tab import Tab
from src.contents.control_content import ControlContent
from src.contents.input_content import InputContent
from src.contents.portfolio_content import PortfolioContent
from src.contents.performance_content import PerformanceContent
from src.utils.constants import Widget
from src.settings import SETTINGS


class Tipper:
    window = Tk()
    tabs = []
    contents = []

    @classmethod
    def launch(cls):
        cls.window.title(SETTINGS.BASE.APP)
        cls.window.resizable(False, False)
        cls.window.geometry(
            f'{Widget.WINDOW_WIDTH}x{Widget.WINDOW_HEIGHT}'
            f'+{Widget.INITIAL_X}+{Widget.INITIAL_Y}'
        )

        cls.create_tabs()
        cls.create_contents()
        cls.window.mainloop()

    @classmethod
    def create_tabs(cls):
        frame = Frame(cls.window)
        callback = cls.on_tab_clicked

        controls = Tab(frame, callback, 'Controls')
        inputs = Tab(frame, callback, 'Inputs')
        portfolios = Tab(frame, callback, 'Portfolios')
        performance = Tab(frame, callback, 'Performance')

        portfolios.select()
        cls.tabs = [controls, inputs, portfolios, performance]

        frame.pack()

    @classmethod
    def create_contents(cls):
        controls = Frame(cls.window)
        inputs = Frame(cls.window)
        portfolios = Frame(cls.window)
        performance = Frame(cls.window)

        input_cont = InputContent(inputs)
        port_cont = PortfolioContent(portfolios)
        perf_cont = PerformanceContent(performance)
        contr_cont = ControlContent(
            controls,
            cls.recreate_input_content,
            port_cont.refresh,
        )

        cls.contents = [controls, inputs, portfolios, performance]
        portfolios.pack()

    @classmethod
    def on_tab_clicked(cls, clicked_tab: Tab):
        for i in range(len(cls.tabs)):
            if cls.tabs[i] != clicked_tab:
                cls.tabs[i].deselect()
                cls.contents[i].pack_forget()
            else:
                cls.contents[i].pack()

    @classmethod
    def recreate_input_content(cls):
        cls.contents[1].pack_forget()
        cls.contents[1].destroy()

        new_input_frame = Frame(cls.window)
        InputContent(new_input_frame)
        cls.contents[1] = new_input_frame

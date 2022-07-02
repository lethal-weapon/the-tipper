from tkinter import Frame, Label, RIGHT

from src.utils.constants import Style, Color, MessageLevel


class Content:

    def __init__(self, parent_widget):
        self.frame = Frame(parent_widget)
        self.message = Label(self.frame, font='Times 12')
        self.set_message(MessageLevel.INFO, 'Good Day & Good Luck!')

    def pack_message(self):
        self.message.pack(side=RIGHT)

    def set_message(self, level: str, text: str):
        self.message.__setitem__(Style.TEXT, text)

        if level == MessageLevel.INFO:
            self.message.__setitem__(Style.FG, Color.BLUE)
        elif level == MessageLevel.ERROR:
            self.message.__setitem__(Style.FG, Color.RED)
        elif level == MessageLevel.SUCCESS:
            self.message.__setitem__(Style.FG, Color.GREEN)

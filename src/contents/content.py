from tkinter import Frame, Label, RIGHT

from src.utils.constants import Style, Color, MessageLevel


class Content:

    def __init__(self, parent_widget):
        self.frame = Frame(parent_widget)
        self.message = Label(self.frame, font='Times 13')
        self.set_info_message('Good Day & Good Luck!')

    def pack_message(self):
        self.message.pack(side=RIGHT)

    def clear_message(self):
        self.set_info_message('')

    def set_info_message(self, message: str):
        self.__set_message(MessageLevel.INFO, message)

    def set_error_message(self, message: str):
        self.__set_message(MessageLevel.ERROR, message)

    def set_success_message(self, message: str):
        self.__set_message(MessageLevel.SUCCESS, message)

    def __set_message(self, level: str, text: str):
        self.message.__setitem__(Style.TEXT, text)

        if level == MessageLevel.INFO:
            self.message.__setitem__(Style.FG, Color.BLUE)
        elif level == MessageLevel.ERROR:
            self.message.__setitem__(Style.FG, Color.RED)
        elif level == MessageLevel.SUCCESS:
            self.message.__setitem__(Style.FG, Color.GREEN)

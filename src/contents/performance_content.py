from tkinter import Frame, Label, Radiobutton, StringVar, LEFT

from src.ui.dropdown import Dropdown
from src.contents.content import Content
from src.utils.constants import Color

PAGE_OPTIONS = {
    'Tipster': [
        'Last day',
        'Recent 3 days',
        'Recent 5 days',
        'Recent 10 days',
        'All times',
    ],
    'Jockey': [
        'Meeting',
        'Earning 22/23',
        'Earning 21/22',
    ],
}


class PerformanceContent(Content):

    def __init__(self, parent_widget):
        super().__init__(parent_widget)

        self.header_frame = Frame(self.frame)
        self.option_key = StringVar()
        self.option_list = None
        self.build_header_frame()
        self.header_frame.pack()

        self.content_frame = None
        self.update_content_frame()
        self.frame.pack()

    def build_header_frame(self):
        for k in PAGE_OPTIONS.keys():
            Radiobutton(
                self.header_frame,
                text=k,
                value=k,
                variable=self.option_key,
                command=self.update_option_list,
                font='Times 16 bold',
            ).pack(padx=15, pady=10, side=LEFT)

        self.option_key.set('Tipster')

        Label(
            self.header_frame,
            text='By',
            font='Times 16 italic',
            fg=Color.BLUE,
        ).pack(padx=20, side=LEFT)

        self.option_list = Dropdown(
            self.header_frame,
            PAGE_OPTIONS[self.option_key.get()],
            self.update_content_frame,
            {'side': LEFT, 'padx': 15},
        )

    def update_option_list(self, *e):
        self.option_list.set_options(
            PAGE_OPTIONS[self.option_key.get()]
        )
        self.update_content_frame()

    def update_content_frame(self, *e):
        if self.content_frame:
            self.content_frame.pack_forget()
            self.content_frame.destroy()

        self.content_frame = Frame(self.frame)
        self.build_content_frame()
        self.content_frame.pack()

    def build_content_frame(self):
        text = \
            f'{self.option_key.get()} / {self.option_list.get_selected_option()}'
        Label(
            self.content_frame,
            text=text,
        ).pack(pady=30)

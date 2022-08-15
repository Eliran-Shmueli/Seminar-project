from tkinter import *
from tkinter import ttk


class TreeviewTemp(ttk.Treeview):
    column_index = 0
    row_index = 0
    font = 'Helvetica 12'

    def __init__(self, master, height, mode, columns,change_width):
        """
        init ListBoxTemp
        :param master: main root
        :param height: number of objects
        :param mode: selection mode
        """
        self.frame = Frame(master)
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=('Calibri', 11))  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))  # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders
        super().__init__(self.frame, height=height, columns=columns, show='headings', selectmode=mode,
                         style="mystyle.Treeview")
        if change_width:
            for column in columns:
                self.column(column, stretch=True, width=150)
        # link a scrollbar to a list
        scrollbar = Scrollbar(self.frame, orient='vertical', command=self.yview)
        # place in grid (frame)
        self['yscrollcommand'] = scrollbar.set
        self.grid(column=self.column_index, row=self.row_index, sticky='nwes')
        scrollbar.grid(column=self.column_index + 1, row=self.row_index, sticky='ns')

    def add_headers(self, tags):
        """
        add headers to treeview
        :param tags: list of tuples - 0- tag, 1- header name
        """

        for tag in tags:
            self.heading(tag[0], text=tag[1], anchor=W)

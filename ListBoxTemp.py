from tkinter import *
from tkinter import ttk


class ListBoxTemp(ttk.Treeview):
    column = 0
    row = 0
    font = 'Helvetica 12'

    def __init__(self, master, height, mode):
        """
        init ListBoxTemp
        :param master: main root
        :param height: number of objects
        :param mode: selection mode
        """
        self.frame = Frame(master)
        columns = ('id', 'name')
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=('Calibri', 11))  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))  # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders
        super().__init__(self.frame, height=height, columns=columns, show='headings', selectmode=mode,
                         style="mystyle.Treeview")

        # link a scrollbar to a list
        scrollbar = Scrollbar(self.frame, orient='vertical', command=self.yview)
        # place in grid (frame)
        self['yscrollcommand'] = scrollbar.set
        self.grid(column=self.column, row=self.row, sticky='nwes')
        scrollbar.grid(column=self.column + 1, row=self.row, sticky='ns')

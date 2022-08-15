from TreeviewTemp import TreeviewTemp
from tkinter import *


class FrameReport(Frame):
    pad_y = 10
    pad_y_label = 2
    pad_x = 10
    title_font = 'Helvetica 20 underline bold'
    font = 'Helvetica 12'

    def __init__(self, root, title, columns, tags,change_width):
        super().__init__(master=root)
        self.is_show = False
        self.root = root
        self.list_widgets = []
        self.B_to_main_menu = None
        self.L_title = None
        self.report_treeview = TreeviewTemp(self, 6, 'none', columns,change_width)
        self.report_treeview.add_headers(tags)
        self.create_frame_report(title)

    def add_data(self, data):
        """
        adds data to treeview
        :param data: list of tuples
        """
        for line in data:
            self.report_treeview.insert('', END, values=line)

    def clear_data(self):
        for line_index in self.report_treeview.get_children():
            self.report_treeview.delete(line_index)

    def create_frame_report(self, title):
        """
        creates and edits frame report
        """
        self.L_title = Label(self, text=title, font=self.title_font)
        img_back = PhotoImage(file='images/buttons/back-button.png')
        self.B_to_main_menu = Button(self, image=img_back, command=self.show_main_menu, bd=0)
        self.B_to_main_menu.image = img_back

        self.L_title.grid(row=0, column=0, columnspan=4, pady=self.pad_y * 2)
        self.report_treeview.frame.grid(row=1, column=0, columnspan=1, pady=self.pad_y)
        # self.B_to_main_menu.grid(row=5, column=0, columnspan=4, pady=self.pad_y)

        self.list_widgets = [self.L_title, self.B_to_main_menu]

    def show_main_menu(self):
        """
        hide frame info and shows main menu
        """
        self.grid_forget()
        self.F_main_menu.grid(row=0, column=0)

    def get_attributes(self, obj, *items):
        values = []
        for item in items:
            values.append(getattr(obj, item))
        return tuple(values)

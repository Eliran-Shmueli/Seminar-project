from TreeviewTemp import TreeviewTemp
from tkinter import *


class FrameReport(Frame):
    pad_y = 10
    pad_y_label = 6
    pad_x = 10
    title_font = 'Helvetica 20 underline bold'
    font = 'Helvetica 12'

    def __init__(self, root, title, columns, tags, change_width):
        super().__init__(master=root)
        self.is_show = False
        self.root = root
        self.list_widgets = []
        self.title = title
        self.report_treeview = TreeviewTemp(self, 9, 'none', columns, change_width)
        self.report_treeview.add_headers(tags)
        self.create_frame_report(title)

    def add_data(self, list_data):
        """
        adds data to treeview
        :param list_data: list of tuples
        """

        for line in list_data:
            data_tuple = self.get_attributes(line, list(line.tags.keys()))
            self.report_treeview.insert('', END, values=data_tuple)

    def clear_data(self):
        for line_index in self.report_treeview.get_children():
            self.report_treeview.delete(line_index)

    def create_frame_report(self, title):
        """
        creates and edits frame report
        """
        L_title = Label(self, text=title, font=self.title_font)

        L_title.grid(row=0, column=0, columnspan=1, pady=self.pad_y_label)
        self.report_treeview.frame.grid(row=1, column=0, columnspan=1, pady=self.pad_y)

        self.list_widgets = [self, L_title, self.report_treeview]

    def show_main_menu(self):
        """
        hide frame info and shows main menu
        """
        self.grid_forget()
        self.F_main_menu.grid(row=0, column=0)

    def get_attributes(self, obj, items):
        """
        get attributes values from an object and returns tuple
        :param obj: object
        :param items: list of object's attributes names
        :return: tuple
        """
        values = []
        for item in items:
            values.append(getattr(obj, item))
        return tuple(values)

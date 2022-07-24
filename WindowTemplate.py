import threading
import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter import *
import winsound
import logging
import pygame


class WindowTemplate:
    pad_x = 20
    pad_y = 20
    title_font = 'Helvetica 20 underline bold'
    font = 'Helvetica 12'
    music_volume = 0.4

    def __init__(self, window_name,window):
        logging.basicConfig(filename=window_name + '.log', filemode='w', format='%(asctime)s - %(message)s',
                            level=logging.INFO)
        print('thread id '+str(threading.get_ident()))
        self.menubar = None
        self.root = window
        self.widgets_dic = {"label": [], "button": [], "listbox": [], "frame": []}
        self.playing_music = True
        self.init_background_music()
        self.edit_template(window_name)
        self.add_widgets(self.root)

    def init_background_music(self):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.music_volume)

    def load_background_music(self, path, loop):
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(loop)

    def mute_background_music(self):
        if self.playing_music is True:
            logging.info('Music turned off')
            pygame.mixer.music.set_volume(0)
            self.playing_music = False
        else:
            pygame.mixer.music.set_volume(self.music_volume)
            logging.info('Music turned on')
            self.playing_music = True

    def click_sound_valid(self):
        winsound.PlaySound('sounds/mixkit-select-click-1109.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

    def click_sound_error(self):
        winsound.PlaySound('sounds/mixkit-click-error-1110.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

    def edit_template(self, window_name):
        """
edit window template
        :param window_name: the title of the window
        """
        self.root.geometry('+0+0')
        self.root.resizable(False, False)
        self.root.title(window_name)
        self.root.columnconfigure(3, weight=1)
        self.root.columnconfigure(4, weight=3)
        self.add_menubar()

    def add_menubar(self):
        """
creates and commands to it
        """
        # create a menubar
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)
        # create a menu
        file_menu = Menu(self.menubar, tearoff=0)
        file_menu.add_command(
            label='Change text color',
            command=lambda: self.change_text_color())
        file_menu.add_command(
            label='Change buttons color',
            command=lambda: self.change_buttons_color()
        )
        file_menu.add_command(
            label='Change background color',
            command=lambda: self.change_background_color()
        )

        file_menu.add_checkbutton(label="Mute music", command=self.mute_background_music)
        file_menu.add_separator()
        # add a menu item to the menu
        file_menu.add_command(
            label='Exit',
            command=lambda: self.exit_app()
        )
        # add the File menu to the menubar
        self.menubar.add_cascade(
            label="File",
            menu=file_menu
        )

    def exit_app(self):
        self.click_sound_valid()
        logging.info('Exit program')
        self.root.destroy()

    def change_buttons_color(self):
        color = askcolor()[1]
        logging.info('The buttons color was changed to ' + color)
        for key in self.widgets_dic.keys():
            if key == "button":
                for widget in self.widgets_dic[key]:
                    widget.configure(bg=color)

    def change_background_color(self):
        color = askcolor()[1]
        logging.info('The background color was changed to ' + color)
        for key in self.widgets_dic.keys():
            if (key != "listbox") and (key != "button"):
                for widget in self.widgets_dic[key]:
                    widget.configure(bg=color)

    def change_text_color(self):
        color = askcolor()[1]
        logging.info('The text color was changed to ' + color)
        for key in self.widgets_dic.keys():
            if key != "frame":
                for widget in self.widgets_dic[key]:
                    widget.configure(fg=color)

    def add_widgets(self, *widgets):
        for widget in widgets:
            if type(widget) == Label:
                self.widgets_dic["label"].append(widget)
            if type(widget) == Button:
                self.widgets_dic["button"].append(widget)
            if (type(widget) == ListBoxTemp) or (type(widget) == Entry):
                self.widgets_dic["listbox"].append(widget)
            if (type(widget) == Frame) or (type(widget) == Tk):
                self.widgets_dic["frame"].append(widget)


class ListBoxTemp(Listbox):
    column = 0
    row = 0
    font = 'Helvetica 12'

    def __init__(self, master, height, width, mode):
        self.frame = Frame(master)
        super().__init__(self.frame, height=height, width=width, selectmode=mode, font=self.font)

        # link a scrollbar to a list
        scrollbar = Scrollbar(self.frame, orient='vertical', command=self.yview)
        # place in grid (frame)
        self['yscrollcommand'] = scrollbar.set
        self.grid(column=self.column, row=self.row, sticky='nwes')
        scrollbar.grid(column=self.column + 1, row=self.row, sticky='ns')

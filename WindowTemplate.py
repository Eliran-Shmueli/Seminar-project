import queue
import threading
from tkinter.colorchooser import askcolor
from tkinter import *
import winsound
import logging
import pygame
import time
from FrameInfo import FrameInfo
from FrameReport import FrameReport
from TreeviewTemp import TreeviewTemp


class WindowTemplate:
    window_width = 700
    window_height = 700
    pad_x = 15
    pad_y = 10
    title_font = 'Helvetica 20 underline bold'
    font = 'Helvetica 12'
    music_volume = 0.4
    num_of_channels = 1
    name_length = 12

    def __init__(self, window_name, is_server):
        """
        init WindowTemplate
        :param window_name: name of the window
        :param is_server: boolean, true - server, false - client
        """
        self.channel = None
        self.event_id = None
        self.menubar = None
        self.root = Tk()
        self.root.attributes("-topmost", True)
        self.Q_messages_received = queue.Queue()
        self.Q_messages_send = queue.Queue()
        self.widgets_dic = {"label": [], "button": [], "listbox": [], "frame": []}
        self.playing_music = True
        self.run_call = True
        self.event = threading.Event()
        logging.basicConfig(filename=window_name + '.log', filemode='w', format='%(asctime)s - %(message)s',
                            level=logging.INFO)
        print('thread id ' + str(threading.get_ident()))
        self.init_background_music()
        self.config_template(window_name, is_server)
        self.add_widgets(self.root)

    def init_background_music(self):
        """
        init background music
        """
        pygame.mixer.init()
        for channel_num in range(self.num_of_channels):
            pygame.mixer.Channel(channel_num).set_volume(self.music_volume)

    def load_background_music(self, channel, path, loop):
        """
        load background music to specific a channel
        :param channel: music channel
        :param path: music path
        :param loop: number of loops
        """
        self.channel = channel
        pygame.mixer.Channel(self.channel).play(pygame.mixer.Sound(path), loop)

    def mute_background_music(self, channel):
        """
        mute background music in a specific channel
        :param channel: music channel
        """
        if self.playing_music is True:
            logging.info('Music turned off')
            pygame.mixer.Channel(channel).set_volume(0)
            self.playing_music = False
        else:
            pygame.mixer.Channel(channel).set_volume(self.music_volume)
            logging.info('Music turned on')
            self.playing_music = True

    def config_template(self, window_name, is_server):
        """
        configure window template
        :param is_server: boolean, true - server, false - client
        :param window_name: the title of the window
        """
        if is_server:
            #  self.root.geometry('+0+0')
            self.root.geometry('1500x750')
        else:
            self.config_geometry()
        self.root.resizable(True, True)
        self.root.title(window_name)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.iconbitmap(r'images/icons/mushroom.ico')
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)
        self.add_menubar()

    def config_geometry(self):
        """
        configure game window geometry
        """
        # get the screen dimension
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # find the center point
        center_x = int(screen_width / 2 - self.window_width / 2)
        center_y = int(screen_height / 2 - self.window_height / 2)
        # set the position of the window to the center of the screen
        self.root.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')

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
        """
        closing mixer and closing window
        """
        self.click_sound_exit()
        time.sleep(1)
        logging.info('Exit program')
        pygame.mixer.quit()
        self.root.quit()

    def change_buttons_color(self):
        """
        changing buttons color
        """
        color = askcolor()[1]
        if color is not None:
            logging.info('The buttons color was changed to ' + color)
            for key in self.widgets_dic.keys():
                if key == "button":
                    for widget in self.widgets_dic[key]:
                        widget.configure(bg=color)

    def change_background_color(self):
        """
        changing background color
        """
        color = askcolor()[1]
        if color is not None:
            logging.info('The background color was changed to ' + color)
            self.root.configure(bg=color)
            for key in self.widgets_dic.keys():
                if key != "listbox":
                    for widget in self.widgets_dic[key]:
                        widget.configure(bg=color)

    def change_text_color(self):
        """
        changing text color
        """
        color = askcolor()[1]
        if color is not None:
            logging.info('The text color was changed to ' + color)
            for key in self.widgets_dic.keys():
                if key != "frame" and key != "listbox":
                    for widget in self.widgets_dic[key]:
                        widget.configure(fg=color)

    def add_widgets(self, *widgets):
        """
        adds widgets to dictionary by type
        :param widgets: list of widgets
        """
        for widget in widgets:
            if type(widget) == Label:
                self.widgets_dic["label"].append(widget)
            if type(widget) == Button:
                self.widgets_dic["button"].append(widget)
            if (type(widget) == TreeviewTemp) or (type(widget) == Entry):
                self.widgets_dic["listbox"].append(widget)
            if (type(widget) == Frame) or (type(widget) == Tk) or (type(widget) == FrameInfo) or (
                    type(widget) == FrameReport):
                self.widgets_dic["frame"].append(widget)
            if type(widget) == list:
                for obj in widget:
                    self.add_widgets(obj)

    def check_queue_received(self):
        pass

    def call_after_func(self):
        """
        recursive function that calls function check_queue_received every 1 seconds,
        """
        if self.run_call is True:
            self.root.after(1000, self.check_queue_received)

    def click_sound_valid(self):
        """
        play valid sound on click
        """
        winsound.PlaySound('sounds/mixkit-select-click-1109.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

    def click_sound_error(self):
        """
        play error sound on click
        """
        winsound.PlaySound('sounds/mixkit-click-error-1110.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

    def click_sound_exit(self):
        """
        play exit sound on click
        """
        winsound.PlaySound('sounds/sci-fi-voiceclip-894-sound-effect-goodbye.wav',
                           winsound.SND_FILENAME | winsound.SND_ASYNC)

# Music by FASSounds from Pixabay
import multiprocessing
import time

from FrameInfo import FrameInfo
from GifLabel import GifLabel
from ToolTip import CreateToolTip
from WindowTemplate import WindowTemplate, ListBoxTemp
import GameWindow
from tkinter import *
from Player import Player
import logging
import threading
from Server import Server
from Message import Message


class ServerWindow(WindowTemplate):
    pad_y = 10
    pad_x = 10

    def __init__(self, window_name):
        super().__init__(window_name)
        self.dic_players = {}
        self.player_id_count = 0
        self.load_background_music(0, 'sounds/best-time-112194.wav', -1)
        self.F_main_menu = Frame(self.root)
        self.F_player_info = FrameInfo(self.root, self.F_main_menu)
        self.add_widgets(self.F_player_info.list_widgets)
        self.listbox = ListBoxTemp(self.F_main_menu, 6, 'browse')
        self.edit_listbox()
        self.edit_server_frame()
        self.T_server = threading.Thread(
            target=Server(self.Q_messages_send, self.Q_messages_received, self.dic_players, self.event).run)
        self.T_server.start()
        self.call_after_func()
        logging.info('Server window started')

    def add_new_player(self, name):
        self.player_id_count = self.player_id_count + 1
        player_new = Player(self.player_id_count, name)
        self.listbox.insert('', END, values=(self.player_id_count, name))
        self.create_player_process(player_new)
        self.dic_players[self.player_id_count] = player_new
        logging.info('Player ' + "Id: " + str(self.player_id_count) + ", Name: " + name + ' was added')
        return self.player_id_count

    def mute_background_music(self):
        super().mute_background_music(0)

    def check_queue_received(self):
        if self.Q_messages_received.empty() is False:
            key, message = self.Q_messages_received.get()
            self.actions(message)
        self.call_after_func()

    def actions(self, message):
        if message.is_message_exit():
            self.delete_player_by_id(message.id)
        if message.is_message_game_info_request() and message.is_message_have_data():
            game_info = message.data
            self.F_main_menu.pack_forget()
            self.F_player_info.edit(game_info)
            self.F_player_info.pack()

    def accept_request_to_connect_from_client(self, key, message):
        new_player_id = self.add_new_player(message.data)
        message_to_send = Message(new_player_id)
        message_to_send.set_message_join_request()
        self.dic_players[new_player_id].socket = key
        self.send_message_to_player(new_player_id, message_to_send)

    def edit_listbox(self):
        self.listbox.heading('id', text="Player's id", anchor=W)
        self.listbox.heading('name', text="Player's name", anchor=W)

    def delete_selected_player_from_listbox(self):
        self.click_sound_valid()
        selected_player = self.listbox.selection()
        if selected_player:
            player_info = self.listbox.item(selected_player[0]).get("values")
            player_id = player_info[0]
            player_name = player_info[1]
            self.listbox.delete(selected_player[0])
            self.disconnect_client(player_id)
            logging.info('Player id: ' + str(player_id) + ', name: ' + player_name + 'was disconnected')
        else:
            self.click_sound_error()

    def delete_all_players_from_listbox(self):
        if len(self.listbox.get_children()) != 0:
            self.click_sound_valid()
            for player_index in self.listbox.get_children():
                self.listbox.delete(player_index)
            for player_id in self.dic_players.keys():
                self.disconnect_client(player_id)
        else:
            self.click_sound_error()

    def delete_player_by_id(self, player_id):
        player_list = self.listbox.get_children()
        for player_index in player_list:
            player_index_id = self.listbox.item(player_index).get("values")[0]
            if player_index_id == player_id:
                self.listbox.delete(player_index)

    def disconnect_client(self, player_id):
        message = Message(player_id)
        message.set_message_exit()
        self.send_message_to_player(player_id, message)

    def send_message_to_player(self, player_id, message):
        key = self.dic_players[player_id].socket
        self.Q_messages_send.put((key, message))

    def create_buttons_frame(self):
        # creating widgets
        img_player_info = PhotoImage(file='images/buttons/user-info.png')
        img_player_disconnect = PhotoImage(file='images/buttons/delete-user.png')
        img_player_disconnect_all = PhotoImage(file='images/buttons/delete-all.png')

        F_buttons = Frame(self.F_main_menu)
        B_player_info = Button(F_buttons, image=img_player_info, font=self.font, bd=0,
                               command=self.get_player_info)
        B_disconnect_player = Button(F_buttons, image=img_player_disconnect, font=self.font, bd=0,
                                     command=self.delete_selected_player_from_listbox)
        B_disconnect_all = Button(F_buttons, image=img_player_disconnect_all, font=self.font, bd=0,
                                  command=self.delete_all_players_from_listbox)

        B_player_info.image = img_player_info
        B_disconnect_player.image = img_player_disconnect
        B_disconnect_all.image = img_player_disconnect_all

        # place in grid
        B_player_info.grid(row=0, column=0, sticky='ew')
        B_disconnect_player.grid(row=1, column=0, pady=self.pad_y * 2, sticky='ew')
        B_disconnect_all.grid(row=2, column=0, sticky='ew')

        CreateToolTip(B_player_info, text="Get player info")
        CreateToolTip(B_disconnect_player, text="Disconnect selected player")
        CreateToolTip(B_disconnect_all, text="Disconnect all players")
        # add to widgets list
        self.add_widgets(B_disconnect_player, B_disconnect_all, B_player_info)
        return F_buttons

    def edit_server_frame(self):
        # creating widgets
        F_addPlayer = self.create_add_player_frame(self.F_main_menu)
        L_title = Label(self.F_main_menu, text="R.P.S - Server", font=self.title_font)
        L_gif = GifLabel(self.F_main_menu)
        F_buttons = self.create_buttons_frame()
        # adding image
        L_gif.load('images/gif/Rock-Paper-Scissors-smaller.gif')
        # place in Frame
        self.F_main_menu.pack()
        L_title.grid(row=0, column=0, columnspan=2, pady=self.pad_y * 2)
        self.listbox.frame.grid(row=1, column=0, columnspan=1, pady=self.pad_y)
        F_buttons.grid(row=1, column=1, columnspan=1, pady=self.pad_y, sticky='wn')
        F_addPlayer.grid(row=2, column=0, columnspan=2, pady=self.pad_y, sticky='w')

        L_gif.grid(row=3, column=0, columnspan=2, pady=self.pad_y, padx=self.pad_x)
        # add to widgets list
        self.add_widgets(L_gif, L_title, self.listbox, self.F_main_menu, F_buttons)

    def get_player_info(self):
        self.click_sound_valid()
        selected_player = self.listbox.selection()
        if selected_player:
            player_info = self.listbox.item(selected_player[0]).get("values")
            player_id = player_info[0]
            message = Message(player_id)
            message.set_message_game_info_request()
            self.send_message_to_player(player_id, message)
            player_name = player_info[1]

            logging.info('Getting player id: ' + str(player_id) + ', name: ' + player_name + 'information')
        else:
            self.click_sound_error()

    def exit_app(self):
        self.delete_all_players_from_listbox()
        # self.p.terminate()
        while bool(self.dic_players) is True:
            time.sleep(1)

        self.run_call = False
        self.event.set()
        super().exit_app()

    def create_player_process(self, player_new):
        player_process = multiprocessing.Process(target=GameWindow.GameWindow, args=(player_new.id, player_new.name,))
        player_process.start()

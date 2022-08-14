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


def create_player_process(player_new):
    """
    creating and starting new game process
    :param player_new: player object
    """
    player_process = multiprocessing.Process(target=GameWindow.GameWindow,
                                             args=(player_new.get_id(), player_new.get_name(),))
    player_process.start()


class ServerWindow(WindowTemplate):
    pad_y = 10
    pad_x = 10

    def __init__(self):
        """
        init server window
        """
        super().__init__("R.P.S - Server", True)
        self.root.geometry('+0+0')
        self.L_error_msg = None
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
        """
        adds new player to the server
        :param name: name of the player
        :return: player's id
        """
        self.player_id_count = self.player_id_count + 1
        player_new = Player(self.player_id_count, name)
        self.listbox.insert('', END, values=(self.player_id_count, name))
        create_player_process(player_new)
        self.dic_players[self.player_id_count] = player_new
        logging.info('Player ' + "Id: " + str(self.player_id_count) + ", Name: " + name + ' was added')
        return self.player_id_count

    def mute_background_music(self, channel=0):
        """
        mute background music
        """
        super().mute_background_music(channel)

    def check_queue_received(self):
        """
        checks queue of received messages
        """
        if self.Q_messages_received.empty() is False:
            key, message = self.Q_messages_received.get()
            self.actions(message)
        self.call_after_func()

    def actions(self, message):
        """
        actions to do according to the received message
        :param message: received message
        """
        if message.is_message_exit():
            self.delete_player_by_id(message.id)
        if message.is_message_game_info_request() and message.is_message_have_data():
            game_info = message.data
            self.F_main_menu.grid_forget()
            self.F_player_info.edit(game_info)
            self.F_player_info.grid(row=0, column=0)

    def edit_listbox(self):
        """
        edits listbox heading
        """
        self.listbox.heading('id', text="Player's id", anchor=W)
        self.listbox.heading('name', text="Player's name", anchor=W)

    def get_player_info(self):
        """
        get selected player information from client
        """
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

    def delete_selected_player_from_listbox(self):
        """
        delete selected player by the user from listbox and disconnect it
        """
        self.click_sound_valid()
        selected_player = self.listbox.selection()
        if selected_player:
            player_info = self.listbox.item(selected_player[0]).get("values")
            player_id = player_info[0]
            player_name = player_info[1]
            self.delete_player_by_id(player_id)
            logging.info('Player id: ' + str(player_id) + ', name: ' + player_name + 'was disconnected')
        else:
            self.click_sound_error()

    def delete_all_players_from_listbox(self):
        """
        delete all players from listbox and disconnect all of them
        """
        if len(self.listbox.get_children()) != 0:
            self.click_sound_valid()
            for player_id in list(self.dic_players):
                self.delete_player_by_id(player_id)
        else:
            self.click_sound_error()

    def delete_player_by_id(self, player_id):
        """
        delete player from the listbox and disconnect him by id
        :param player_id: player's id
        """
        player_list = self.listbox.get_children()
        for player_index in player_list:
            player_index_id = self.listbox.item(player_index).get("values")[0]
            if player_index_id == player_id:
                if self.dic_players[player_id].socket is not None:
                    self.listbox.delete(player_index)
                    self.disconnect_client(player_id)
                else:
                    time.sleep(1)
                    self.delete_player_by_id(player_id)

    def disconnect_client(self, player_id):
        """
        send message to disconnect player
        :param player_id:
        """
        message = Message(player_id)
        message.set_message_exit()
        self.send_message_to_player(player_id, message)

    def send_message_to_player(self, player_id, message):
        """
        send message to player
        :param player_id: the id of the player to send to
        :param message: message
        """
        key = self.dic_players[player_id].socket
        self.Q_messages_send.put((key, message))

    def create_buttons_frame(self):
        """
        creates frame with buttons to add, delete and delete all users actions
        :return: frame
        """
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
        """
        edit main server frame
        """
        # creating widgets

        F_addPlayer = self.create_add_player_frame(self.F_main_menu)
        L_title = Label(self.F_main_menu, text="R.P.S - Server", font=self.title_font)
        self.L_error_msg = Label(self.F_main_menu, text="", font=self.font)
        L_gif = GifLabel(self.F_main_menu)
        F_buttons = self.create_buttons_frame()
        # adding image
        L_gif.load('images/gif/Rock-Paper-Scissors-smaller.gif')
        # place in Frame
        self.F_main_menu.grid(row=0, column=0, padx=self.pad_x)
        L_title.grid(row=0, column=0, columnspan=2, pady=self.pad_y * 2)
        self.listbox.frame.grid(row=1, column=0, columnspan=1, pady=self.pad_y)
        F_buttons.grid(row=1, column=1, columnspan=1, pady=self.pad_y, sticky='wn')
        F_addPlayer.grid(row=2, column=0, columnspan=2, pady=self.pad_y, sticky='w')
        self.L_error_msg.grid(row=3, column=0, columnspan=2, sticky='w')

        L_gif.grid(row=4, column=0, columnspan=2, pady=self.pad_y, padx=self.pad_x)
        # add to widgets list
        self.add_widgets(L_gif, L_title, self.L_error_msg, self.listbox, self.F_main_menu, F_buttons)

    def create_add_player_frame(self, root):
        """
        creates frame to add new player
        :param root: server main root
        :return: frame
        """
        F_addPlayer = Frame(root)

        L_addPlayer = Label(F_addPlayer, text="Player's name:", font=self.font, padx=self.pad_x)
        E_playerName = Entry(F_addPlayer, font=self.font)
        img_add_player = PhotoImage(file='images/buttons/add-user.png')
        B_addPlayer = Button(F_addPlayer, image=img_add_player, font=self.font, bd=0,
                             command=lambda: self.set_player_name(E_playerName))
        B_addPlayer.image = img_add_player

        # place in F_addPlayer
        L_addPlayer.pack(side=LEFT)
        E_playerName.pack(side=LEFT)
        B_addPlayer.pack(side=LEFT, padx=self.pad_x)

        CreateToolTip(B_addPlayer, "Add player")
        # add to widgets list
        self.add_widgets(B_addPlayer, L_addPlayer, E_playerName, F_addPlayer)
        return F_addPlayer

    def set_player_name(self, E_playerName):
        """
        get name from entry and checks if name is valid
        :param E_playerName: Entry of add player frame
        """
        name = E_playerName.get()
        if (len(name) != 0) and (name.isalpha() and (len(name) <= self.name_length)):
            self.click_sound_valid()
            self.L_error_msg.configure(text="")
            E_playerName.delete(0, 'end')
            self.add_new_player(name)
        else:
            self.click_sound_error()
            self.L_error_msg.configure(text="Error: Name can be only with letters, no spaces and in max length of 12")

    def exit_app(self):
        """
        closing all connections and closing the app
        """
        self.delete_all_players_from_listbox()
        while bool(self.dic_players) is True:
            time.sleep(1)

        self.run_call = False
        self.event.set()
        super().exit_app()

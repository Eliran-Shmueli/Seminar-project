# Music by FASSounds from Pixabay
import multiprocessing
import operator
import time

from ClickSounds import click_sound_valid, click_sound_error
from FrameInfo import FrameInfo
from FrameReport import FrameReport
from GameInfo import GameInfo
from GifLabel import GifLabel
from PlayerInfo import PlayerInfo
from ToolTip import CreateToolTip
from WindowTemplate import WindowTemplate, TreeviewTemp
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


def return_list_of_tuples(dict_data):
    """
    returns list of tuples from dictionary
    :param dict_data: dictionary
    :return: list of tuples
    """
    return [(k, v) for k, v in dict_data.items()]


class ServerWindow(WindowTemplate):
    pad_y = 10
    pad_x = 10

    def __init__(self):
        """
        init server window
        """
        super().__init__("R.P.S - Server", True)
        self.B_show_games_report = None
        self.B_show_players_report = None
        self.L_gif = None
        self.L_error_msg = None
        self.dic_players_connected = {}
        self.dic_players_info = {}
        self.player_id_count = 0
        self.load_background_music(0, 'sounds/best-time-112194.wav', -1)
        self.F_main_menu = Frame(self.root)
        self.F_report_players = self.init_report_frame(PlayerInfo, "Players report")
        self.F_report_games = self.init_report_frame(GameInfo, "Games report")
        self.F_player_info = FrameInfo(self.root, self.F_main_menu)
        self.add_player_info(self.player_id_count, "Pc")
        self.add_widgets(self.F_player_info.list_widgets)
        self.treeview = None
        self.edit_server_frame()
        self.treeview.add_headers([('id', "Player's id"), ('name', "Player's name")])
        self.T_server = threading.Thread(
            target=Server(self.Q_messages_send, self.Q_messages_received, self.dic_players_connected, self.event).run)
        self.T_server.start()
        self.call_after_func()
        logging.info('Server window started')

    def add_player_info(self, player_id, name):
        """
        add player info to dictionary of players info
        :param player_id: player's id
        :param name: player's name
        """
        player_info = PlayerInfo(player_id, name)
        self.dic_players_info[player_id] = player_info
        self.update_report_frame(self.F_report_players, True)

    def add_new_player(self, name):
        """
        adds new player to the server
        :param name: name of the player
        :return: player's id
        """
        self.player_id_count = self.player_id_count + 1
        player_new = Player(self.player_id_count, name)
        self.add_player_info(player_new.get_id(), player_new.get_name())
        self.treeview.insert('', END, values=(self.player_id_count, name))
        create_player_process(player_new)
        self.dic_players_connected[self.player_id_count] = player_new
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
            player_info, game_info = message.data
            self.update_information(player_info, game_info)
            self.update_report_frame(self.F_report_players, True)
            self.update_report_frame(self.F_report_games, False)

    def update_information(self, new_player_info, game_info):
        """
        update players and games dictionaries
        :param new_player_info: new player info
        :param game_info: new game info
        """
        player_info = self.dic_players_info[new_player_info.get_id()]
        player_info.update_info(new_player_info, game_info)

    def show_player_info(self, player_info):
        """
        update and show player_info
        :param player_info: selected player info
        """
        self.F_main_menu.grid_forget()
        self.F_player_info.edit(player_info)
        self.F_player_info.grid(row=0, column=0)

    def get_player_info(self):
        """
        get selected player information from client
        """
        click_sound_valid()
        selected_player = self.treeview.selection()
        if selected_player:
            player_from_listbox = self.treeview.item(selected_player[0]).get("values")
            player_id = player_from_listbox[0]
            player_name = player_from_listbox[1]
            player_info = self.dic_players_info[player_id]
            self.show_player_info(player_info)
            logging.info('Getting player id: ' + str(player_id) + ', name: ' + player_name + 'information')
        else:
            click_sound_error()

    def delete_selected_player_from_listbox(self):
        """
        delete selected player by the user from listbox and disconnect it
        """
        click_sound_valid()
        selected_player = self.treeview.selection()
        if selected_player:
            player_info = self.treeview.item(selected_player[0]).get("values")
            player_id = player_info[0]
            player_name = player_info[1]
            self.delete_player_by_id(player_id)
            logging.info('Player id: ' + str(player_id) + ', name: ' + player_name + 'was disconnected')
        else:
            click_sound_error()

    def delete_all_players_from_listbox(self):
        """
        delete all players from listbox and disconnect all of them
        """
        if len(self.treeview.get_children()) != 0:
            click_sound_valid()
            for player_id in list(self.dic_players_connected):
                self.delete_player_by_id(player_id)
        else:
            click_sound_error()

    def delete_player_by_id(self, player_id):
        """
        delete player from the listbox and disconnect him by id
        :param player_id: player's id
        """
        player_list = self.treeview.get_children()
        for player_index in player_list:
            player_index_id = self.treeview.item(player_index).get("values")[0]
            if player_index_id == player_id:
                if self.dic_players_connected[player_id].socket is not None:
                    self.treeview.delete(player_index)
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
        key = self.dic_players_connected[player_id].socket
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
        img_players_report = PhotoImage(file='images/buttons/user_report.png')
        img_games_report = PhotoImage(file='images/buttons/game_report.png')

        F_buttons = Frame(self.F_main_menu)
        B_player_info = Button(F_buttons, image=img_player_info, font=self.font, bd=0,
                               command=self.get_player_info)
        B_disconnect_player = Button(F_buttons, image=img_player_disconnect, font=self.font, bd=0,
                                     command=self.delete_selected_player_from_listbox)
        B_disconnect_all = Button(F_buttons, image=img_player_disconnect_all, font=self.font, bd=0,
                                  command=self.delete_all_players_from_listbox)
        self.B_show_players_report = Button(F_buttons, image=img_players_report, font=self.font, bd=0,
                                            command=lambda: self.show_report_frame(self.F_report_players,
                                                                                   self.F_report_games, True))
        self.B_show_games_report = Button(F_buttons, image=img_games_report, font=self.font, bd=0,
                                          command=lambda: self.show_report_frame(self.F_report_games,
                                                                                 self.F_report_players,
                                                                                 False))
        B_player_info.image = img_player_info
        B_disconnect_player.image = img_player_disconnect
        B_disconnect_all.image = img_player_disconnect_all
        self.B_show_players_report.image = img_players_report
        self.B_show_games_report.image = img_games_report
        self.treeview = TreeviewTemp(F_buttons, 9, 'browse', ('id', 'name'), False)

        # place in grid
        self.treeview.frame.grid(row=0, column=0, rowspan=5, pady=self.pad_y, padx=self.pad_x)
        B_player_info.grid(row=0, column=1, sticky='ew')
        B_disconnect_player.grid(row=1, column=1, pady=self.pad_y, sticky='ew')
        B_disconnect_all.grid(row=2, column=1, sticky='ew')
        self.B_show_players_report.grid(row=3, column=1, pady=self.pad_y, sticky='ew')
        self.B_show_games_report.grid(row=4, column=1, sticky='ew')

        CreateToolTip(B_player_info, text="Get player info")
        CreateToolTip(B_disconnect_player, text="Disconnect selected player")
        CreateToolTip(B_disconnect_all, text="Disconnect all players")
        CreateToolTip(self.B_show_players_report, text="Show/Hide players report")
        CreateToolTip(self.B_show_games_report, text="Show/Hide games report")
        # add to widgets list
        self.add_widgets(B_disconnect_player, B_disconnect_all, B_player_info, self.B_show_players_report,
                         self.B_show_games_report)
        return F_buttons

    def change_reports_buttons(self):
        """
        change buttons images according to frames report states
        """
        if self.F_report_players.is_show:
            img_players_report_selected = PhotoImage(file='images/buttons/user_reports_selected.png')
            self.B_show_players_report.configure(image=img_players_report_selected)
            self.B_show_players_report.image = img_players_report_selected
        else:
            img_players_report = PhotoImage(file='images/buttons/user_report.png')
            self.B_show_players_report.configure(image=img_players_report)
            self.B_show_players_report.image = img_players_report

        if self.F_report_games.is_show:
            img_games_report_selected = PhotoImage(file='images/buttons/game_report_selected.png')
            self.B_show_games_report.configure(image=img_games_report_selected)
            self.B_show_games_report.image = img_games_report_selected
        else:
            img_games_report = PhotoImage(file='images/buttons/game_report.png')
            self.B_show_games_report.configure(image=img_games_report)
            self.B_show_games_report.image = img_games_report

    def edit_server_frame(self):
        """
        edit main server frame
        """
        # creating widgets
        F_addPlayer = self.create_add_player_frame(self.F_main_menu)
        L_title = Label(self.F_main_menu, text="R.P.S - Server", font=self.title_font)
        self.L_error_msg = Label(self.F_main_menu, text="", font=self.font)
        self.L_gif = GifLabel(self.F_main_menu)
        F_buttons = self.create_buttons_frame()
        # adding image
        self.L_gif.load('images/gif/Rock-Paper-Scissors-smaller.gif')
        # place in Frame
        self.F_main_menu.grid(row=0, column=0, padx=self.pad_x)
        L_title.grid(row=0, column=0, columnspan=2, pady=self.pad_y * 2)

        F_buttons.grid(row=1, column=1, columnspan=1, pady=self.pad_y, sticky='wn')
        F_addPlayer.grid(row=2, column=0, columnspan=2, pady=self.pad_y)
        self.L_error_msg.grid(row=3, column=0, columnspan=2)

        self.L_gif.grid(row=4, column=0, columnspan=2, pady=self.pad_y, padx=self.pad_x)
        # add to widgets list
        self.add_widgets(self.L_gif, L_title, self.L_error_msg, self.treeview, self.F_main_menu, F_buttons)

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
            click_sound_valid()
            self.L_error_msg.configure(text="")
            E_playerName.delete(0, 'end')
            self.add_new_player(name)
        else:
            click_sound_error()
            self.L_error_msg.configure(text="Error: Name can be only with letters, no spaces and in max length of 12")

    def exit_app(self):
        """
        closing all connections and closing the app
        """
        self.delete_all_players_from_listbox()
        while bool(self.dic_players_connected) is True:
            time.sleep(1)

        self.run_call = False
        self.event.set()
        super().exit_app()

    def sort_player_info_dict(self):
        """
        sort dictionary player info by number of winnings
        :return: sorted list
        """
        return sorted(self.dic_players_info.values(), key=operator.attrgetter('num_wins'), reverse=True)

    def init_report_frame(self, obj, title):
        """
        init and edit report frame
        :param obj: PlayerInfo or GameInfo
        :param title: str
        :return: FrameReport obj
        """
        columns = list(obj.tags.keys())
        tags = return_list_of_tuples(obj.tags)
        frame_report = FrameReport(self.F_main_menu, title, columns, tags, True)
        self.add_widgets(frame_report.list_widgets)
        return frame_report

    def show_report_frame(self, frame_show, frame_hide, is_player_report):
        """
        show or hide report frame
        :param frame_show: frame to show, if is already shown hide frame
        :param frame_hide: frame to hide if is shown
        :param is_player_report: true if frame_shoe is player_report, else false
        """
        if not frame_show.is_show:
            click_sound_valid()
            self.forget_frame(frame_hide)
            self.grid_report_frame(frame_show, is_player_report)
        else:
            click_sound_error()
            self.forget_frame(frame_show)
            self.L_gif.grid(row=4, column=0, columnspan=2, pady=self.pad_y, padx=self.pad_x)
            self.L_gif.is_show = True
        self.change_reports_buttons()

    def forget_frame(self, frame):
        """
         frame and L_gif if frame or L_gif is in window
        :param frame: frame to remove from window
        """
        if frame.is_show:
            frame.grid_forget()
            frame.is_show = False
        if self.L_gif.is_show:
            self.L_gif.grid_forget()
            self.L_gif.is_show = False

    def grid_report_frame(self, frame, is_player_report):
        """
        add frame report to the window.
        choose data according to if frame is players report
        :param frame: frame to add to the window
        :param is_player_report: true - player report, false - games report
        """
        frame.is_show = True
        self.update_report_frame(frame, is_player_report)
        frame.grid(row=4, column=0, columnspan=2, padx=self.pad_x, pady=self.pad_y)

    def update_report_frame(self, frame, is_player_report):
        """
        update report if is_show is true
        :param frame: player report or games report
        :param is_player_report: true - player report, false - games report
        """
        if frame.is_show:
            frame.clear_data()
            if is_player_report:
                list_obj = self.sort_player_info_dict()
            else:
                list_obj = self.get_list_of_game_info()
            frame.add_data(list_obj)

    def get_list_of_game_info(self):
        """
        returns list of all the game_info from players
        :return: list of game_info
        """
        list_gameinfo = []
        for player in self.dic_players_info.values():
            for game in player.List_games:
                list_gameinfo.append(game)
        return list_gameinfo

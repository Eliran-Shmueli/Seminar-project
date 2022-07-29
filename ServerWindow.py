# Music by Lesfm from Pixabay
import multiprocessing
from tkinter import messagebox

from event_scheduler import EventScheduler

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
        self.server = None
        self.listbox = ListBoxTemp(self.root, 6, 'browse')
        self.dic_players = {}
        self.player_id_count = 0
        # self.load_background_music(0, 'sounds/energetic-indie-rock-115484.wav', -1)
        self.edit_listbox()
        self.edit_server_window()
        self.T_server= threading.Thread(target=Server(self.Q_messages_send, self.Q_messages_received, self.dic_players,self.event).run)
        self.T_server.start()
        self.start_event_scheduler()
        self.p=None
        logging.info('Server window started')




    def add_new_player(self, name,is_client_init = False):
        self.player_id_count = self.player_id_count + 1
        player_new = Player(self.player_id_count, name)
        self.dic_players[self.player_id_count] = player_new
        self.listbox.insert('', END, values=(self.player_id_count, name))
        if is_client_init is False:
            self.create_player_process(player_new)
        logging.info('Player ' + "Id: " + str(self.player_id_count) + ", Name: " + name + ' was added')
        return self.player_id_count

    def mute_background_music(self):
        super().mute_background_music(0)

    def check_queue_received(self):
        if self.Q_messages_received.empty() is False:
            key, message = self.Q_messages_received.get()
            if message.is_message_exit():
                self.delete_player_by_id(message.id)

    def accept_request_to_connect_from_client(self,key,message):
        new_player_id = self.add_new_player(message.data,True)
        message_to_send = Message(new_player_id)
        message_to_send.set_message_connected()
        self.dic_players[new_player_id].socket = key
        self.Q_messages_send.put((key, message_to_send))

    def edit_listbox(self):
        self.listbox.heading('id', text='Player id', anchor=W, )
        self.listbox.heading('name', text='Player name', anchor=W)

    def delete_selected_player_from_listbox(self):
        self.click_sound_valid()
        selected_player = self.listbox.selection()
        if selected_player:
            player_info = self.listbox.item(selected_player[0]).get("values")
            player_id = player_info[0]
            player_name = player_info[1]
            self.listbox.delete(selected_player[0])
            self.disconnect_client(player_id)
            del self.dic_players[player_id]
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
            self.dic_players.clear()
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
        key = self.dic_players[player_id].socket
        self.Q_messages_send.put((key, message))

    def edit_server_window(self):
        # creating widgets
        F_addPlayer=self.create_add_player_frame()
        L_title = Label(self.root, text="R.P.S - Server", font=self.title_font)
        B_disconnectPlayer = Button(self.root, text='Disconnect a player', font=self.font,
                                    command=self.delete_selected_player_from_listbox)
        B_disconnectAll = Button(self.root, text='Disconnect all players', font=self.font,
                                 command=self.delete_all_players_from_listbox)
        # adding image
        img_server = PhotoImage(file=r"images/janken.png")
        img_server = img_server.subsample(2, 2)
        L_img = Label(self.root, image=img_server)
        L_img.image = img_server

        # place in grid
        L_title.pack(pady=self.pad_y * 2)
        self.listbox.frame.pack(pady=self.pad_y)
        F_addPlayer.pack(pady=self.pad_y)
        B_disconnectPlayer.pack(pady=self.pad_y)
        B_disconnectAll.pack(pady=self.pad_y)
        L_img.pack(pady=self.pad_y, padx=self.pad_x)

        # add to widgets list
        self.add_widgets(L_img, L_title, self.listbox, B_disconnectPlayer, B_disconnectAll)

    def exit_app(self):
        self.delete_all_players_from_listbox()
        self.p.terminate()

        self.event_scheduler.stop()
        self.event.set()
        super().exit_app()

    def create_player_process(self,player_new):
        self.p=multiprocessing.Process(target=GameWindow.GameWindow, args=(player_new.id, player_new.name,))
        self.p.start()

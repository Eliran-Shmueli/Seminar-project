# Music by Lesfm from Pixabay
import multiprocessing
from tkinter import messagebox
from WindowTemplate import WindowTemplate, ListBoxTemp
from GameWindow import GameWindow
from tkinter import *
from Player import Player
import logging
import threading
from Server import Server
from Message import Message


def start_game_window(player_new):
    x = GameWindow(player_new.id, player_new.name)
    x.root.mainloop()


def create_player_process(player_new):
    multiprocessing.Process(target=start_game_window, args=(player_new,)).start()


class ServerWindow(WindowTemplate):
    pad_y = 10
    pad_x = 10
    name_length = 12

    def __init__(self, window_name):
        super().__init__(window_name)
        self.server = None
        self.listbox = ListBoxTemp(self.root, 6, 'browse')
        self.dic_players = {}
        self.player_id = 0
        self.load_background_music(0,'sounds/best-time-112194.wav', -1)
        self.edit_listbox()
        self.edit_server_window()
        threading.Thread(target=Server(self.Q_messages_send, self.Q_messages_received, self.dic_players).run).start()
        self.bind_widgets()
        logging.info('Server window started')

    def mute_background_music(self):
        super().mute_background_music(0)

    def check_queue_received(self, event):
        if self.Q_messages_received.empty() is False:
            message = self.Q_messages_received.get()
            if message.is_message_exit():
                self.delete_player_by_id(message.id)

    def edit_listbox(self):
        self.listbox.heading('id', text='Player id', anchor=W, )
        self.listbox.heading('name', text='Player name', anchor=W)

    def create_add_player_frame(self):
        F_addPlayer = Frame(self.root)
        L_addPlayer = Label(F_addPlayer, text="Player name:", font=self.font, padx=self.pad_x)
        E_playerName = Entry(F_addPlayer, font=self.font)
        B_addPlayer = Button(F_addPlayer, text='add player', font=self.font,
                             command=lambda: self.set_player_name(E_playerName))

        # place in F_addPlayer
        L_addPlayer.pack(side=LEFT)
        E_playerName.pack(side=LEFT)
        B_addPlayer.pack(side=LEFT, padx=self.pad_x)

        # add to widgets list
        self.add_widgets(B_addPlayer, L_addPlayer, E_playerName, F_addPlayer)

        return F_addPlayer

    def set_player_name(self, E_playerName):
        name = E_playerName.get()
        if (len(name) != 0) and (name.isalpha() and (len(name) <= self.name_length)):
            self.click_sound_valid()
            self.player_id = self.player_id + 1
            player_new = Player(self.player_id, name)
            self.dic_players[self.player_id] = player_new
            create_player_process(player_new)
            self.listbox.insert('', END, values=(self.player_id, name))
            logging.info('Player ' + "Id: " + str(self.player_id) + ", Name: " + name + ' was added')
            E_playerName.delete(0, 'end')
        else:
            self.click_sound_error()
            messagebox.showerror('R.P.S - Server',
                                 'Error: Name can be only with letters, no spaces and in max length of 12')

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
        F_addPlayer = self.create_add_player_frame()
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
        super().exit_app()

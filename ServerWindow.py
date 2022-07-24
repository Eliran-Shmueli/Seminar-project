from WindowTemplate import WindowTemplate, ListBoxTemp
from GameWindow import GameWindow
from tkinter import *
from Player import Player
import logging
import threading


def start_game_window(player_new):
    x = GameWindow(player_new.id, player_new.name)
    try:
        x.root.mainloop()
    except:
        pass


def create_player_thread(player_new):
    threading.Thread(target=start_game_window, args=(player_new,)).start()


class ServerWindow(WindowTemplate):
    pad_y = 10
    pad_x = 10

    def __init__(self, window_name):
        super().__init__(window_name, Tk())
        self.listbox = ListBoxTemp(self.root, 6, 45, 'SINGLE')
        self.dic_players = {}
        self.player_id = 0
        # self.load_background_music('sounds/Tenacious D - Master Exploder.wav', -1)
        self.edit_server_window()
        logging.info('Server window started')

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
        if (len(name) != 0) and (name.isalpha()):
            self.click_sound_valid()
            self.player_id = self.player_id + 1
            player_new = Player(self.player_id, name)
            self.dic_players[self.player_id] = player_new.name
            create_player_thread(player_new)
            self.listbox.insert(END, "Id: " + str(self.player_id) + ", Name: " + name)
            logging.info('Player ' + "Id: " + str(self.player_id) + ", Name: " + name + ' was added')
            E_playerName.delete(0, 'end')
        else:
            self.click_sound_error()

    def delete_player(self, selected_player):
        player_info = self.listbox.get(selected_player)
        self.listbox.delete(selected_player)
        logging.info('Player ' + player_info + ' was disconnected')

    def delete_selected_player_from_listbox(self):
        self.click_sound_valid()
        selected_player = self.listbox.curselection()
        print(selected_player)
        if selected_player:
            self.delete_player(selected_player)
        else:
            self.click_sound_error()

    def delete_all_players_from_listbox(self):
        self.click_sound_valid()
        selected_player = self.listbox.curselection()
        if self.listbox.size() != 0:
            for player in self.listbox.get(0, END):
                self.delete_player((0,))

        else:
            self.click_sound_error()

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

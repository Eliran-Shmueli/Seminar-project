from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from pandas import DataFrame


class FrameInfo(Frame):
    pad_y = 10
    pad_y_label = 5
    pad_x = 10
    title_font = 'Helvetica 20 underline bold'
    font = 'Helvetica 12'

    def __init__(self, root, previous_frame):
        super().__init__(master=root)
        self.root = root
        self.B_to_main_menu = None
        self.list_widgets = []
        self.F_main_menu = previous_frame
        self.L_player_results = None
        self.L_player_picks = None
        self.L_num_rounds = None
        self.L_num_games = None
        self.L_player_name = None
        self.L_player_id = None
        self.L_title = None
        self.create_player_info_frame()

    def create_player_info_frame(self):
        self.L_title = Label(self, text="Player info", font=self.title_font)
        self.L_player_id = Label(self, text="Player id: ", font=self.font)
        self.L_player_name = Label(self, text="Player_name", font=self.font)
        self.L_num_games = Label(self, text="Number of games: ", font=self.font)
        self.L_num_rounds = Label(self, text="Number of rounds:", font=self.font)
        self.L_player_picks = Label(self, text="player picks: ", font=self.font)
        self.L_player_results = Label(self, text="player results", font=self.font)
        img_back = PhotoImage(file='images/buttons/back-button.png')
        self.B_to_main_menu = Button(self, image=img_back, command=self.show_main_menu)
        self.B_to_main_menu.image = img_back

        self.L_title.grid(row=0, column=0, columnspan=4, pady=self.pad_y * 2)
        self.L_player_id.grid(row=1, column=0, columnspan=2, pady=self.pad_y_label, padx=self.pad_x, sticky='w')
        self.L_player_name.grid(row=2, column=0, columnspan=2, pady=self.pad_y_label, padx=self.pad_x, sticky='w')
        self.L_num_games.grid(row=3, column=0, columnspan=2, pady=self.pad_y_label, padx=self.pad_x, sticky='w')
        self.L_num_rounds.grid(row=4, column=0, columnspan=2, pady=self.pad_y_label, padx=self.pad_x, sticky='w')
        self.B_to_main_menu.grid(row=6, column=0, columnspan=2, pady=self.pad_y)

        self.list_widgets = [self.L_title, self.L_player_id, self.L_player_name, self.L_num_games, self.L_num_rounds,
                             self.B_to_main_menu]

    def edit(self, game_info):
        self.L_player_id.configure(text="Player id: " + str(game_info.get_player_id()))
        self.L_player_name.configure(text="Player_name: " + game_info.get_player_name())
        self.L_num_games.configure(text="Number of games: " + str(game_info.num_games))
        self.L_num_rounds.configure(text="Number of rounds: " + str(game_info.num_rounds))
        self.plot(game_info)

    def plot(self,game_info):
        data1 = {'Selections': ['Rock', 'Paper', 'Scissors'],
                 'Number': [game_info.num_rock, game_info.num_paper, game_info.num_scissors]
                 }
        df1 = DataFrame(data1, columns=['Selections', 'Number'])
        figure1 = Figure(figsize=(4, 4), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, self)
        bar1.get_tk_widget().grid(row=5, column=0, columnspan=2,pady=self.pad_y,padx=self.pad_x)
        df1 = df1[['Selections', 'Number']].groupby('Selections').sum()
        df1.plot(kind='bar', legend=True, ax=ax1)
        ax1.set_title("The player's selection history")

    def show_main_menu(self):
        self.pack_forget()
        self.F_main_menu.pack()

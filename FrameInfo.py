from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


class FrameInfo(Frame):
    pad_y = 10
    pad_y_label = 2
    pad_x = 10
    title_font = 'Helvetica 20 underline bold'
    font = 'Helvetica 12'

    def __init__(self, root, previous_frame):
        """
        init FrameInfo
        :param root: window main root
        :param previous_frame: frame to go back to on a button click
        """
        super().__init__(master=root)
        self.root = root
        self.B_to_main_menu = None
        self.list_widgets = []
        self.F_main_menu = previous_frame
        self.L_player_results = None
        self.L_player_picks = None
        self.L_num_games = None
        self.L_player_name = None
        self.L_player_id = None
        self.L_title = None
        self.create_player_info_frame()

    def create_player_info_frame(self):
        """
        creates and edits player info frame
        """
        self.L_title = Label(self, text="Player's info", font=self.title_font)
        self.L_player_id = Label(self, text="Player's id: ", font=self.font)
        self.L_player_name = Label(self, text="Player's name", font=self.font)
        self.L_num_games = Label(self, text="Number of games: ", font=self.font)
        img_back = PhotoImage(file='images/buttons/back-button.png')
        self.B_to_main_menu = Button(self, image=img_back, command=self.show_main_menu, bd=0)
        self.B_to_main_menu.image = img_back
        # place on grid
        self.L_title.grid(row=0, column=0, columnspan=4, pady=self.pad_y * 2)
        self.L_player_id.grid(row=1, column=0, columnspan=2, pady=self.pad_y_label, padx=self.pad_x, sticky='w')
        self.L_player_name.grid(row=2, column=0, columnspan=2, pady=self.pad_y_label, padx=self.pad_x, sticky='w')
        self.L_num_games.grid(row=3, column=0, columnspan=2, pady=self.pad_y_label, padx=self.pad_x, sticky='w')
        self.B_to_main_menu.grid(row=5, column=0, columnspan=4, pady=self.pad_y)
        # add to dict
        self.list_widgets = [self.L_title, self.L_player_id, self.L_player_name, self.L_num_games,
                             self.B_to_main_menu, self]

    def edit(self, player_info):
        """
        changes labels according to the game info
        :param player_info: game information
        """
        self.L_player_id.configure(text="Player's id: " + str(player_info.get_id()))
        self.L_player_name.configure(text="Player's name: " + player_info.get_name())
        self.L_num_games.configure(text="Number of games: " + str(player_info.num_games))
        self.plot(player_info)

    def plot(self, game_info):
        """
        creates statistics
        :param game_info: game information
        """
        # prepare data
        data_selected = {
            'Rock': game_info.num_rock,
            'Paper': game_info.num_paper,
            'Scissors': game_info.num_scissors
        }

        data_game_results = {
            'Wins': game_info.num_wins,
            'Tie': game_info.num_ties,
            'Losses': game_info.num_losses
        }

        selections = data_selected.keys()
        selections_counter = data_selected.values()

        results = data_game_results.keys()
        results_counter = data_game_results.values()

        # create a figures
        figure_selections = Figure(figsize=(6, 4), dpi=100)
        figure_results = Figure(figsize=(6, 4), dpi=100)

        # create FigureCanvasTkAgg objects
        canvas_selection = FigureCanvasTkAgg(figure_selections, self)
        canvas_results = FigureCanvasTkAgg(figure_results, self)

        # create axes
        axes_selections = figure_selections.add_subplot()
        axes_results = figure_results.add_subplot()

        # create the barchart
        axes_selections.bar(selections, selections_counter)
        axes_selections.set_title("The player's selection history")
        axes_selections.set_ylabel('Number of time selected')

        axes_results.bar(results, results_counter)
        axes_results.set_title("The player's round results history")
        axes_results.set_ylabel('Counter')

        canvas_selection.get_tk_widget().grid(row=4, column=0, columnspan=2, pady=self.pad_y, padx=self.pad_x)
        canvas_results.get_tk_widget().grid(row=4, column=2, columnspan=2, pady=self.pad_y, padx=self.pad_x)

    def show_main_menu(self):
        """
        hide frame info and shows main menu
        """
        self.grid_forget()
        self.F_main_menu.grid(row=0, column=0)

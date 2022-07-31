from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)


class FrameInfo(Frame):
    pad_y = 5
    pad_x = 10
    title_font = 'Helvetica 20 underline bold'
    font = 'Helvetica 12'

    def __init__(self, root, previous_frame):
        super().__init__(master=root)
        self.root=root
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
        self.B_to_main_menu = Button(self, image=img_back)
        self.B_to_main_menu.image = img_back
        self.plot()

        self.L_title.grid(row=0, column=0, columnspan=4, pady=self.pad_y)
        self.L_player_id.grid(row=1, column=0, columnspan=1, pady=self.pad_y)
        self.L_player_name.grid(row=2, column=0, columnspan=1, pady=self.pad_y)
        self.L_num_games.grid(row=3, column=0, columnspan=1, pady=self.pad_y)
        self.L_num_rounds.grid(row=4, column=0, columnspan=1, pady=self.pad_y)

        self.list_widgets=[self.L_title, self.L_player_id, self.L_player_name, self.L_num_games, self.L_num_rounds, self.B_to_main_menu]

    def plot(self):
        # the figure that will contain the plot
        fig = Figure(figsize=(4,4),
                     dpi=100)

        # list of squares
        y = [i ** 2 for i in range(101)]

        # adding the subplot
        plot1 = fig.add_subplot(111)

        # plotting the graph
        plot1.plot(y)

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().grid(row=5,columnspan=2)

        # creating the Matplotlib toolbar
      #  toolbar = NavigationToolbar2Tk(canvas,self.root)
        #toolbar.update()

        # placing the toolbar on the Tkinter window
        #canvas.get_tk_widget().grid(row=6,columnspan=2)

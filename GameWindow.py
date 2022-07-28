from Client import Client
from WindowTemplate import WindowTemplate
from tkinter import *
from PIL import ImageTk, Image
from Player import Player
import logging
from Message import Message
import threading


class GameWindow(WindowTemplate):
    font_score = 'Helvetica 14 bold'
    num_music_loops = 0

    def __init__(self, player_id, player_name):
        super().__init__('Client-- Id - ' + str(player_id) + ', Name - ' + player_name, Tk())
        self.L_pc_pick = None
        logging.info('Game window started')
        self.image_type = "animated_"
        self.player_info = Player(player_id, player_name)
        self.message = Message(self.player_info.id)
        self.round_count = 1
        self.player_score = 0
        self.pc_score = 0
        self.player_choice = None
        self.pc_choice = None
        self.images = {}
        self.load_all_images()
        self.L_final_result_img = None
        self.L_round_result_pc_choice_img = None
        self.L_round_result_player_choice_img = None
        self.L_round_result_title = None
        self.L_title = None
        self.L_pc_score = None
        self.L_player_score = None
        self.L_final_result_pc_score = None
        self.L_final_result_player_score = None
        self.L_player_pick = None
        self.B_rock = None
        self.B_paper = None
        self.B_scissors = None
        self.B_bottom = self.init_bottom_button()
        self.message.set_message_connected()
        threading.Thread(target=lambda: Client(self.player_info, self.message, self.Q_messages_send,
                                               self.Q_messages_received)).start()
        self.F_round_result = self.create_round_result_frame()
        self.F_final_result = self.create_final_result_frame()
        self.F_main_menu = self.create_main_menu()
        self.F_game = self.create_game_frame()
        self.add_action_to_menubar()
        self.bind_widgets()

    def check_queue_received(self, event):
        if self.Q_messages_received.empty() is False:
            message = self.Q_messages_received.get()
            if message.is_message_exit():
                message.set_message_goodbye()
                self.send_info(message)
                super().exit_app()
            else:
                self.Q_messages_received.put(message)

    def send_info(self, message, data=None):
        message.set_message_data(data)
        self.Q_messages_send.put(message)

    def mute_background_music(self, channel=1):
        super().mute_background_music(channel)

    def check_if_everybody_choose(self):
        if len(self.player_choice) != 0 and len(self.pc_choice) != 0:
            self.config_bottom_button(state="normal")

    def actions(self):
        message_received = self.Q_messages_received.get(block=True)
        if message_received.is_message_ready():
            self.config_bottom_button("start", 'normal', lambda: self.start_game())
        if message_received.is_message_data():
            self.pc_choice = message_received.data
            self.L_pc_pick.configure(text="pc chose")
            self.check_if_everybody_choose()
        if message_received.is_message_goodbye():
            self.message.set_message_goodbye()
            self.send_info(self.message)
            super().exit_app()

    def show_frame_in_grid(self, frame):
        """
        add selected frame to the top grid
        :param frame: selected frame
        """
        frame.grid(row=0, column=0, pady=self.pad_y)

    def init_bottom_button(self):
        """
        init and config the button at the bottom of the grid
        :return: button
        """
        self.root.configure(pady=self.pad_y)
        B_bottom = Button(self.root, font=self.font_score, width=10, height=2, state="disabled")
        B_bottom.grid(row=1, column=0)
        self.add_widgets(B_bottom)
        return B_bottom

    def config_bottom_button(self, text='', state='', func=None):
        """
        config the button at the bottom of the window
        :param text: the text in the button
        :param state: normal or disable
        :param func: function that will run when the user clicked the button
        """
        if len(text) != 0:
            self.B_bottom.configure(text=text)
        if len(state) != 0:
            self.B_bottom.configure(state=state)
        if func is not None:
            self.B_bottom.configure(command=func)

    def create_main_menu(self):
        """
        creates the main menu frame
        :return: main menu frame
        """
        # create widgets
        F_main_menu = Frame(self.root)
        self.actions()
        # adding image
        img_main_menu = PhotoImage(file=r"images/event-featured-the-legend-of-rock-paper-scissors-1634241914.png")
        img_main_menu = img_main_menu.subsample(2, 2)
        L_img = Label(F_main_menu, image=img_main_menu)
        L_img.image = img_main_menu

        # add to root
        L_img.pack(padx=self.pad_x)

        self.show_frame_in_grid(F_main_menu)

        # add to dict
        self.add_widgets(F_main_menu, L_img)
        return F_main_menu

    def create_scores_frame(self, F_game):
        """
        creates a scores frame to the game frame
        :param F_game:
        :return: scores frame
        """
        # create widgets
        F_scores = Frame(F_game)

        self.L_player_score = Label(F_scores, text=self.player_info.name + ": " + str(self.player_score),
                                    font=self.font_score)
        self.L_pc_score = Label(F_scores, text="Pc: " + str(self.pc_score), font=self.font_score)
        # put in order
        self.L_player_score.pack(side=LEFT, padx=self.pad_x)
        self.L_pc_score.pack(side=LEFT, padx=self.pad_x)

        self.add_widgets(self.L_player_score, self.L_pc_score)
        return F_scores

    def create_choices_frame(self, F_game):
        """
        creates frame with rock, paper, scissors buttons
        :param F_game:
        :return: choices frame
        """
        # create widgets
        F_choices = Frame(F_game)
        self.B_rock = Button(F_choices, image=self.images.get("animated_rock"),
                             command=lambda: self.player_pick("rock"))
        self.B_paper = Button(F_choices, image=self.images.get("animated_paper"),
                              command=lambda: self.player_pick("paper"))
        self.B_scissors = Button(F_choices, image=self.images.get("animated_scissors"),
                                 command=lambda: self.player_pick("scissors"))
        # put in order
        self.B_rock.pack(side=LEFT, pady=self.pad_y, padx=self.pad_x)
        self.B_paper.pack(side=LEFT, pady=self.pad_y, padx=self.pad_x)
        self.B_scissors.pack(side=LEFT, pady=self.pad_y, padx=self.pad_x)

        self.add_widgets(self.B_rock, self.B_paper, self.B_scissors)
        return F_choices

    def create_game_frame(self):
        """
        creates the game frame with choices frame and scores frame
        :return: game frame
        """
        # create frames
        F_game = Frame(self.root)
        F_choices = self.create_choices_frame(F_game)
        F_scores = self.create_scores_frame(F_game)
        # create widgets
        self.L_title = Label(F_game, text="Round: " + str(self.round_count), font=self.title_font)
        self.L_player_pick = Label(F_game, text="Choose your destiny", font=self.font)
        self.L_pc_pick = Label(F_game, text="Waiting for pc to choose", font=self.font)

        self.L_title.pack()
        F_scores.pack(pady=self.pad_y)
        F_choices.pack()
        self.L_player_pick.pack(pady=self.pad_y)
        self.L_pc_pick.pack(pady=self.pad_y)

        self.add_widgets(F_game, F_choices, F_scores, self.L_title, self.L_player_pick, self.L_pc_pick)
        return F_game

    def create_final_result_frame(self):
        """
        creates a frame that show the result of the game
        :return: frame
        """
        F_final_result = Frame(self.root)
        self.L_final_result_img = Label(F_final_result)
        self.L_final_result_player_score = Label(F_final_result, font=self.title_font)
        self.L_final_result_pc_score = Label(F_final_result, font=self.title_font)

        self.L_final_result_player_score.grid(row=0, column=0)
        self.L_final_result_pc_score.grid(row=0, column=1)
        self.L_final_result_img.grid(row=1, columnspan=2, pady=self.pad_y, padx=self.pad_x)

        self.add_widgets(F_final_result, self.L_final_result_img, self.L_final_result_player_score,
                         self.L_final_result_pc_score)
        return F_final_result

    def create_round_result_frame(self):
        """
        creates a frame that show the result of a round
        :return: frame
        """
        F_round_result = Frame(self.root)
        self.L_round_result_title = Label(F_round_result, font=self.title_font)
        L_round_result_player = Label(F_round_result, text=self.player_info.name + ':', font=self.font_score)
        L_round_result_pc = Label(F_round_result, text='Pc:', font=self.font_score)
        self.L_round_result_player_choice_img = Label(F_round_result)
        self.L_round_result_pc_choice_img = Label(F_round_result)

        self.L_round_result_title.grid(row=0, column=0, columnspan=3)
        L_round_result_player.grid(row=1, column=0, pady=self.pad_y, padx=self.pad_x)
        L_round_result_pc.grid(row=1, column=2, pady=self.pad_y, padx=self.pad_x)
        self.L_round_result_player_choice_img.grid(row=2, column=0, padx=self.pad_x)
        self.L_round_result_pc_choice_img.grid(row=2, column=2, padx=self.pad_x)

        self.add_widgets(F_round_result, self.L_round_result_title, L_round_result_player, L_round_result_pc,
                         self.L_round_result_player_choice_img, self.L_round_result_pc_choice_img)
        return F_round_result

    def start_game(self):
        """
        starting the game
        """
        self.config_bottom_button('Go!!!', 'disabled', lambda: self.play_game())
        self.reset_choices()
        self.message.set_message_choose()
        self.send_info(self.message)
        self.actions()
        self.click_sound_valid()
        self.load_background_music(1, 'sounds/start.wav', self.num_music_loops)
        logging.info('Player started a new game')
        self.player_info.increase_num_games()
        self.F_main_menu.grid_forget()
        self.show_frame_in_grid(self.F_game)

    def play_game(self):
        self.click_sound_valid()
        self.config_bottom_button('Next round', 'normal', lambda: self.next_stage())
        logging.info('Round ' + str(self.round_count))
        self.round_count = self.round_count + 1
        result = self.get_round_result()
        self.update_title_and_scores(result)
        self.F_game.grid_forget()
        self.show_frame_in_grid(self.F_round_result)

        logging.info(
            'Player chose - ' + self.player_choice)
        logging.info(
            'Result - ' + result + ', Player score - ' + str(self.player_score) + ', Pc score - ' + str(self.pc_score))

    def next_stage(self):
        """
        showing the next stage in the game
        if the game is over or someone score a 2 - go to the final result frame
        else go to the next round
        """
        self.click_sound_valid()
        if (self.round_count > 3) or (self.player_score == 2) or (self.pc_score == 2):
            self.config_bottom_button("Play again?", 'normal', lambda: self.reset_game())
            self.update_final_round_frame()
            self.F_round_result.grid_forget()
            self.show_frame_in_grid(self.F_final_result)
        else:
            self.reset_choices()
            self.config_bottom_button("Go!!!", 'disabled', lambda: self.play_game())
            self.message.set_message_choose()
            self.send_info(self.message)
            self.actions()
            self.update_scores_and_round_labels()
            self.F_round_result.grid_forget()
            self.show_frame_in_grid(self.F_game)

    def reset_choices(self):
        self.pc_choice = ""
        self.player_choice = ""

    def reset_game(self):
        """
        reset all variables and show the main menu
        """
        logging.info('Game over, player got back to the main menu')
        self.load_background_music(1, 'sounds/play_again.wav', self.num_music_loops)
        self.config_bottom_button('Start', 'normal', lambda: self.start_game())
        self.F_final_result.grid_forget()
        self.show_frame_in_grid(self.F_main_menu)
        self.round_count = 1
        self.player_score = 0
        self.pc_score = 0
        self.update_scores_and_round_labels()
        self.reset_choices()

    def update_scores_and_round_labels(self):
        """
        updates the labels of round and scores
        """
        self.L_player_score.configure(text=self.player_info.name + ": " + str(self.player_score))
        self.L_pc_score.configure(text="Pc: " + str(self.pc_score))
        self.L_title.configure(text="Round: " + str(self.round_count))

    def player_pick(self, pick):
        """
        saves the player pick the player choice and config bottom button to normal
        :param pick: what the button represents
        """
        self.click_sound_valid()
        self.player_choice = pick
        self.check_if_everybody_choose()
        self.L_player_pick.configure(text="You chose: " + pick)
        self.check_if_everybody_choose()

    def update_final_round_frame(self):
        """
        updates the titles and image at the final result frame, according to the scores
        """
        self.L_final_result_player_score.configure(text=self.player_info.name + ": " + str(self.player_score))
        self.L_final_result_pc_score.configure(text="Pc: " + str(self.pc_score))
        if self.player_score == self.pc_score:
            logging.info('The game ended in a tie')
            self.load_background_music(1, 'sounds/tie.wav', self.num_music_loops)
            self.L_final_result_img.configure(image=self.images.get("tie"))
        elif self.player_score > self.pc_score:
            logging.info('The player won the game')
            self.load_background_music(1, 'sounds/mixkit-video-game-win-2016.wav', self.num_music_loops)
            self.L_final_result_img.configure(image=self.images.get("win"))
        else:
            logging.info('The player lost the game')
            self.load_background_music(1, 'sounds/mixkit-horror-lose-2028.wav', self.num_music_loops)
            self.L_final_result_img.configure(image=self.images.get("lose"))

    def update_title_and_scores(self, result):
        """
        updates the title and scores at the round result frame
        """
        self.update_images_choices()
        if result == "tie":
            self.load_background_music(1, 'sounds/tie.wav', self.num_music_loops)
            self.L_round_result_title.configure(text="It's a tie")
            self.player_info.increase_num_ties()
        elif result == "win":
            self.load_background_music(1, 'sounds/mixkit-video-game-win-2016.wav', self.num_music_loops)
            self.L_round_result_title.configure(text="You won")
            self.player_score = self.player_score + 1
            self.player_info.increase_num_wins()
        elif result == "lose":
            self.load_background_music(1, 'sounds/mixkit-horror-lose-2028.wav', self.num_music_loops)
            self.L_round_result_title.configure(text="You lost")
            self.pc_score = self.pc_score + 1
            self.player_info.increase_num_losses()

    def get_round_result(self):
        """

        :return: the result of a round
        """
        if self.player_choice == self.pc_choice:
            return "tie"

        if self.player_choice == "rock":
            self.player_info.increase_num_rock()
            return self.result("scissors")

        elif self.player_choice == "paper":
            self.player_info.increase_num_paper()
            return self.result("rock")

        else:
            self.player_info.increase_num_scissors()
            return self.result("paper")

    def result(self, weak_pick):
        """
        check if pc choice is "weaker" than player choice
        :param weak_pick:
        :return: result
        """
        if self.pc_choice == weak_pick:
            return "win"
        else:
            return "lose"

    def load_all_images(self):
        """
        load all the images and adds them to the dict
        """
        # hands
        self.load_image('images/hands/rock.jpg', 180, "hands_rock")
        self.load_image('images/hands/paper.jpg', 180, "hands_paper")
        self.load_image('images/hands/sci.jpg', 180, "hands_scissors")
        # animated
        self.load_image('images/animated/animated_rock.png', 180, "animated_rock")
        self.load_image('images/animated/animated_paper.png', 180, "animated_paper")
        self.load_image('images/animated/animated_scissors.png', 180, "animated_scissors")
        # neon
        self.load_image('images/neon/neon-rock.png', 180, "neon_rock")
        self.load_image('images/neon/neon-paper.png', 180, "neon_paper")
        self.load_image('images/neon/neon-scissors.png', 180, "neon_scissors")
        # real
        self.load_image('images/real/rock.png', 180, "real_rock")
        self.load_image('images/real/paper.png', 180, "real_paper")
        self.load_image('images/real/scissors.png', 180, "real_scissors")
        # game result
        self.load_image('images/winner.jpg', 500, "win")
        self.load_image('images/you_lose.png', 500, "lose")
        self.load_image('images/tie.gif', 500, "tie")

    def load_image(self, path, size, name):
        """
        loads an image,config size and adds the dict
        :param path: image path
        :param size: size of image in the window
        :param name: key for the dict
        """
        image = Image.open(path)
        image = image.resize((size, size), Image.Resampling.LANCZOS)
        Photo = ImageTk.PhotoImage(image)
        self.images[name] = Photo

    def add_action_to_menubar(self):
        """
        adds the images selection option for the menubar
        """
        file_menu = Menu(self.menubar, tearoff=0)

        file_menu.add_command(
            label='Animated',
            command=lambda: self.change_images("animated_"))

        file_menu.add_command(
            label='Hands',
            command=lambda: self.change_images("hands_"))

        file_menu.add_command(
            label='Neon',
            command=lambda: self.change_images("neon_"))

        file_menu.add_command(
            label='Real',
            command=lambda: self.change_images("real_"))

        self.menubar.add_cascade(
            label="Images options",
            menu=file_menu
        )

    def change_images(self, name):
        """
        changes the images of the choices buttons
        :param name: name of the "type" of image
        """
        self.image_type = name
        logging.info('Images were change to ' + self.image_type)
        self.B_rock.configure(image=self.images.get(name + "rock"))
        self.B_paper.configure(image=self.images.get(name + "paper"))
        self.B_scissors.configure(image=self.images.get(name + "scissors"))
        if self.player_choice is not None:
            self.update_images_choices()

    def update_images_choices(self):
        """
        updates the images at the result round according to the player and pc choices
        """
        self.L_round_result_pc_choice_img.configure(image=self.images.get(self.image_type + self.pc_choice))
        self.L_round_result_player_choice_img.configure(image=self.images.get(self.image_type + self.player_choice))

    def exit_app(self):
        self.message.set_message_exit()
        self.send_info(self.message)  # exit
        self.actions()

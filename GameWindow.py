from GameInfo import GameInfo
from Client_server import Client
from GifLabel import GifLabel
from PlayerInfo import PlayerInfo
from WindowTemplate import WindowTemplate
from tkinter import *
from PIL import ImageTk, Image
import logging
from Message import Message
import threading


class GameWindow(WindowTemplate):
    font_score = 'Helvetica 14 bold'
    num_music_loops = 0

    def __init__(self, player_id, player_name):
        """
        init game window
        :param player_id: player's id
        :param player_name: player's name
        """
        super().__init__('Client-- Id - ' + str(player_id) + ', Name - ' + player_name, False)
        self.game_info = GameInfo(player_id, player_name)
        self.player_info = PlayerInfo(player_id, player_name)
        self.image_type = "animated_"
        self.round_count = 1
        self.player_score = 0
        self.pc_score = 0
        self.images = {}
        self.message = None
        self.player_choice = None
        self.pc_choice = None
        self.F_game = None
        self.F_main_menu = None
        self.F_final_result = None
        self.F_round_result = None
        self.L_pc_pick = None
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
        self.B_replay = None
        self.B_next = None
        self.call_after_func()
        self.message = Message(self.game_info.get_player_id())
        self.init_server()

    def init_server(self):
        """
        init game's frames and client server
        """
        self.init_frames()
        self.message.set_message_join_request()
        self.init_client_server()
        self.send_to_server(self.message)
        self.run()

    def run(self):
        """
        start the game window
        """
        self.root.mainloop()
        logging.info('Game window started')

    def init_frames(self):
        """
        init,creates frames
        adds menubar and button to root
        """
        self.load_all_images()
        self.F_main_menu = self.create_main_menu()
        self.create_game_frame()
        self.F_final_result = self.create_final_result_frame()

        self.add_action_to_menubar()

    def init_client_server(self):
        """
        init message and thread, set message to "connected"
        """
        T_server_client = threading.Thread(target=lambda: Client(self.game_info.get_player_id(), self.Q_messages_send,
                                                                 self.Q_messages_received, self.event))
        T_server_client.start()

    def check_queue_received(self):
        """
        checks if there are messages in the queue
        """
        if self.Q_messages_received.empty() is False:
            message = self.Q_messages_received.get()
            self.actions(message)
        self.call_after_func()

    def send_to_server(self, message, data=None):
        """
        send message to the server
        :param message: a message to send
        :param data: a data to add to the message
        """
        message.add_data_to_message(data)
        self.Q_messages_send.put(message)

    def send_info(self):
        """
        sends updated info to server
        data - (playerInfo, gameInfo)
        """
        data = (self.player_info, self.game_info)
        self.message.set_message_game_info_request()
        self.send_to_server(self.message, data)

    def mute_background_music(self, channel=1):
        """
        mute main background music
        :param channel: channel number
        """
        super().mute_background_music(channel)

    def check_if_everybody_choose(self):
        """
        checks if player and pc selected and play the game
        """
        if len(self.player_choice) != 0 and len(self.pc_choice) != 0:
            self.play_game()

    def actions(self, message_received):
        """
        actions to do according to the message content
        :param message_received: message from the server
        """
        if message_received.is_message_exit():
            self.message.set_message_goodbye()
            self.send_to_server(self.message)
            self.run_call = False
            self.event.set()
            super().exit_app()
        if message_received.is_message_game_info_request():
            game_info = self.player_info.create_copy()
            self.message.set_message_game_info_request()
            self.send_to_server(self.message, game_info)
        if message_received.is_message_accepted():
            self.start_game()
        if message_received.is_message_choose():
            self.pc_choice = message_received.data
            self.L_pc_pick.configure(text="Pc already selected")
            self.check_if_everybody_choose()

    def show_frame_in_grid(self, frame):
        """
        add selected frame to the top grid
        :param frame: selected frame
        """
        frame.grid(row=0, column=0, pady=self.pad_y)

    def create_main_menu(self):
        """
        creates the main menu frame
        :return: main menu frame
        """

        # create widgets
        F_main_menu = Frame(self.root)
        # adding images
        L_img = GifLabel(F_main_menu)
        L_img.load("images/gif/connecting.gif")
        # add to root
        L_img.pack(pady=self.pad_y, padx=self.pad_x)
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
        self.L_player_score = Label(F_scores, text=self.game_info.get_player_name() + ": " + str(self.player_score),
                                    font=self.font_score)
        self.L_pc_score = Label(F_scores, text="Pc: " + str(self.pc_score), font=self.font_score)
        # put in order
        self.L_player_score.pack(side=LEFT, padx=self.pad_x)
        self.L_pc_score.pack(side=LEFT, padx=self.pad_x)
        # add to dict
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
        # add to dict
        self.add_widgets(self.B_rock, self.B_paper, self.B_scissors)
        return F_choices

    def create_game_frame(self):
        """
        creates the game frame with choices frame and scores frame
        :return: game frame
        """
        # create frames
        self.F_game = Frame(self.root)
        F_choices = self.create_choices_frame(self.F_game)
        F_scores = self.create_scores_frame(self.F_game)
        self.F_round_result = self.create_round_result_frame()
        # create widgets
        self.L_title = Label(self.F_game, text="Round: " + str(self.round_count), font=self.title_font)
        # add to grid
        self.L_title.grid(row=0, column=0)
        F_scores.grid(row=1, column=0, pady=self.pad_y)
        F_choices.grid(row=2, column=0)
        self.F_round_result.grid(row=5, column=0)
        # add to dict
        self.add_widgets(self.F_game, F_choices, F_scores, self.L_title)

    def create_round_result_frame(self):
        """
        creates a frame that show the result of a round
        :return: frame
        """
        F_round_result = Frame(self.F_game)
        self.L_round_result_title = Label(F_round_result, font=self.title_font)
        L_round_result_player = Label(F_round_result, text=self.game_info.get_player_name() + ':', font=self.font_score)
        L_round_result_pc = Label(F_round_result, text='Pc:', font=self.font_score)
        self.L_round_result_player_choice_img = GifLabel(F_round_result)
        self.L_round_result_pc_choice_img = GifLabel(F_round_result)
        self.L_player_pick = Label(F_round_result, text="Waiting for you to select", font=self.font)
        self.L_pc_pick = Label(F_round_result, text="Waiting for Pc to select", font=self.font)
        # load image
        img_forward = PhotoImage(file='images/buttons/next-button.png')
        self.B_next = Button(F_round_result, image=img_forward, bd=0, state="disabled", command=self.next_stage)
        self.B_next.image = img_forward
        # add to grid
        self.L_round_result_title.grid(row=0, column=0, columnspan=3)
        L_round_result_player.grid(row=1, column=0, pady=self.pad_y, padx=self.pad_x)
        L_round_result_pc.grid(row=1, column=2, pady=self.pad_y, padx=self.pad_x)
        self.L_round_result_player_choice_img.grid(row=2, column=0, padx=self.pad_x)
        self.L_round_result_pc_choice_img.grid(row=2, column=2, padx=self.pad_x)
        self.L_player_pick.grid(row=3, column=0, padx=self.pad_x)
        self.L_pc_pick.grid(row=3, column=2, padx=self.pad_x)
        self.B_next.grid(row=4, column=1, pady=self.pad_y, )
        # add to dict
        self.add_widgets(F_round_result, self.L_round_result_title, L_round_result_player, L_round_result_pc,
                         self.L_round_result_player_choice_img, self.L_round_result_pc_choice_img, self.L_player_pick,
                         self.L_pc_pick, self.B_next)
        return F_round_result

    def create_final_result_frame(self):
        """
        creates a frame that show the result of the game
        :return: frame
        """
        F_final_result = Frame(self.root)
        self.L_final_result_img = Label(F_final_result)
        self.L_final_result_player_score = Label(F_final_result, font=self.title_font)
        self.L_final_result_pc_score = Label(F_final_result, font=self.title_font)
        # load image
        img_forward = PhotoImage(file='images/buttons/replay-button.png')
        self.B_replay = Button(F_final_result, image=img_forward, bd=0, command=self.reset_game)
        self.B_replay.image = img_forward
        # add to grid
        self.L_final_result_player_score.grid(row=0, column=0)
        self.L_final_result_pc_score.grid(row=0, column=1)
        self.L_final_result_img.grid(row=1, columnspan=2, pady=self.pad_y, padx=self.pad_x)
        self.B_replay.grid(row=2, columnspan=2, pady=self.pad_y)
        # add to dict
        self.add_widgets(F_final_result, self.L_final_result_img, self.L_final_result_player_score,
                         self.L_final_result_pc_score, self.B_replay)
        return F_final_result

    def start_game(self):
        """
        starting the game
        """
        self.reset_choices()
        self.message.set_message_choose()
        self.send_to_server(self.message)
        self.click_sound_valid()
        self.load_background_music(1, 'sounds/start.wav', self.num_music_loops)
        logging.info('Player started a new game')
        self.player_info.increase_num_games()
        self.F_main_menu.grid_forget()
        self.show_frame_in_grid(self.F_game)

    def play_game(self):
        """
        play game and updates accordingly
        """
        self.click_sound_valid()
        logging.info('Round ' + str(self.round_count))
        self.round_count = self.round_count + 1
        result = self.get_round_result()
        self.update_title_and_scores(result)
        self.B_next.configure(state="normal")
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
            self.update_final_round_frame()
            self.send_info()
            self.F_game.grid_forget()
            self.show_frame_in_grid(self.F_final_result)
        else:
            self.reset_choices()
            self.activate_choices_buttons()
            self.message.set_message_choose()
            self.send_to_server(self.message)
            self.update_scores_and_round_labels()
        self.L_pc_pick.configure(text="Waiting for Pc to choose")
        self.L_player_pick.configure(text="Waiting for you to select")

    def reset_choices(self):
        """
        reset pc and player's selections, reset images, disable button and reset result title
        """
        self.pc_choice = ""
        self.player_choice = ""
        self.reset_images_choices()
        self.B_next.configure(state="disabled")
        self.L_round_result_title.configure(text="")

    def reset_game(self):
        """
        reset all variables and show the main menu
        """
        self.load_background_music(1, 'sounds/play_again.wav', self.num_music_loops)
        logging.info("Game over")
        self.player_info.clear_results()
        self.game_info.start_new_game()
        self.round_count = 1
        self.player_score = 0
        self.pc_score = 0
        self.update_scores_and_round_labels()
        self.activate_choices_buttons()
        self.F_final_result.grid_forget()
        self.start_game()

    def update_scores_and_round_labels(self):
        """
        updates the labels of round and scores
        """
        self.L_player_score.configure(text=self.game_info.get_player_name() + ": " + str(self.player_score))
        self.L_pc_score.configure(text="Pc: " + str(self.pc_score))
        self.L_title.configure(text="Round: " + str(self.round_count))

    def player_pick(self, pick):
        """
        saves the player pick the player choice and config bottom button to normal
        :param pick: what the button represents
        """
        self.click_sound_valid()
        self.disable_choices_buttons()
        self.player_choice = pick
        self.check_if_everybody_choose()
        self.L_player_pick.configure(text="You selected: " + pick)

    def disable_choices_buttons(self):
        """
        disable rock, paper and scissors buttons
        """
        self.B_rock.configure(state="disabled")
        self.B_paper.configure(state="disabled")
        self.B_scissors.configure(state="disabled")

    def activate_choices_buttons(self):
        """
        activate rock, paper and scissors buttons
        """
        self.B_rock.configure(state="normal")
        self.B_paper.configure(state="normal")
        self.B_scissors.configure(state="normal")

    def update_final_round_frame(self):
        """
        updates the titles, image at the final result frame and game info winner, according to the scores
        """
        self.L_final_result_player_score.configure(
            text=self.game_info.get_player_name() + ": " + str(self.player_score))
        self.L_final_result_pc_score.configure(text="Pc: " + str(self.pc_score))
        if self.player_score == self.pc_score:
            self.load_background_music(1, 'sounds/tie.wav', self.num_music_loops)
            self.L_final_result_img.configure(image=self.images.get("tie"))
            self.game_info.winner = "Tie"
            logging.info('The game ended in a tie')
        elif self.player_score > self.pc_score:
            self.load_background_music(1, 'sounds/mixkit-video-game-win-2016.wav', self.num_music_loops)
            self.L_final_result_img.configure(image=self.images.get("win"))
            self.game_info.winner = self.player_info.get_name()
            logging.info('The player won the game')
        else:
            self.load_background_music(1, 'sounds/mixkit-horror-lose-2028.wav', self.num_music_loops)
            self.L_final_result_img.configure(image=self.images.get("lose"))
            self.game_info.winner = "Pc"
            logging.info('The player lost the game')

    def update_title_and_scores(self, result):
        """
        updates the title and scores at the round result frame
        """
        self.update_images_choices()
        self.L_pc_pick.configure(text="Pc selected: " + self.pc_choice)
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
        returns the result of a round
        :return: result
        """
        self.game_info.increase_num_rounds()
        self.increase_selection_counter()
        if self.player_choice == self.pc_choice:
            return "tie"

        if self.player_choice == "rock":
            return self.result("scissors")

        elif self.player_choice == "paper":
            return self.result("rock")

        else:
            return self.result("paper")

    def increase_selection_counter(self):
        if self.player_choice == "rock":
            self.player_info.increase_num_rock()
        elif self.player_choice == "paper":
            self.player_info.increase_num_paper()
        else:
            self.player_info.increase_num_scissors()

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
        image = image.resize((size, size), resample=Image.LANCZOS)
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
        if len(self.player_choice) != 0 and len(self.pc_choice) != 0:
            self.update_images_choices()

    def update_images_choices(self):
        """
        updates the images at the result round frame according to the player and pc choices
        """
        self.L_round_result_pc_choice_img.unload()
        self.L_round_result_player_choice_img.unload()
        self.L_round_result_pc_choice_img.configure(image=self.images.get(self.image_type + self.pc_choice))
        self.L_round_result_player_choice_img.configure(image=self.images.get(self.image_type + self.player_choice))

    def reset_images_choices(self):
        """
        resets the images at the result round frame
        """
        self.L_round_result_pc_choice_img.unload()
        self.L_round_result_player_choice_img.unload()
        self.L_round_result_pc_choice_img.load('images/gif/right_hand.gif')
        self.L_round_result_player_choice_img.load('images/gif/left_hand.gif')

    def exit_app(self):
        """
        send message to server to close the app
        """
        self.message.set_message_exit()
        self.send_to_server(self.message)  # exit

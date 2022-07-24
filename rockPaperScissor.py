"""Rock Paper Scissors Game"""
from tkinter import *
import random
from PIL import ImageTk, Image
import matplotlib.pyplot as plt;

plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from WindowTemplate import WindowTemplate

"""set statistics counter to 0, every win tie or lose increases by 1 and added to the statistics table"""
youcounter = 0
computercounter = 0
tiecounter = 0
"""set to false the click and the options for player, later set to true the option he picked """
click = False
rock = False
paper = False
scissors = False
"""configure the main window of the program and the images for the buttons"""
window_main = WindowTemplate('Client - Rock-Paper-Scissor', False)
window_main.root
window_main.root.wm_attributes("-topmost", 1)
window_main.root.configure(bg="#ffffff")
window_main.root.geometry('+0+0')
window_main.root.iconbitmap("images/Game.ico")
window_main.root.resizable(width=False, height=False)
root = Frame(window_main.root)
root.pack()

image = Image.open('images/rock.jpg')
image = image.resize((180, 180), Image.Resampling.LANCZOS)
rockHandPhoto = ImageTk.PhotoImage(image)

image = Image.open('images/paper.jpg')
image = image.resize((180, 180), Image.Resampling.LANCZOS)
paperHandPhoto = ImageTk.PhotoImage(image)

image = Image.open('images/sci.jpg')
image = image.resize((180, 180), Image.Resampling.LANCZOS)
scissorHandPhoto = ImageTk.PhotoImage(image)

image = Image.open('images/1Daz.gif')
image = image.resize((300, 300), Image.Resampling.LANCZOS)
decisionPhoto = ImageTk.PhotoImage(image)

image = Image.open('images/win.gif')
image = image.resize((300, 300), Image.Resampling.LANCZOS)
winPhoto = ImageTk.PhotoImage(image)

image = Image.open('images/lost.gif')
image = image.resize((300, 300), Image.Resampling.LANCZOS)
losePhoto = ImageTk.PhotoImage(image)

image = Image.open('images/tie.gif')
image = image.resize((300, 300), Image.Resampling.LANCZOS)
tiePhoto = ImageTk.PhotoImage(image)

rockHandButton = " "
paperHandButton = " "
scissorHandButton = " "

resultButton = Button(root, image=decisionPhoto)

"""list to save the states that the player chose, from this will restore the last state"""
saved_states = []


class Game:

    def play(self):
        global rockButton, welcome, paperButton, statButton, scissorButton, click, lastchoice, compPick, you, computer, computerwin, youwin, tie, startbutton, yourchoice, chooserps, playagainbutton, yesButton, undoButton
        """Set images and commands for buttons: """
        rockButton = Button(root, image=rockHandPhoto, command=lambda: self.youPick("Rock"))
        paperButton = Button(root, image=paperHandPhoto, command=lambda: self.youPick("Paper"))
        scissorButton = Button(root, image=scissorHandPhoto, command=lambda: self.youPick("Scissor"))
        statButton = Button(root, text="Statistics", command=self.display_graph)
        startbutton = Button(root, text="Start Game", command=lambda: self.youPick("Start"))
        playagainbutton = Button(root, width=10, text="Play again", command=lambda: self.youPick("PlayAgain"))
        yesButton = Button(root, width=20, text="Yes", command=lambda: self.yesno("Yes"))
        undoButton = Button(root, width=20, text="Undo", command=lambda: self.yesno("Undo"))
        """set labels for the game"""
        chooserps = Label(root, text="The Computer made a choice now Your turn, please choose Rock Paper or Scissors",
                          font=('Helvetica', 10, 'bold'), fg='red')
        welcome = Label(root, text="Welcome to Rock Paper Scissors Game, to start please click on Start Game!",
                        font=('Helvetica', 11, 'bold'))
        yourchoice = Label(root, font=('Helvetica', 12, 'bold'))
        lastchoice = Label(root, font=('Helvetica', 12, 'bold'))
        you = Label(root, text="You", font=('Helvetica', 12, 'bold'))
        computer = Label(root, text="computer", font=('Helvetica', 12, 'bold'))
        youwin = Label(root, text="Yon Won!! Good Job", font=('Helvetica', 12, 'bold'))
        computerwin = Label(root, text="Computer Won :( Good Day", font=('Helvetica', 12, 'bold'))
        tie = Label(root, text="Its a tie!!", font=('Helvetica', 12, 'bold'))

        window_main.add_widgets(window_main.root, root, rockButton, welcome, paperButton, statButton,
                                scissorButton, click,
                                lastchoice, you, computer, computerwin, youwin, tie, startbutton, yourchoice,
                                chooserps, playagainbutton, yesButton, undoButton)
        """placing the buttons on the window"""
        rockButton.grid(row=1, column=0)
        paperButton.grid(row=1, column=1)
        scissorButton.grid(row=1, column=2)

        root.grid_rowconfigure(7, minsize=15)

        resultButton.grid(row=5, column=0, columnspan=50)
        startbutton.grid(row=6, column=0, columnspan=50)
        statButton.grid(row=7, column=0, columnspan=50)
        welcome.grid(row=0, column=0, columnspan=50)

    def computerPick(self):
        """generate random option for the computer"""
        choice = random.choice(["Rock", "Paper", "Scissor"])
        return choice

    def youPick(self, yourChoice):
        global click, compPick, rock, paper, scissors, youcounter, computercounter, tiecounter
        compPick = self.computerPick()
        """start the game, only if the player press click the game will start, click sets to true"""
        if yourChoice == "Start":
            chooserps.grid(row=0, column=0, columnspan=50)
            resultButton.grid(row=7, column=0, columnspan=50)

            """remove the grids that irrelevant for this window"""
            welcome.grid_forget()
            statButton.grid_forget()
            startbutton.grid_forget()
            click = True
        """if click sets to true the player started the game and need to choose an option"""
        if click == True:

            if yourChoice == "Rock":
                """display the choice of the player and the option to change his choice"""
                yourchoice.configure(text="You chose: " + yourChoice + " are you sure?")
                yourchoice.grid(row=2, column=0, columnspan=50)
                yesButton.grid(row=3, column=0, columnspan=2)
                undoButton.grid(row=3, column=1, columnspan=2)
                resultButton.grid(row=7, column=0, columnspan=50)

                """remove the grids that irrelevant for this window"""
                lastchoice.grid_forget()
                statButton.grid_forget()
                startbutton.grid_forget()
                """saving the state to the originator for the option to restore it later"""
                originator.set(yourChoice)
                saved_states.append(originator.save_to_memento())
                """if player chose rock, set it to true"""
                rock = True

            elif yourChoice == "Paper":
                yourchoice.configure(text="You chose: " + yourChoice + " are you sure?")
                yourchoice.grid(row=2, column=0, columnspan=50)
                yesButton.grid(row=3, column=0, columnspan=2)
                undoButton.grid(row=3, column=1, columnspan=2)
                """remove the grids that irrelevant for this window"""
                lastchoice.grid_forget()
                """saving the state to the originator for the option to restore it later"""
                originator.set(yourChoice)
                saved_states.append(originator.save_to_memento())
                """if player chose paper set it to true"""
                paper = True

            elif yourChoice == "Scissor":

                yourchoice.configure(text="You chose: " + yourChoice + " are you sure?")
                yourchoice.grid(row=2, column=0, columnspan=50)
                yesButton.grid(row=3, column=0, columnspan=2)
                undoButton.grid(row=3, column=1, columnspan=2)
                """remove the grids that irrelevant for this window"""
                lastchoice.grid_forget()
                """saving the state to the originator for the option to restore it later"""
                originator.set(yourChoice)
                saved_states.append(originator.save_to_memento())
                """if player chose scissors set it to true"""
                scissors = True

        else:
            """to reset the game and play again"""
            if yourChoice == "PlayAgain":
                """placing and configure the buttons on the window"""
                rockButton.configure(image=rockHandPhoto)
                paperButton.configure(image=paperHandPhoto)
                scissorButton.configure(image=scissorHandPhoto)
                resultButton.configure(image=decisionPhoto)
                welcome.grid(row=0, column=0, columnspan=50)
                resultButton.grid(row=5, column=0, columnspan=50)
                startbutton.grid(row=6, column=0, columnspan=50)
                statButton.grid(row=7, column=0, columnspan=50)
                scissorButton.grid(row=1, column=2)
                """remove the grids that irrelevant for this window"""
                chooserps.grid_forget()
                yesButton.grid_forget()
                undoButton.grid_forget()
                yourchoice.grid_forget()
                lastchoice.grid_forget()
                playagainbutton.grid_forget()
                you.grid_forget()
                computer.grid_forget()
                tie.grid_forget()
                computerwin.grid_forget()
                youwin.grid_forget()

                """set click to false for the initial step"""
                click = False

    def yesno(self, sure):
        global click, compPick, rock, paper, scissors, youcounter, computercounter, tiecounter, lastchoice, last
        if len(saved_states) > 0:
            last = originator.restore_from_memento(saved_states.pop())

        if sure == "Yes" and rock == True:
            """placing and configure the buttons on the window"""
            rockButton.configure(image=rockHandPhoto)
            you.grid(row=0, column=0)
            resultButton.grid(row=5, column=0, columnspan=50)

            if compPick == "Rock":
                """placing and configure the buttons on the window"""
                paperButton.configure(image=rockHandPhoto)
                resultButton.configure(image=tiePhoto)
                computer.grid(row=0, column=1)
                tie.grid(row=6, column=0, columnspan=50)
                playagainbutton.grid(row=7, column=0, columnspan=1)
                """remove the grids that irrelevant for this window"""
                scissorButton.grid_forget()
                startbutton.grid_forget()
                statButton.grid_forget()
                chooserps.grid_forget()
                yourchoice.grid_forget()
                yesButton.grid_forget()
                undoButton.grid_forget()
                lastchoice.grid_forget()
                """counter for the statistics graph"""
                tiecounter += 1

                click = False
                rock = False

            elif compPick == "Paper":
                """placing and configure the buttons on the window"""
                paperButton.configure(image=paperHandPhoto)
                resultButton.configure(image=losePhoto)
                computer.grid(row=0, column=1)
                computerwin.grid(row=6, column=0, columnspan=50)
                playagainbutton.grid(row=7, column=0, columnspan=1)

                """remove the grids that irrelevant for this window"""
                scissorButton.grid_forget()
                startbutton.grid_forget()
                chooserps.grid_forget()
                yesButton.grid_forget()
                lastchoice.grid_forget()
                statButton.grid_forget()
                undoButton.grid_forget()
                yourchoice.grid_forget()
                """counter for the statistics graph"""
                computercounter += 1

                rock = False
                click = False

            elif compPick == "Scissor":
                """placing and configure the buttons on the window"""
                paperButton.configure(image=scissorHandPhoto)
                computer.grid(row=0, column=1)
                youwin.grid(row=6, column=0, columnspan=50)
                resultButton.configure(image=winPhoto)
                playagainbutton.grid(row=7, column=0, columnspan=1)

                """remove the grids that irrelevant for this window"""
                scissorButton.grid_forget()
                yesButton.grid_forget()
                lastchoice.grid_forget()
                startbutton.grid_forget()
                chooserps.grid_forget()
                undoButton.grid_forget()
                yourchoice.grid_forget()
                statButton.grid_forget()

                """counter for the statistics graph"""
                youcounter += 1

                rock = False
                click = False


        elif sure == "Yes" and paper == True:
            """placing and configure the buttons on the window"""
            rockButton.configure(image=paperHandPhoto)
            you.grid(row=0, column=0)
            resultButton.grid(row=5, column=0, columnspan=50)

            if compPick == "Rock":
                """placing and configure the buttons on the window"""
                paperButton.configure(image=rockHandPhoto)
                resultButton.configure(image=winPhoto)
                computer.grid(row=0, column=1)
                youwin.grid(row=6, column=0, columnspan=50)
                playagainbutton.grid(row=7, column=0, columnspan=1)

                """remove the grids that irrelevant for this window"""
                startbutton.grid_forget()
                chooserps.grid_forget()
                yesButton.grid_forget()
                undoButton.grid_forget()
                yourchoice.grid_forget()
                lastchoice.grid_forget()
                scissorButton.grid_forget()
                statButton.grid_forget()

                """counter for the statistics graph"""
                youcounter += 1

                click = False
                paper = False

            elif compPick == "Paper":
                """placing and configure the buttons on the window"""
                paperButton.configure(image=paperHandPhoto)
                resultButton.configure(image=tiePhoto)
                computer.grid(row=0, column=1)
                tie.grid(row=6, column=0, columnspan=50)
                playagainbutton.grid(row=7, column=0, columnspan=1)

                """remove the grids that irrelevant for this window"""
                chooserps.grid_forget()
                startbutton.grid_forget()
                yesButton.grid_forget()
                undoButton.grid_forget()
                lastchoice.grid_forget()
                yourchoice.grid_forget()
                scissorButton.grid_forget()
                statButton.grid_forget()

                """counter for the statistics graph"""
                tiecounter += 1

                click = False
                paper = False


            elif compPick == "Scissor":
                """placing and configure the buttons on the window"""
                paperButton.configure(image=scissorHandPhoto)
                resultButton.configure(image=losePhoto)
                computer.grid(row=0, column=1)
                computerwin.grid(row=6, column=0, columnspan=50)
                playagainbutton.grid(row=7, column=0, columnspan=1)

                """remove the grids that irrelevant for this window"""
                chooserps.grid_forget()
                statButton.grid_forget()
                scissorButton.grid_forget()
                yesButton.grid_forget()
                lastchoice.grid_forget()
                startbutton.grid_forget()
                undoButton.grid_forget()
                yourchoice.grid_forget()
                """counter for the statistics graph"""
                computercounter += 1

                click = False
                paper = False

        elif sure == "Yes" and scissors == True:
            """placing and configure the buttons on the window"""
            rockButton.configure(image=scissorHandPhoto)
            you.grid(row=0, column=0)
            resultButton.grid(row=5, column=0, columnspan=50)

            if compPick == "Rock":
                """placing and configure the buttons on the window"""
                paperButton.configure(image=rockHandPhoto)
                resultButton.configure(image=losePhoto)
                computerwin.grid(row=6, column=0, columnspan=50)
                computer.grid(row=0, column=1)
                playagainbutton.grid(row=7, column=0, columnspan=1)

                """remove the grids that irrelevant for this window"""
                startbutton.grid_forget()
                chooserps.grid_forget()
                yesButton.grid_forget()
                undoButton.grid_forget()
                lastchoice.grid_forget()
                yourchoice.grid_forget()
                statButton.grid_forget()
                scissorButton.grid_forget()

                """counter for the statistics graph"""
                computercounter += 1

                scissors = False
                click = False

            elif compPick == "Paper":
                """placing and configure the buttons on the window"""
                paperButton.configure(image=paperHandPhoto)
                resultButton.configure(image=winPhoto)
                computer.grid(row=0, column=1)
                youwin.grid(row=6, column=0, columnspan=50)
                playagainbutton.grid(row=7, column=0, columnspan=1)

                """remove the grids that irrelevant for this window"""
                startbutton.grid_forget()
                chooserps.grid_forget()
                scissorButton.grid_forget()
                statButton.grid_forget()
                yesButton.grid_forget()
                lastchoice.grid_forget()
                undoButton.grid_forget()
                yourchoice.grid_forget()

                """counter for the statistics graph"""
                youcounter += 1

                scissors = False
                click = False

            elif compPick == "Scissor":
                """placing and configure the buttons on the window"""
                paperButton.configure(image=scissorHandPhoto)
                resultButton.configure(image=tiePhoto)
                computer.grid(row=0, column=1)
                tie.grid(row=6, column=0, columnspan=50)
                playagainbutton.grid(row=7, column=0, columnspan=1)

                """remove the grids that irrelevant for this window"""
                yesButton.grid_forget()
                undoButton.grid_forget()
                lastchoice.grid_forget()
                yourchoice.grid_forget()
                scissorButton.grid_forget()
                chooserps.grid_forget()
                statButton.grid_forget()
                startbutton.grid_forget()
                """counter for the statistics graph"""
                tiecounter += 1

                click = False
                scissors = False

        if sure == "Undo":
            """placing and configure the buttons on the window"""
            lastchoice.configure(text="your last choice was " + last + " you can choose other option now")
            lastchoice.grid(row=2, column=0, columnspan=50)
            """remove the grids that irrelevant for this window"""
            undoButton.grid_forget()
            yesButton.grid_forget()

    """function for making the statistics graph"""

    def display_graph(self):
        x = ["you", "computer", "tie"]
        """list of the counters from the game"""
        z = [youcounter, computercounter, tiecounter]
        y_pos = np.arange(len(x))

        lns1 = plt.bar(y_pos, z)
        plt.ylabel('Bar Graph')

        plt.ylabel('Line Data')
        plt.xticks(y_pos, x)
        plt.title('Game Statistics')

        plt.draw()
        plt.show()


"""the memento classes that used in the project, saving the player choices and restoring it later"""


class Memento:
    def __init__(self, state) -> None:
        self._state = state

    def get_saved_state(self):
        return self._state


class Originator:
    _state = ""

    def set(self, state) -> None:
        self._state = state

    def save_to_memento(self) -> Memento:
        return Memento(self._state)

    def restore_from_memento(self, memento) -> _state:
        self._state = memento.get_saved_state()
        return self._state


originator = Originator()

if __name__ == '__main__':
    """start the game"""
    game = Game()
    game.play()
    root.mainloop()

import os

from ServerWindow import ServerWindow
from GameWindow import GameWindow


def main():
    server_frame = ServerWindow('server')
    server_frame.root.mainloop()


main()

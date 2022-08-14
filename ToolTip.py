# https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python
from tkinter import *


class ToolTip(object):

    def __init__(self, widget):
        """
        init ToolTip
        :param widget: a widget to attach the ToolTip
        """
        self.widget = widget
        self.tip_window = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        """
        Display text in tooltip window
        :param text: text to display
        :return: none if text or tip_window are none
        """
        self.text = text
        if self.tip_window or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 33
        self.tip_window = tw = Toplevel(self.widget)
        self.tip_window.attributes("-topmost", True)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        """
        hides and destroys ToolTip
        """
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()


def CreateToolTip(widget, text):
    """
    creates ToolTip and binds it to events
    :param widget: a widget to attach the ToolTip
    :param text: text to display
    """
    toolTip = ToolTip(widget)

    def enter(event):
        """
        display text on event
        :param event: event
        """
        toolTip.showtip(text)

    def leave(event):
        """
        hides text on event
        :param event: event
        """
        toolTip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

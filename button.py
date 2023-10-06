# button.py
from graphics import *


class Button:

    """A button is a labeled rectangle in a window.
    It is activated or deactivated with the activate()
    and deactivate() methods. The clicked(p) method
    returns true if the button is active and p is inside it."""

    def __init__(self, win, center, width, height, label, color='lightgrey', display_label=True):
        """ Creates a rectangular button, eg:
        qb = Button(myWin, centerPoint, width, height, 'Quit') """
        w, h = width/2.0, height/2.0
        x, y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1, p2)
        if color:
            self.rect.setFill(color)
        self.rect.draw(win)
        self.label = Text(center, label)
        if display_label:
            self.label.draw(win)
        self.deactivate()

    def activate(self):
        "Sets this button to 'active'."
        self.label.setFill('black')
        self.rect.setWidth(2)
        self.active = True

    def deactivate(self):
        "Sets this button to 'inactive'."
        self.label.setFill('darkgrey')
        self.rect.setWidth(1)
        self.active = False

    def clicked(self, p):
        "Returns true if button is active and p is inside."
        return (self.active and
            self.xmin <= p.getX() <= self.xmax and
            self.ymin <= p.getY() <= self.ymax)
    def getLabel(self):
        "Returns the label string of this button."
        return self.label.getText()

    def undraw(self):
        self.deactivate()
        self.rect.undraw()

    def textSize(self, pixel):
        "Adj the text size to specified value."
        self.label.setSize(pixel)

    def textStyle(self, style):
        "Changes the style of the label"
        self.label.setStyle(style)

    def setColor(self, color):
        "Changes the color of the button"
        self.rect.setFill(color)

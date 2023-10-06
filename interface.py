# interface.py
# It contains the classes for the interface of the game.
# It has Graphical Interface and Text Interface
from graphics import *
from button import Button


class TextInterface:

    def __init__(self):
        print("Welcome to video poker.")

    def setMoney(self, amt):
        print("You currently have ${}.".format(amt))

    def setDice(self, values):
        print("Dice:", values)

    def wantToPlay(self):
        ans = input("Do you wish to try your luck? ")
        return ans[0] in "yY"

    def close(self):
        print("\nThanks for playing!")

    def showResult(self, msg, score):
        print("{}. You win ${}.".format(msg, score))

    def chooseDice(self):
        return eval(input("Enter list of which to change ([] to stop) "))


class PokerInterface:

    def __init__(self, win, center, size):
        """Create a view of a die, e.g.:
        d1 = DieView(myWin, Point(40,50), 20)
        creates a die centered at (40,50) having sides
        of length 20."""

        # first define some standard values
        self.win = win            # save this for drawing pips later
        self.background = 'white' # color of die face
        self.foreground = 'black' # color of the pips
        self.psize = 0.1 * size   # radius of each pip
        hsize = size/2.0          # half the size of the die
        offset = 0.6 * hsize      # distance from center to outer pips

        # creates a square for the face
        cx,cy = center.getX(),center.getY()
        p1 = Point(cx-hsize, cy-hsize)
        p2 = Point(cx+hsize, cy+hsize)
        rect = Rectangle(p1, p2)
        rect.draw(win)
        rect.setFill(self.background)
        rect.setOutline('red')

        # create 7 circles for standard pip locations
        self.pips = [
        self.__makePip(cx+offset,cy+offset),
        self.__makePip(cx-offset,cy-offset),
        self.__makePip(cx-offset,cy),
        self.__makePip(cx-offset,cy+offset),
        self.__makePip(cx,cy),
        self.__makePip(cx+offset,cy-offset),
        self.__makePip(cx+offset,cy)
        ]

        # Create a table for which pips are on for each value
        self.onTable = [ [], [4], [0,1], [0,1,4,], [0,1,3,5], [0,1,3,4,5], [0,1,2,3,5,6], ]

        # Draw an initial value
        self.setValue(1)

    def __makePip(self, x, y):
        "Internal helper method to draw a pip at (x,y)"
        pip = Circle(Point(x,y), self.psize)
        pip.setFill(self.background)
        pip.setOutline(self.background)
        pip.draw(self.win)
        return pip

    def setValue(self, value):
        "Set this die to display value."
        # turn all pips off
        for pip in self.pips:
            pip.setFill(self.background)
        # turn correct pips on
        for i in self.onTable[value]:
            self.pips[i].setFill(self.foreground)
        self.value = value

    def setColor(self, color):
        self.foreground = color
        self.setValue(self.value)


class GraphicsInterface:


    def __init__(self):

        self.win = GraphWin("Dice Poker", 600, 400)
        self.win.setBackground("green3")
        banner = Text(Point(300, 30), "Python Poker Parlor")
        banner.setSize(24)
        banner.setFill("yellow2")
        banner.setStyle("bold")
        banner.draw(self.win)
        self.msg = Text(Point(300, 380), "Welcome to the Dice Table")
        self.msg.setSize(18)
        self.msg.draw(self.win)
        self.createDice(Point(300,100), 75)
        self.buttons = []
        self.addDiceButtons(Point(300,100), 75)
        b = Button(self.win, Point(300, 230), 400, 40, "Roll Dice")
        self.buttons.append(b)
        b = Button(self.win, Point(300, 280), 150, 40, "Score")
        self.buttons.append(b)
        b = Button(self.win, Point(570,375), 40,30, "Quit")
        self.buttons.append(b)
        self.money = Text(Point(300, 325), "$")
        self.money.setSize(18)
        self.money.draw(self.win)


    def createDice(self, center, size):
        center.move(-3*size, 0)
        self.dice = []
        for i in range(5):
            view = PokerInterface(self.win, center, size)
            self.dice.append(view)
            center. move(1.5*size, 0)

    def addDiceButtons(self, center, size):
        center.move(-3*size, 0)
        for i in range(1, 6):
            label = f"Die {i}"
            b = Button(self.win, center, size, size, label, color=None, display_label=False)
            self.buttons.append(b)
            center.move(1.5*size, 0)

    def setMoney(self, amt):
        self.money.setText("${}".format(amt))

    def showResult(self, msg, score):
        if score > 0:
            text = "{}! You win ${}".format(msg, score)
        else:
            text = "You rolled {}".format(msg)
        self.msg.setText(text)

    def setDice(self, values):
        for i in range(5):
            self.dice[i].setValue(values[i])


    def chooseDice(self):
        # choices is a list of the indexes of the selected dice
        choices = []                    # No dice chosen yet
        while True:
            # wait for user to click a valid button
            b = self.choose(["Die 1", "Die 2", "Die 3", "Die 4", "Die 5", "Roll Dice", "Score"])
            if b[0] == "D":             # User clicked a die button
                i = int(b[4]) - 1       # Translate label to die index
                if i in choices:        # Currently selected, unselect it
                    choices.remove(i)
                    self.dice[i].setColor("black")
                else:                   # Currently unselected, select it
                    choices.append(i)
                    self.dice[i].setColor("lightgrey")
            else:                       # User clicked Roll or Score
                for d in self.dice:     # Revert appearance of all dice
                    d.setColor("black")
                if b == "Score":        # Score clicked, igmore choices
                    return []
                elif choices != []:     # Don't accept Roll unless some dice are actually selected
                    return choices

    def choose(self, choices):
        buttons = self.buttons

        # activate choice buttons, deactivate others
        for b in buttons:
            if b.getLabel() in choices:
                b.activate()
            else:
                b.deactivate()

        # get mouse clicks until an active button is clicked
        while True:
            p = self.win.getMouse()
            for b in buttons:
                if b.clicked(p):
                    return b.getLabel()     # function exit here

    def wantToPlay(self):
        ans = self.choose(["Roll Dice", "Quit"])
        self.msg.setText("")
        return ans == "Roll Dice"

    def close(self):
        self.win.close()

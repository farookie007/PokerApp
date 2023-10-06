# poker.py

from random import randrange


class Dice:

    def __init__(self):
        self.dice = [0]*5
        self.rollAll()

    def roll(self, which):
        "Rolls a subset of the dice"
        for pos in which:
            self.dice[pos] = randrange(1,7)

    def rollAll(self):
        "Rolls all dice available."
        self.roll(range(5))

    def values(self):
        "Return the values of all the dice."
        return self.dice[:] # list slicing was used to produce a copy of the list to avoid altercation by the user

    def score(self):
        "Scores the result of the dice after rolling."
        # Create the counts list
        counts = [0] * 7
        for value in self.dice:
            counts[value] += 1

        # score the hand
        if 5 in counts:
            return "Five of a Kind", 30
        elif 4 in counts:
            return "Four of a Kind", 15
        elif (3 in counts) and (2 in counts):
            return "Full House", 12
        elif 3 in counts:
            return "Three of a Kind", 8
        elif not (2 in counts) and (counts[1]==0 or counts[6]==0):
            return "Straight", 20
        elif counts.count(2) == 2:
            return "Two Pairs", 5
        else:
            return "Garbage", 0


class PokerApp:
    "Emulates the Poker Game with Interface."

    def __init__(self, interface):
        self.dice = Dice()
        self.money = 150
        self.interface = interface
        self.interface.setMoney(self.money)

    def run(self):
        "Continues playing until player's money falls below 10."
        while self.money >= 10 and self.interface.wantToPlay():
            self.playRound()
        self.interface.close()

    def playRound(self):
        self.money -= 10
        self.interface.setMoney(self.money)
        self.doRolls()
        result, score = self.dice.score()
        self.interface.showResult(result, score)
        self.money += score
        self.interface.setMoney(self.money)

    def doRolls(self):
        self.dice.rollAll()
        roll = 1
        self.interface.setDice(self.dice.values())
        toRoll = self.interface.chooseDice()
        while roll < 3 and toRoll != []:
            self.dice.roll(toRoll)
            roll += 1
            self.interface.setDice(self.dice.values())
            if roll < 3:
                toRoll = self.interface.chooseDice()

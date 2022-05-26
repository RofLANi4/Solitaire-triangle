# Artem Zhowtovatyuk KH-20

import os
import random
import sys

from PyQt5 import uic, QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication, QPushButton, QMessageBox


class Card(QPushButton):
    def __init__(self, suit, value, i, j):
        super().__init__()
        self.value = value
        self.suit = suit
        self.j = j
        self.i = i
        self.cardIcon = f"Card/{value} {suit}.png"

        if self.i == 5:
            self.setIcon(QtGui.QIcon(self.cardIcon))
        elif self.value is None:
            pass
        else:
            self.setIcon(QtGui.QIcon("Card/Back.png"))
            self.cardIcon = "Card/Back.png"

        self.setIconSize(QtCore.QSize(145, 214))
        self.setMaximumSize(150, 217)
        self.move(self.j, self.i * 100 + 50)
        self.clicked.connect(self.was_clicked)

        if self.j == 1140:
            self.helpCard = HelpCard(self)

    def was_clicked(self):
        if self.j == 1140 and self.cardIcon == "Card/Back.png" and self.value is not None:
            self.helpCard.help()
            return
        elif self.j == 1139:
            self.helpCard = HelpCard(self)
            self.helpCard.help()
            return
        elif self.cardIcon == "Card/Back.png":
            return
        test = CheckWin(self, self.value)
        test.test()
        Back.back()


class HelpCard:
    allHelpCard = []
    allDeskHelpCard = []

    def __init__(self, card):
        HelpCard.allHelpCard.append(card)
        self.card = card

    def help(self):
        for i in HelpCard.allHelpCard:
            if i.isHidden():
                HelpCard.allHelpCard.remove(i)
        if HelpCard.allHelpCard[-1].suit is not None:
            HelpCard.allHelpCard[0].setIcon(
                QtGui.QIcon(f"Card/{HelpCard.allHelpCard[0].value} {HelpCard.allHelpCard[0].suit}.png"))
            HelpCard.allHelpCard[0].move(980, 50)
            HelpCard.allHelpCard[0].cardIcon = f"Card/{HelpCard.allHelpCard[0].value} {HelpCard.allHelpCard[0].suit}.png"
            HelpCard.allDeskHelpCard.append(HelpCard.allHelpCard[0])
            del HelpCard.allHelpCard[0]
        elif HelpCard.allHelpCard[-1].suit is None:
            HelpCard.allHelpCard = HelpCard.allDeskHelpCard[0:]
            HelpCard.allDeskHelpCard.clear()
            for i in HelpCard.allHelpCard:
                i.move(1140, 50)
                i.setIcon(QtGui.QIcon(f"Card/Back.png"))
                i.cardIcon = f"Card/Back.png"


class Back:
    allDeskCard = []

    def __init__(self, card):
        if len(Back.allDeskCard) == card.i:
            Back.allDeskCard.append([])
        Back.allDeskCard[card.i].append(card)

    @staticmethod
    def back():
        for i in range(len(Back.allDeskCard)):
            for j in range(i):
                if (Back.allDeskCard[i][j]).isHidden() and (Back.allDeskCard[i][j + 1]).isHidden():
                    (Back.allDeskCard[i - 1][j]).setIcon(QtGui.QIcon(f"Card/{(Back.allDeskCard[i - 1][j]).value} {(Back.allDeskCard[i - 1][j]).suit}.png"))
                    (Back.allDeskCard[i - 1][j]).cardIcon = f"Card/{(Back.allDeskCard[i - 1][j]).value} {(Back.allDeskCard[i - 1][j]).suit}.png"


class CheckWin:
    win = ""
    stack = []

    def __init__(self, card, value):
        self.card = card
        self.value = value
        self.if_stack_is_full = IfStackIsFull(CheckWin.stack, self.card)
        self.msg = QMessageBox()

    def test(self):

        CheckWin.stack.append(self.card)
        self.card.setStyleSheet('border-style: solid; border-width: 5px; border-color: black;')
        CheckWin.win += f"+{self.value}"

        if eval(CheckWin.win) == 13:
            self.card.hide()
            CheckWin.win = ""
            ClearStack(CheckWin.stack)
            if self.card.i == 0 and self.card.j == 600:
                player = QMediaPlayer()
                path = os.path.join(os.getcwd(), "Card/VI KA Гимн ПапичаArthas.mp3")
                url = QUrl.fromLocalFile(path)
                content = QMediaContent(url)
                player.setMedia(content)
                player.play()
                self.msg.setWindowTitle("Перемога")
                self.msg.setText("Ви перемогли")
                self.msg.exec()

        elif len(CheckWin.win) > 3:
            self.if_stack_is_full.stack_full()
            CheckWin.win = ""


class IfStackIsFull:
    def __init__(self, stack, card):
        self.stack = stack
        self.card = card

    def stack_full(self):
        self.stack.pop()
        self.stack[0].setStyleSheet('border-style: solid; border-width: 0px; border-color: black;')
        self.card.setStyleSheet('border-style: solid; border-width: 0px; border-color: black;')
        self.stack.clear()
        return self.stack, self.card


class ClearStack:
    def __init__(self, stack):
        stack[0].hide()
        stack.clear()


class MainField(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("Card/untitled.ui")
        self.ui.label.setPixmap(QtGui.QPixmap("Card/BackGround.jpg"))
        suit = ["C", "D", "H", "S"]
        value = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]

        create_card_aray = CreateAllCardAray(suit, value)
        allCard = create_card_aray.aray()

        random.shuffle(allCard)
        for i in range(6):
            for j in range(i + 1):
                CreateGameField(allCard[0].split(" ")[0], allCard[0].split(" ")[1], i, ((6 - i) + (j * 2)) * 100, self.ui)
                del allCard[0]

        CreateGameField(None, None, 0, 1139, self.ui)

        for i in allCard:
            CreateGameField(i.split(" ")[0], i.split(" ")[1], 0, 1140, self.ui)

        self.ui.show()


class CreateAllCardAray:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def aray(self):
        allCard = []
        for i in self.suit:
            for j in self.value:
                allCard.append(f"{i} {j}")
        return allCard


class CreateGameField:
    def __init__(self, suit, value, i, j, ui):
        card = Card(suit, value, i, j)
        if j <= 1100:
            Back(card)
        self.ui = ui
        self.ui.layout().addWidget(card)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tks = MainField()
    sys.exit(app.exec())

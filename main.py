from termcolor import colored
from os import system, name
from keyboard import is_pressed
from time import sleep
import time
import colorama
import ctypes
import random


N = 20  # maxY
M = 25  # maxX


class Player:
    states = ['↑', '→', '↓', '←']
    vects = [[-1, 0], [0, 1], [1, 0], [0, -1]]

    def __init__(self, x, y):
        self.state = 0
        self.x = x
        self.y = y
        self.out = colored(Player.states[self.state], "red")

    def changeState(self, st):
        if st < 0 or st > 3:
            raise Exception(f"state out of bound: {st}")
        self.state = st
        self.out = colored(Player.states[self.state], "red")

    def move(self, st):
        self.changeState(st)
        if (8 <= self.x + Player.vects[st][0] < N and
                0 <= self.y + Player.vects[st][1] < M):
            self.x += Player.vects[st][0]
            self.y += Player.vects[st][1]


class Field:
    def __init__(self):
        self.score = 0
        self.player = Player(N - 1, M // 2)
        self.field = [generateRow(8) for i in range(N)]
        self.field[self.player.x][self.player.y] = self.player.out
        self.last_fall = time.time_ns()

    def drawAll(self):
        output = colored(" " * ((M - 13) // 2) + "SNOWFALL GAME" + " " * ((M - 13) // 2), "light_grey") + "\n"
        output += colored("=" * M, "light_grey") + "\n"
        for i in range(len(self.field)):
            s = "".join(self.field[i])
            s += "\n"
            output += s
        output += colored("=" * M, "light_grey") + "\n"
        output += f"Score: {self.score}"
        system("cls")
        print(output)

    def checkIfBroken(self):
        if (self.field[self.player.x][self.player.y] != ' '):
            self.field[self.player.x][self.player.y] = self.player.out
            self.drawAll()
            print(f"Game over! Score: {self.score}")
            exit()

    def move(self, st):
        self.field[self.player.x][self.player.y] = ' '
        self.player.move(st)
        self.checkIfBroken()
        self.field[self.player.x][self.player.y] = self.player.out
        self.drawAll()
        sleep(0.1)

    def snowFall(self):
        if (time.time_ns() - self.last_fall > 10 ** 9):
            self.field[self.player.x][self.player.y] = ' '
            self.field.remove(self.field[N - 1])
            self.field.insert(0, generateRow(8))
            self.checkIfBroken()
            self.field[self.player.x][self.player.y] = self.player.out
            self.last_fall = time.time_ns()
            self.score += 1
            self.drawAll()


def generateRow(percent: int):
    if percent < 0 or percent > 100:
        raise Exception(f"percent must be in range [0, 100], {percent}")

    ar = [colored("*", "cyan") if random.randint(1, 100) <= percent else ' ' for _ in range(M)]
    return ar

def hide_cursor():
    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]

    if name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))


if __name__ == '__main__':
    random.seed(time.time())
    hide_cursor()
    colorama.init()

    field = Field()
    field.drawAll()

    while True:
        if is_pressed("w") or is_pressed("W"):
            field.move(0)
        if is_pressed("d") or is_pressed("D"):
            field.move(1)
        elif is_pressed("s") or is_pressed("S"):
            field.move(2)
        elif is_pressed("a") or is_pressed("A"):
            field.move(3)
        elif is_pressed("esc"):
            exit()
        field.snowFall()

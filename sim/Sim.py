import numpy as np
from FieldObjects import *
import os
import time


class Sim:
    def __init__(self, size_x, size_y):
        self.__size_x = size_x
        self.__size_y = size_y
        self.field = [[None for y in range(size_y)] for x in range(size_x)]
        self.__delay = 1.0
    
    def addFieldObject(self, o):
        self.field[o.getX()][o.getY()] = o

    def getSize(self):
        return self.__size_x, self.__size_y

    def getDelay(self):
        return self.__delay

    def setDelay(self, delay):
        self.__delay = delay

    def update(self):
        new_field = []
        for i in range(self.__size_x):
            new_field.append([x for x in self.field[i]])

        for i in range(self.__size_x):
            for j in range(self.__size_y):
                if isinstance(self.field[i][j], Drone):
                    d = self.field[i][j]
                    new_field[i][j] = None
                    d.update(self.field)
                    newI, newJ = d.getPos()
                    if 0 <= newI < self.__size_x and 0 <= newJ < self.__size_y:
                        new_field[newI][newJ] = d
        self.field = new_field

    def print(self):
        fstr = "{:^3}"
        os.system('cls' if os.name=='nt' else 'clear')

        print(" ", end="")
        for _ in range(self.__size_y):
            print(fstr.format("="), end="")
        print()

        for col in self.field:
            print('|', end="")
            for c in col:
                print(fstr.format("" if c is None else str(c)), end="")
            print('|')

        print(" ", end="")
        for _ in range(self.__size_y):
            print(fstr.format("="), end="")
        print()

    def __str__(self):
        res = ""
        fstr = "{:^3}"

        res += " "
        for _ in range(self.__size_y):
            res += fstr.format("=")
        res += '\n'

        for col in self.field:
            res += '|'
            for c in col:
                res += fstr.format("" if c is None else str(c))
            res += "|\n"

        res += " "
        for _ in range(self.__size_y):
            res += fstr.format("=")
        
        return res

    def clear_screen(self):
        os.system('cls' if os.name=='nt' else 'clear')
        

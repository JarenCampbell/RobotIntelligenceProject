import numpy as np
from FieldObjects import *
import os
import time

class Sim:
    def __init__(self, size_x, size_y):
        self.__size_x = size_x
        self.__size_y = size_y
        self.__field = np.full((size_y, size_x), None, dtype=FieldObject)
        self.__delay = 1.0
    
    def addFieldObject(self, o):
        self.__field[o.getY()][o.getX()] = o

    def getSize(self):
        return (self.__size_x, self.__size_y)

    def getDelay(self):
        return self.__delay

    def setDelay(self, delay):
        self.__delay = delay

    def update(self):
        new_field = self.__field.copy()
        for i in range(self.__size_x):
            for j in range(self.__size_y):
                if isinstance(self.__field[j, i], Drone):
                    d = self.__field[j, i]
                    new_field[j, i] = None
                    d.update(self.__field)
                    newI, newJ = d.getPos() 
                    if newI < self.__size_x and newJ < self.__size_y and new_field[newJ, newI] is None:
                        new_field[newJ, newI] = d
                    else:
                        d.setSymbol("x")
                        new_field[j, i] = d     # if running off the edge, stay in place
        self.__field = new_field


    def print(self):
        fstr = "{:^3}"
        os.system('cls' if os.name=='nt' else 'clear')

        print(" ", end="")
        for _ in range(self.__size_x):
            print(fstr.format("="), end="")
        print()

        for col in self.__field:
            print('|', end="")
            for c in col:
                print(fstr.format("" if c is None else str(c)), end="")
            print('|')

        print(" ", end="")
        for _ in range(self.__size_x):
            print(fstr.format("="), end="")
        print()
        

if __name__ == "__main__":
    sim = Sim(10, 25)
    sim.setDelay(1.5)
    sim.addFieldObject(Obstacle(2, 3))
    sim.addFieldObject(Obstacle(2, 2))
    sim.addFieldObject(Obstacle(2, 1))
    sim.addFieldObject(Obstacle(9, 5))
    sim.addFieldObject(Goal(8, 12))
    sim.addFieldObject(TestDrone1(4, 5))
    sim.addFieldObject(TestDrone2(2, 11))

    for i in range(9):
        sim.print()
        print("=== Simulation is on update {} ===".format(i))
        time.sleep(sim.getDelay())
        sim.update()
    sim.print()
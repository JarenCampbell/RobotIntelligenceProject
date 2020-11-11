import numpy as np
from FieldObject import *

class Sim:
    def __init__(self, size_x, size_y):
        self.__size_x = size_x
        self.__size_y = size_y
        self.__field = np.full((size_y, size_x), None, dtype=FieldObject)
        # self.__drones = []
        self.__delay = 0.0
    
    def addFieldObject(self, o):
        self.__field[o.getY()][o.getX()] = o

    def getSize(self):
        return (self.__size_x, self.__size_y)

    def setDelay(self, delay):
        self.__delay = delay

    # def addDrone(self, drone):
    #     self.__drones.append(drone)

    # def update(self):
    #     for drone in self.__drones:
    #         drone.update()

    def render(self, do_update=False):
        pass

    def print(self):
        fstr = "{:^3}"

        print(" ", end="")
        for i in range(self.__size_x):
            print(fstr.format("="), end="")
        print()

        for row in self.__field:
            print('|', end="")
            for c in row:
                print(fstr.format("" if c is None else str(c)), end="")
            print('|')

        print(" ", end="")
        for i in range(self.__size_x):
            print(fstr.format("="), end="")
        print()

if __name__ == "__main__":
    sim = Sim(10, 20)
    sim.addFieldObject(Obstacle(2, 3))
    sim.addFieldObject(Obstacle(2, 2))
    sim.addFieldObject(Obstacle(2, 1))
    sim.addFieldObject(Goal(8, 12))

    sim.print()
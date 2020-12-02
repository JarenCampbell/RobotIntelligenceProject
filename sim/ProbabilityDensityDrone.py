from FieldObjects import Drone, Obstacle, Goal
# import FieldObjects
# from FieldObjects.py import *
import numpy as np
from random import randint
from math import inf
from random import shuffle

class ProbabilityDensityDrone(Drone):
    def __init__(self, posx:int, posy:int, field_size:tuple):
        super().__init__(posx, posy)
        self.__field_size = field_size
        self.__probability_density = np.zeros(field_size, dtype=float)

    def update(self, field):
        field = np.array(field)
        if -inf in self.__probability_density:
            return True
        moves = []
        x, y = super().getPos()
        illegal_moves = []
        possible_moves = [(x, y), (x+1, y), (x-1, y), (x, y+1), (x, y-1) ]#, (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)]
        for _x, _y in possible_moves:
            if _x >= self.__field_size[0] or _x < 0 or _y >= self.__field_size[1] or _y < 0:
                continue
            if isinstance(field[_x, _y], Goal):
                self.__probability_density[_x, _y] = -inf
                self.setSymbol("X")
                return True
            if isinstance(field[_x, _y], Obstacle):
                self.__probability_density[_x, _y] = inf
            else:
                self.__probability_density[_x, _y] += 0.5     # increase probability density at checked spots
                moves.append((self.__probability_density[_x, _y], (_x, _y)))

        #search for other drones
        for _x in range(x-2, x+3):
            for _y in range(y-2, y+3):
                if _x < 0 or _y < 0:
                    continue
                if _x >= self.__field_size[0] or _y >= self.__field_size[1]:
                    continue
                if _x == x and _y == y:
                    continue
                if isinstance(field[_x, _y], Drone):
                    field[_x, _y].update_probability_density(self.__probability_density)
                    self.update_probability_density(field[_x, _y].get_probability_density())
                    illegal_moves.append(field[_x, _y].getPos()) 
                
        
        #remove illegal moves
        for l in illegal_moves:
            for i in range(len(moves)):
                if len(moves) > 0:
                    if moves[i][1] == l:
                        moves.pop(i)
                        break
                
        try:
            shuffle(moves)
            min_density = inf
            min_x = x
            min_y = y
            for m in moves:
                if m[0] < min_density:
                    min_density = m[0]
                    min_x, min_y = m[1]
            # min_density, (min_x, min_y) = min(moves)
        except ValueError:
            return
        super().update(min_x, min_y)
        self.__probability_density[min_x, min_y] += 0.5
        return False

    def get_probability_density(self):
        return self.__probability_density
        
    def update_probability_density(self, prob):
        for i in range(self.__field_size[0]):
            for j in range(self.__field_size[1]):
                if prob[i, j] > self.__probability_density[i, j]:
                    self.__probability_density[i, j] = prob[i, j]


if __name__ == "__main__":
    d = ProbabilityDensityDrone(1, 2, (5,6))
    d.update([[None for i in range(5)] for j in range(5)])

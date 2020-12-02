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
        if -1 not in self.__probability_density or 2 in self.__probability_density:
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
                    field[_x, _y].recieveSearched(self.__probability_density)
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
            min_density, (min_x, min_y) = min(moves)
        except ValueError:
            return
        super().update(min_x, min_y)
        self.__probability_density[min_x, min_y] += 0.5
        return False

        
    # def _find_random(self):
    #     self.__hist = []
    #     while 0 in self.__probability_density:
    #         rand_x = randint(0, self.__field_size[0]-1)
    #         rand_y = randint(0, self.__field_size[1]-1)
    #         if self.__probability_density[rand_x, rand_y] == 0:
    #             break
    #     self.__temp_goal = (rand_x, rand_y) 

    # def __cost(self, pos):
    #     goal = self.__temp_goal
    #     if self.__probability_density[pos] == -1:
    #         return inf
    #     if goal == pos:
    #         return 0

    #     del_x = abs(pos[0] - goal[0])
    #     del_y = abs(pos[1] - goal[1])

    #     if self.__probability_density[pos] == 1:
    #         offset = self.__offset_size
    #     else:
    #         offset = 0
    #     return pow( pow(del_y, 2) + pow(del_x, 2) , 0.5) + offset


    def recieve_probability_density(self, prob):
        for i in range(self.__field_size[0]):
            for j in range(self.__field_size[1]):
                if prob[i, j] > self.__probability_density[i, j]:
                    self.__probability_density[i, j] = prob[i, j]


if __name__ == "__main__":
    d = ProbabilityDensityDrone(1, 2, (5,6))
    d.update([[None for i in range(5)] for j in range(5)])

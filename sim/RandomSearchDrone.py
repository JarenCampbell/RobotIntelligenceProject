from FieldObjects import Drone, Obstacle, Goal
# import FieldObjects
# from FieldObjects.py import *
import numpy as np
from random import randint
from math import inf

class RandomSearchDrone(Drone):
    def __init__(self, posx:int, posy:int, field_size:tuple):
        super().__init__(posx, posy)
        self.__field_size = field_size
        self.__offset_size = np.mean(field_size) * 0.25
        self.__searched = np.zeros(field_size, dtype=int)
        self.__temp_goal = randint(0, field_size[0]-1), randint(0, field_size[1]-1)
        self.__hist = []
        self.__code = {None: 1,
                       Obstacle: -1,
                       Goal: 2
                       }

    def update(self, field):
        field = np.array(field)
        if 0 not in self.__searched or 2 in self.__searched:
            return
        if self.__searched[self.__temp_goal] != 0:
            self._find_random()
        moves = []
        x, y = super().getPos()
        illegal_moves = []
        possible_moves = [(x, y), (x+1, y), (x-1, y), (x, y+1), (x, y-1) ]#, (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)]
        for _x, _y in possible_moves:
            if _x >= self.__field_size[0] or _x < 0 or _y >= self.__field_size[1] or _y < 0:
                continue
            if isinstance(field[_x, _y], Goal):
                self.__searched[_x, _y] = self.__code[Goal]
                self.__temp_goal = (_x, _y)
                self.setSymbol("X")
                return True
            # if isinstance(field[_x, _y], Drone):
            #     field[_x, _y].recieveSearched(self.__searched)
            #     illegal_moves.append(field[_x, _y].getPos())
            if isinstance(field[_x, _y], Obstacle):
                self.__searched[_x, _y] = self.__code[Obstacle]
            else:
                moves.append((self.__cost((_x, _y)), (_x, _y)))

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
                    field[_x, _y].recieveSearched(self.__searched)
                    illegal_moves.append(field[_x, _y].getPos()) 
                
        
        #remove illegal moves
        for l in illegal_moves:
            for i in range(len(moves)):
                if len(moves) > 0:
                    if moves[i][1] == l:
                        moves.pop(i)
                        break
                
        try:
            min_val, (min_x, min_y) = min(moves)
        except ValueError:
            return
        if (min_x, min_y) == (x, y):    # local minima
            self._find_random()
        elif (min_x, min_y) in self.__hist:
            self._find_random()
        else:
            self.__hist.append((min_x, min_y))
            if len(self.__hist) > 3:
                self.__hist.pop(0)
            super().update(min_x, min_y)
        
        return False

        
    def _find_random(self):
        self.__hist = []
        while 0 in self.__searched:
            rand_x = randint(0, self.__field_size[0]-1)
            rand_y = randint(0, self.__field_size[1]-1)
            if self.__searched[rand_x, rand_y] == 0:
                break
        self.__temp_goal = (rand_x, rand_y) 

    def __cost(self, pos):
        goal = self.__temp_goal
        if self.__searched[pos] == -1:
            return inf
        if goal == pos:
            return 0

        del_x = abs(pos[0] - goal[0])
        del_y = abs(pos[1] - goal[1])

        if self.__searched[pos] == 1:
            offset = self.__offset_size
        else:
            offset = 0
        return pow( pow(del_y, 2) + pow(del_x, 2) , 0.5) + offset


    def recieveSearched(self, searched):
        for i in range(self.__field_size[0]):
            for j in range(self.__field_size[1]):
                if searched[i, j] != 0 and self.__searched[i, j] == 0:
                    self.__searched[i, j] = searched[i, j]


if __name__ == "__main__":
    d = RandomSearchDrone(1, 2, (5,6))
    d.update([[None for i in range(5)] for j in range(5)])

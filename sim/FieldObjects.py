from abc import ABC, abstractmethod
import random   # For randomly moving drones

### abstract class for all objects that exist on the simulation field
class FieldObject:
    def __init__(self, pos_x, pos_y, symbol="O"):
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__symbol = symbol

    def getX(self):
        return self.__pos_x

    def setX(self, pos_x):
        self.__pos_x = pos_x

    def getY(self):
        return self.__pos_y

    def setY(self, pos_y):
        self.__pos_y = pos_y

    def getPos(self):
        return self.__pos_x, self.__pos_y
    
    def setSymbol(self, symbol):
        self.__symbol = symbol

    def __str__(self):
        return self.__symbol

    def __repr__(self):
        return self.__symbol
    

class Drone(FieldObject, ABC):
    """ 
    Abstract base class for drones
    """
    def __init__(self, pos_x, pos_y, show_dir=False, orientation=0):
        super().__init__(pos_x, pos_y, "*")
        self.__show_dir = show_dir
        self.__char_lst = ['^', '>', 'v', '<']
        self.__orientation = orientation

    ## Abstract update method must be implimented in base classes
    ## using super().update(x, y) will update the position of the drone
    @abstractmethod
    def update(self, pos_x, pos_y):
        super().setX(pos_x)
        super().setY(pos_y)

    def __str__(self):
#        if self.__show_dir:
#            return self.__char_lst[self.__orientation]
        return super().__str__()
    
    def __repr__(self):
        return self.__str__()

    #orientation can be implimented in child classes if wanted
    def setOrientation(self, orientation):
        self.__orientation = orientation % 4

    def right(self):
        self.__orientation += 1
        self.__orientation %= 4

    def left(self):
        self.__orientation -= 1
        self.__orientation %= 4


class SimpleDrone(Drone):
    def __init__(self, position:tuple,  drone_number:int, num_drones:int, field_size:tuple, show_dir=False, orientation=0):
        super().__init__(position[0], position[1], show_dir, orientation)
        self.__my_num = drone_number
        self.__searched = [] # list of searched columns in row
        self.__field_size = field_size 
        self.__row_idx = 0
        start_row = (field_size[0] // num_drones) * drone_number #some start row
        end_row = (field_size[0] // num_drones) * (drone_number + 1) - 1 if drone_number != num_drones - 1 \
                else field_size[0] - 1
        print("drone " + str(drone_number) + ": " + str(start_row) + ", " + str(end_row))
        self.__my_rows = [name for name in range(start_row, end_row + 1)]
        self.__initialized = position[0] == self.__my_rows[0]
        self.__in_obstacle_avoidance = False
        self.__orientation = 1
        self.__rows_jumped = 0
        self.__avoid_direction = 1
        self.__just_stepped = True

    ## example of how to use 
    def update(self, field):    #update will be passed a copy of the field
        x, y = super().getPos() #get the current position
        # print("starting x,y: " + str(x) + ", " + str(y))
        # get to first row of my rows
        if not self.__initialized: 
            x = x + 1 
            self.__initialized = x == self.__my_rows[0]
        else: 
            # search through columns
            # check that next possible move is in bounds
            if y + self.__orientation != -1 and y + self.__orientation != self.__field_size[1]:
                if isinstance(field[x][y + self.__orientation], Obstacle):
                    # if there is an obstacle, try increasing row to get around it
                    # if above doesn't work try decreasing row
                    self.__in_obstacle_avoidance = True

                    if self.__row_idx == len(self.__my_rows) - 1 or x == self.__field_size[0] - 1 or isinstance(field[x+1][y], Obstacle):
                        self.__avoid_direction = -1

                    if self.__avoid_direction == -1 and isinstance(field[x-1][y], Obstacle):
                        return # don't update position. We failed here

                    self.__row_idx += self.__avoid_direction
                    self.__rows_jumped += 1
                    x = self.__my_rows[self.__row_idx]
                    # else
                        # backtrack
                elif isinstance(field[x][y + self.__orientation], Goal):
                    self.setSymbol("X")
                else: # if we can go to the next cell, fucking do it
                    if not self.__in_obstacle_avoidance:
                        y = y + self.__orientation
                    else:
                        if self.__rows_jumped != 0 and not isinstance(field[x - self.__avoid_direction][y], Obstacle) and not self.__just_stepped:
                            self.__rows_jumped -= 1
                            x -= self.__avoid_direction
                            self.__row_idx -= self.__avoid_direction
                        else:
                            y = y + self.__orientation
                        self.__in_obstacle_avoidance = self.__rows_jumped != 0
                        self.__just_stepped = False
            else:
                self.__orientation *= -1 
                # assuming that there are no obstacles on the edges for now
                self.__row_idx += 1
                if self.__row_idx < len(self.__my_rows):
                    x = self.__my_rows[self.__row_idx]
                else:
                    # search failed. Just leave y where it was before
                    _,y = super().getPos()

        # print("new x,y: " + str(x) + "," + str(y))
        super().update(x, y)    #use super().update to set the new x and y positions in the class

### Goal class
class Goal(FieldObject):
    def __init__(self, pos_x, pos_y, symbol="G"):
        super().__init__(pos_x, pos_y, symbol)


### Obstacle class
class Obstacle(FieldObject):
    def __init__(self, pos_x, pos_y, symbol="#"):
        super().__init__(pos_x, pos_y, symbol)

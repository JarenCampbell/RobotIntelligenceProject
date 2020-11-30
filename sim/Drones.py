from FieldObjects.py import FieldObject, Drone
import random   # For randomly moving drone

### example class for drone abstract base class
class TestDrone1(Drone):
    def __init__(self, pos_x, pos_y, show_dir=False, orientation=0):
        super().__init__(pos_x, pos_y, show_dir, orientation)

    ## example of how to use 
    def update(self, field):    #update will be passed a copy of the field
        x, y = super().getPos() #get the current position 
        x += 1                  #modify the current position as needed
        super().update(x, y)    #use super().update to set the new x and y positions in the class




### example class for drone abstract base class
class TestDrone2(Drone):
    def __init__(self, pos_x, pos_y, show_dir=False, orientation=0):
        super().__init__(pos_x, pos_y, show_dir, orientation)

    ## example of how to use 
    def update(self, field):    #update will be passed a copy of the field
        x, y = super().getPos() #get the current position 
        x += 1                  #modify the current position as needed
        y += 2
        super().update(x, y)    #use super().update to set the new x and y positions in the class

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

### Drone will move randomly
class RandomMovementDrone(Drone):
    def __init__(self, pos_x, pos_y, show_dir=False, orientation=0):
        super().__init__(pos_x, pos_y, show_dir, orientation)

    ## example of how to use 
    def update(self, field):    #update will be passed a copy of the field
        x, y = super().getPos() #get the current position 

        randX = random.randint(-1, 1)
        randY = random.randint(-1, 1)

        attemptedPosition = field[x + randX][y + randY]

        # If the random direction has an obstacle or drone, try another random direction
        while isinstance(attemptedPosition, Obstacle) or isinstance(attemptedPosition, Drone):
            randX = random.randint(-1, 1)
            randY = random.randint(-1, 1)
        
        # Case where goal is found
        if isinstance(field[x + randX][y + randY], Goal):
            self.setSymbol("X")
        else:
            super.update(x + randX, y + randY)
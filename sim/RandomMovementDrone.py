from FieldObjects import Drone, Obstacle, Goal
import random

### Drone will move randomly
class RandomMovementDrone(Drone):
    def __init__(self, pos_x, pos_y, show_dir=False, orientation=0):
        super().__init__(pos_x, pos_y, show_dir, orientation)

    ## example of how to use 
    def update(self, field):    #update will be passed a copy of the field
        x, y = super().getPos() #get the current position 

        


        possible_moves = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for newX, newY in possible_moves:
            if newX < 0 or newX >= len(field) or newY < 0 or newY >= len(field[0]):
                continue
            if isinstance(field[newX][newY], Goal):
                self.setSymbol("X")
                return True

        finalX = x
        finalY = y
        good_move = False

        while not good_move and len(possible_moves) > 0:
            chosen_move = random.randint(0, len(possible_moves) - 1)
            newX, newY = possible_moves[chosen_move]

            if newX < 0 or newX >= len(field) or newY < 0 or newY >= len(field[0]):
                possible_moves.pop(chosen_move)
            
            # elif isinstance(field[newX][newY], Goal):
            #     self.setSymbol("X")
            #     return True

            elif self.checkForDrones(field, x, y, newX, newY) or isinstance(field[newX][newY], Obstacle):
                possible_moves.pop(chosen_move)

            else:
                finalX = newX
                finalY = newY
                good_move = True
        
        super().update(finalX, finalY)
        return False

    def checkForDrones(self, field, x, y, newX, newY):
        for i in range(newX - 1, newX + 2):
            for j in range(newY - 1, newY + 2):
                if i == x and j == y:
                    continue
                if i < 0 or i >= len(field) or j < 0 or j >= len(field[0]):
                    continue
                if isinstance(field[i][j], (Drone)):
                    return True
        
        return False
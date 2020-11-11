from abc import ABC, abstractmethod

### base class for all objects that exist on the simulation field
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
    

### Goal class
class Goal(FieldObject):
    def __init__(self, pos_x, pos_y, symbol="G"):
        super().__init__(pos_x, pos_y, symbol)


### Obstacle class
class Obstacle(FieldObject):
    def __init__(self, pos_x, pos_y, symbol="#"):
        super().__init__(pos_x, pos_y, symbol)


### Abstract base class for all drones
class Drone(FieldObject, ABC):
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
        if self.__show_dir:
            return self.__char_lst[self.__orientation]
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


### Test program for above code
if __name__ == "__main__":
    # fo = FieldObject(2, 3)
    # g = Goal(3, 4)
    # o = Obstacle(1, 2)
    # print(o)
    # o.setSymbol("X")
    # print(o)
    # print(fo)
    # print(g)
    td = TestDrone1(1, 5)
    print(td.getPos())
    for i in range(5):
        td.update(field=None)
        print(td.getPos())
    
    print()

    td2 = TestDrone2(2, 2)
    print(td2.getPos())
    for i in range(5):
        td2.update(field=None)
        print(td2.getPos())
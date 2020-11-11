class FieldObject:
    def __init__(self, pos_x, pos_y):
        self.__pos_x = pos_x
        self.__pos_y = pos_y

    def getX(self):
        return self.__pos_x

    def getY(self):
        return self.__pos_y

    def __str__(self):
        return "O"

    def __repr__(self):
        return "O"
    
class Goal(FieldObject):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
    
    def __str__(self):
        return "G"
    
    def __repr__(self):
        return "G"


class Obstacle(FieldObject):
    def __init__(self, pos_x, pos_y, symbol="#"):
        super().__init__(pos_x, pos_y)
        self.__symbol = symbol

    def setSymbol(self, symb):
        self.__symbol = symb

    def __str__(self):
        return self.__symbol
    
    def __repr__(self):
        return self.__symbol

class Drone(FieldObject):
    def __init__(self, pos_x, pos_y, show_dir=False, orientation=0):
        super().__init__(pos_x, pos_y)
        self.__show_dir = show_dir
        self.__char_lst = ['^', '>', 'v', '<']
        self.__orientation = orientation

    def __str__(self):
        if self.__show_dir:
            return self.__char_lst[self.__orientation]
        return "*"
    
    def __repr__(self):
        return self.__str__()

    def setOrientation(self, orientation):
        self.__orientation = orientation % 4

    def right(self):
        self.__orientation += 1
        self.__orientation %= 4

    def left(self):
        self.__orientation -= 1
        self.__orientation %= 4

if __name__ == "__main__":
    fo = FieldObject(2, 3)
    g = Goal(3, 4)
    print(fo)
    print(g)
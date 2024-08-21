from copy import deepcopy

class Box:
    def __init__(self, x, y):
        self.coordinates = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
        
        self.XY = (x, y)

        # lines
        self.TopLine = (self.coordinates[0], self.coordinates[1])
        self.LeftLine = (self.coordinates[0], self.coordinates[2])
        self.RightLine = (self.coordinates[1], self.coordinates[3])
        self.BottomLine = (self.coordinates[2], self.coordinates[3])
        # lines 
        self.lines = [self.TopLine, self.LeftLine, self.RightLine, self.BottomLine]

        # lines connection indicator 
        self._top = False
        self._left = False
        self._right = False
        self._bottom = False

        self.owner = None
        self.completed = False

        self.value = 1

    def connect(self, coordinates):
        line = coordinates
        success = False

        if line not in self.lines:
            return False
        
        if line == self.TopLine and self._top is False:
            self._top = True
            success = True
        elif line == self.LeftLine and self._left is False:
            self._left = True
            success = True
        elif line == self.RightLine and self._right is False:
            self._right = True
            success = True
        elif line == self.BottomLine and self._bottom is False:
            self._bottom = True
            success = True

        if self._top == True and self._bottom == True and self._left == True and self._right == True:
            self.completed = True
        
        return success

    def un_connect(self, coordinates):
        line = coordinates
        if line in self.lines:
            self.completed = False
            # self.owner = None

        if line == self.TopLine:
            self._top = False
        elif line == self.LeftLine:
            self._left = False
        elif line == self.RightLine:
            self._right = False
        elif line == self.BottomLine:
            self._bottom = False

        
    def copy(self):
        return deepcopy(self)
    
    def _repr_pretty_(self, p, cycle):
        if cycle:
            pass

        if self._top:
            p.text("*---*")
        else:
            p.text("*   *")
        p.break_()
        if self._left:
            p.text("|")
        else:
            p.text(" ")
        
        if self.completed:
            p.text(f" {self.owner} ")
        else:
            p.text("   ") 

        if self._right:
            p.text("|")

        p.break_()

        if self._bottom:
            p.text("*---*")
        else:
            p.text("*   *")


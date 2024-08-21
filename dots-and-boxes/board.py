from box import Box
from collections import deque
from copy import deepcopy

class Board:
    display_single_box = False

    def __init__(self, m, n):
        self.player_score = 0
        self.ai_score = 0
        self.m = m
        self.n = n
        self._boxes = self._generate_boxes(m, n)
        self._open_vectors = self._generate_vectors(m, n)
        self._moves = []

    def _generate_boxes(self, rows, cols):
        """
        This function generates the boxes of the board
        """
        boxes = [[Box(x, y) for x in range(cols)] for y in range(rows)]

        return boxes
    
    def _generate_vectors(self, m, n):
        '''
        The vectors represent the available moves, or lines, which can
        be played on a game board of m rows and n columns. These are stored as tuples
        containing each coordinate and are stored in a queue. The vector queue, along
        with the list of boxes that correspond to the coordinates, are used to represent
        game state.
        Vector format: ((x1, y1), (x2, y2)).

        The vectors always point away from the origin (0, 0), so moving like (1, 0) => (0, 0)
        is not a valid move while (0, 0) => (1, 0) is a valid move
        '''
        vectors = set()
        for i in range(0, m + 1):
            for j in range(0, n):
                # Adding horizontal line vectors
                vectors.add(((j, i), (j + 1, i)))
                # Adding vertical line vectors if not in the last row
                if i < m:
                    vectors.add(((j, i), (j, i + 1)))
            # Adding the vertical line for the last column in the current row
            if i < m:
                vectors.add(((n, i), (n, i + 1)))
        return vectors

    def move(self, coordinates, player_move: bool = False):
        player = "P" if player_move == True else "A"
        
        if coordinates not in self._open_vectors:
            return False
        
        self._open_vectors.remove(coordinates)
        self._moves.append(coordinates)
        closed = self._checkboxes(coordinates, player)
            # print("board: moved")
        return closed
    
    def undo_last_move(self):
        if self._moves:
            move = self._moves.pop()
            for i in range(0, self.m):
                for j in range(0, self.n):
                    box = self._boxes[i][j]
                    if move in box.lines:
                        if box.completed is True:
                            if box.owner == "P":
                                self.player_score -= 1
                            else:
                                self.ai_score -= 1
                            box.owner = None
                        box.un_connect(move)                
        
    def has_moves(self):
        # return len(self._open_vectors) != 0
        return bool(self._open_vectors)

    def get_available_moves(self):
        return self._open_vectors
        
    def _checkboxes(self, coordinates, player: str):
        closed = None
        for i in range(self.m):
            for j in range(self.n):
                box = self._boxes[i][j]
                if coordinates in box.lines:
                    box.connect(coordinates)
                if box.completed == True and box.owner == None:
                    box.owner = player
                    if player == "P":
                        self.player_score += 1
                    else:
                        self.ai_score += 1
                    closed = True
        return closed

    
    def copy(self):
        return deepcopy(self)

    def display_board(self):
        # Display player scores
        print(f"Player 1: {self.player_score}")
        print(f"Player AI: {self.ai_score}\n")

        # Display the board
        for i in range(self.m):
            # Top line of each row
            top_line = "   "  # Start with some spacing for alignment
            middle_line = "   "  # Line below to display vertical lines and boxes
            
            for j in range(self.n):
                # Dot
                top_line += "*"

                # Horizontal line
                if ((j, i), (j + 1, i)) in self._moves:
                    top_line += "---"
                else:
                    top_line += "   "
                
                # Vertical line and box
                if ((j, i), (j, i + 1)) in self._moves:
                    middle_line += "|"
                else:
                    middle_line += " "
                
                # Box ownership
                if self._boxes[j][i].completed:
                    middle_line += f" {self._boxes[j][i].owner} "
                else:
                    middle_line += "   "
            
            # Last dot on the right end of the row
            top_line += "*"
            if ((self.n, i), (self.n, i + 1)) in self._moves:
                middle_line += "|"
            else:
                middle_line += " "
            
            # Print the top line and the middle line
            print(top_line)
            print(middle_line)

        # Bottom line of the last row
        bottom_line = "   "
        for j in range(self.n):
            bottom_line += "*"
            if ((j, self.m), (j + 1, self.m)) in self._moves:
                bottom_line += "---"
            else:
                bottom_line += "   "
        bottom_line += "*"
        
        # Print the bottom line
        print(bottom_line)
        print("")  # New line for spacing
    
    def _repr_pretty_(self, p, cycle):
        if (cycle):
            pass

        # Display player scores
        # p.text(f"    AI Score : {self.aiScore}\n")
        # p.text(f"Player Score : {self.playerScore}\n")

        if Board.display_single_box:
            self.__display_single_box(p)
        else:
            self.__display_multi_box(p)
        
    def __display_single_box(self, p):
        last_line = ""
        for i in range(self.m - 1):
            top_line = "\t*"
            middle_line = "\t"
            last_line = "\t*"

            for j in range(self.n):
                box = self._boxes[i][j]
                top_line += "---*" if box._top else "   *"
                middle_line += "|" if box._left else " "
                if box.completed:
                    middle_line += f" {box.owner} "
                else:
                    middle_line += "   "
                last_line += "---*" if box._bottom else "   *"

            
            if box and box._right:
                middle_line += "|"
            
            p.text(top_line)
            p.break_()
            p.text(middle_line)
            p.break_()

        p.text(last_line)
        p.break_()
    
    def __display_multi_box(self, p):
        for i in range(self.m):
            top_line = "\t"
            middle_line = "\t"
            bottom_line = "\t"

            for j in range(self.n):
                box = self._boxes[i][j]
                top_line += "*---*" if box._top else "*   *"
                middle_line += "|" if box._left else " "
                if box.completed:
                    middle_line += f" {box.owner} "
                else:
                    middle_line += "   "
                middle_line += "|" if box._right else " "
                bottom_line += "*---*" if box._bottom else "*   *"
            
            p.text(top_line)
            p.break_()
            p.text(middle_line)
            p.break_()
            p.text(bottom_line)
            p.break_()
            

import numpy as np
import globals as g

class Sokoban:
    board = np.array((0,0))
    playerPosition = (0,0) #(y,x)
    goals = list()
    completed = False
    moveHistory= ''
    
    def __init__(self, board):
        self.board = board
        #find the player position and replace with an empty tile
        #find storage and replace with empty tiles
        #boxes remain the same
        for y in range(board.shape[0]):
            for x in range(board.shape[1]):
                if(board[y][x] == g.PLAYER_LOCATION):
                    self.playerPosition = (y,x)
                    board[y][x] = g.EMPTY
                if(board[y][x] == g.STORAGE):
                    board[y][x] = g.EMPTY
                    self.goals.append((y,x))

    def emptyPosition(self, position):
        return (self.board[position[0]][position[1]] == g.EMPTY)

    def movePlayer(self, direction):
        newPos = list(self.playerPosition)
        newBoxPos = list(self.playerPosition)
        if direction == g.DOWN:
            newPos[0] += 1
            newBoxPos[0] +=2
            move = 'D'
        if direction == g.UP:
            newPos[0] -= 1
            newBoxPos[0] -=2
            move = 'U'
        if direction == g.LEFT:
            newPos[1] -= 1
            newBoxPos[1] -=2
            move = 'L'
        if direction == g.RIGHT:
            newPos[1] += 1
            newBoxPos[1] +=2
            move = 'R'

        if self.emptyPosition(newPos):
            self.playerPosition = tuple(newPos)
            self.moveHistory += move
            return True
        if(self.board[newPos[0]][newPos[1]] == g.WALL):
            return False
        if(self.board[newPos[0]][newPos[1]] == g.BOXES):
            if self.emptyPosition(newBoxPos):
                self.playerPosition = tuple(newPos)
                self.board[newPos[0]][newPos[1]] = g.EMPTY
                self.board[newBoxPos[0]][newBoxPos[1]] = g.BOXES
                if self.boxesRemaining() == 0:
                    self.completed = True
                self.moveHistory += move           
                return True
            return False
        #I should throw Exception here
        return False
    
    def boxesRemaining(self):
        boxes = len(self.goals)
        for y, x in self.goals:
            if self.board[y][x] == g.BOXES:
                boxes -=1
        return boxes

    def printBoard(self):
        temp = self.board.tolist()
        for i in range(len(temp)):
            for j in range (len(temp[0])):
                if temp[i][j] == 0:
                    temp[i][j] = ' '
                if temp[i][j] == 1:
                    temp[i][j] = '|'
        for element in self.goals:
            if( temp[element[0]][element[1]] != g.BOXES):
                temp[element[0]][element[1]] = '_'
        temp[self.playerPosition[0]][self.playerPosition[1]] = 'P'
        for line in temp:
            for elem in line:
                print(elem, end='')
            print()
        print()

    def autoMove(self, moves):
        print("Beginning Auto Move")
        for i,v in enumerate(moves):
            print(v,end="")
            if v == 'U':
                self.movePlayer(g.UP)
            if v == 'D':
                self.movePlayer(g.DOWN)
            if v == 'L':
                self.movePlayer(g.LEFT)
            if v == 'R':
                self.movePlayer(g.RIGHT)
        print("\n\nAuto move finished")
            

    @staticmethod
    def readFile(inputLocation: str):
        try:
            with open(inputLocation, "r") as f:
                inputLines = [i.strip() for i in f.readlines()]
        except FileNotFoundError:
            print("Error Accessing File")
            return
        input_split = list()
        for line in inputLines:
            row = list()
            for num in line.split():
                row.append(int(num))
            input_split.append(row)  

        WALL = g.WALL
        BOXES =  g.BOXES
        STORAGE = g.STORAGE
        PLAYER_LOCATION = g.PLAYER_LOCATION
        try:
            sokoban_board = np.zeros( (input_split[0][0], input_split[0][1]), dtype=int )
            # print("\nwall")
            for i in range(1, 2*(input_split[WALL][0]) + 1, 2):
                y = input_split[WALL][i] - 1
                x = input_split[WALL][i+1] - 1
                # print(f"x{x},y{y}")
                sokoban_board[y][x] = WALL

            # print("\nboxes")
            for i in range(1, 2*(input_split[BOXES][0]) + 1, 2):
                y = input_split[BOXES][i] - 1
                x = input_split[BOXES][i+1] - 1
                # print(f"x{x},y{y}")
                sokoban_board[y][x] = BOXES

            # print("\nstorage")
            for i in range(1, 2*(input_split[STORAGE][0]) + 1, 2):
                y = input_split[STORAGE][i] - 1 
                x = input_split[STORAGE][i+1] - 1
                # print(f"x{x},y{y}")
                sokoban_board[y][x] = STORAGE 

            y = input_split[PLAYER_LOCATION][0] - 1
            x = input_split[PLAYER_LOCATION][1] - 1
            sokoban_board[y][x] = PLAYER_LOCATION

        except Exception as E:
            print(f"Error converting to np array\n{E}")

        return sokoban_board
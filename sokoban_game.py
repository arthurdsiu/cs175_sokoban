import numpy as np
import globals as g

class Sokoban:
    board = np.array((0,0))
    playerPosition = (0,0) #(y,x)
    goals = list()
    completed = False
    
    def __init__(self, board):
        self.board = board
        #find the player position and replace with an empty tile
        #find storage and replace with empty tiles
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
        if direction == g.UP:
            newPos[0] -= 1
            newBoxPos[0] -=2
        if direction == g.LEFT:
            newPos[1] -= 1
            newBoxPos[1] -=2
        if direction == g.RIGHT:
            newPos[1] += 1
            newBoxPos[1] +=2

        if self.emptyPosition(newPos):
            self.playerPosition = tuple(newPos)
            return True
        if(self.board[newPos[0]][newPos[1]] == g.WALL):
            return False
        if(self.board[newPos[0]][newPos[1]] == g.BOXES):
            if self.emptyPosition(newBoxPos):
                self.playerPosition = tuple(newPos)
                self.board[newPos[0]][newPos[1]] = g.EMPTY
                self.board[newBoxPos[0]][newBoxPos[1]] = g.BOXES
                print(self.board)
                if self.boxesRemaining() == 0:
                    self.completed = True        
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

    
import numpy as np
import globals as g
import time
import sokoban_game

'''This class detects deadlocks. Grids that are deadzone will be marked
with g.DEADLOCK'''
class Deadlock:
    deadlockMarked = np.array((0,0))
    goals = list()

    def __init__(self, nparray, goals):
        self.deadlockMarked = nparray
        self.goals = goals
        for goal in self.goals:
            #update the goals
            goal = 0

    def pull():
        return

    def deadlockList(self):
        return

'''Solves a sokoban boad through dfs'''
class AI:
    deadlock = None
    board = np.zeros((0,0))
    startLocation = None
    goals = None
    path = str
    
    def __init__(self, nparray):
        game = sokoban_game.Sokoban(nparray)
        self.board =  game.board
        self.startLocation = game.playerPosition
        self.goals = game.goals
        deadlock = Deadlock(self.board, self.goals)

    def dfsSolver(self):
        self.startTime = time.time()
        #clear out visited array
        #initilize state to starting board state
        solved = self.dfs()
        if solved:
            return self.path
        return None

    def dfs(self):
        if time.time() - self.startTime  > g.TIME_LIMIT:
            return False
        if self.finished():
            return True
        #generate frontier
        
    def finished(self):
        return None

    def generateAllMoves(self, position, board):
        #find connected whitespace
        cur = position
        visited = np.zeros((board.shape))
        connectedSpace = list()
        boxes = list()
        visitedBoxes = np.zeros((board.shape))

        def isValidConnectedSpace(cur):
            if 0 < cur[0] <= board.shape[0] and 0 < cur[1] <= board.shape[1]:
                if board[cur[0]][cur[1]] == g.BOXES:
                    if visitedBoxes[cur[0]][cur[1]]:
                        return False
                    boxes.append(cur) # add the box we encountered into the frontier
                    visitedBoxes[cur[0]][cur[1]] = 1
                    return False
                if board[cur[0]][cur[1]] == g.EMPTY:
                    return True 
                if board[cur[0]][cur[1]] == g.STORAGE:
                    return True
            return False

        def visit(curTile):
            possible_neighbors = self.getNeigbors(curTile)
            for i in possible_neighbors:
                if not visited[i[0]][i[1]] and isValidConnectedSpace(i):
                    connectedSpace.append(i)
                    visited[i[0]][i[1]]=1
                    visit(i)

        def isEmpty(tile):
            if board[tile[0]][tile[1]] == g.EMPTY:
                return True
            return False

        if(isValidConnectedSpace(cur)):
            connectedSpace.append(cur)
            visited[cur[0]][cur[1]]=1
        visit(cur)

        #return boxes
        #found all connected space
        #now we need to find all neighboring boxes of the connected space
        pushable = [] #check whether box can be pushed
        pushVisited = np.zeros((board.shape[0],board.shape[1],4))
        for box in boxes:
            neighbors = self.getNeigbors(box)
            print(f"Box{box} neribors:{neighbors}")
            opposite = [1,0,3,2]
            for i,n in enumerate(neighbors):
                print(f"neigbor:{n}, visited: {visited[n[0]][n[1]]}, oppositEmpty: {isEmpty(neighbors[opposite[i]])}")
                if pushVisited[n[0]][n[1]][opposite[i]]:
                        continue
                if visited[n[0]][n[1]] and isEmpty(neighbors[opposite[i]]):
                    n.append(opposite[i])
                    pushable.append(n)
                    pushVisited[n[0]][n[1]][[opposite[i]]]=1  
        return pushable

    def getNeigbors(self, tile):
        #up, down, left, right
        return [[tile[0]+1, tile[1]], [tile[0]-1, tile[1]], [tile[0], tile[1]-1], [tile[0], tile[1]+1]]
    
if __name__ == '__main__':
    file = "sokoban01.txt"
    ai =AI((sokoban_game.Sokoban.readFile(file)))
    locations =  ai.generateAllMoves(ai.startLocation, ai.board)
    print(f"start location:{ai.startLocation}")
    output = ai.board.tolist()
    for loc in locations:
        print(loc)
        output[loc[0]][loc[1]] = '.'
    output[ai.startLocation[0]][ai.startLocation[1]] = 'P'
    for i in output:
        for j in i:
            if j != 0:
                print(j,end="")
            else:
                print(" ",end="")
        print()



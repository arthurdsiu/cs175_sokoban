import numpy as np
import globals as g
import time
import sys
import copy
from collections import deque
from sokoban_game import Sokoban
from BitVector import BitVector


'''Solves a sokoban boad through dfs'''
class AI:
    '''This class detects deadlocks. Grids that are deadzone will be marked
    with g.DEADLOCK'''
    class Deadlock:
        deadlockByGoals = np.array((0,0))
        deadlockMarked = np.array((0,0))
        counterHash = np.array((0,0))
        hashNameToBoxLimitCount = list()

        def __init__(self, board, goals):
            self.deadlockByGoals = np.ones((len(goals), board.shape[0], board.shape[1]), dtype=bool)
            self.deadlockMarked = np.ones((board.shape[0], board.shape[1]), dtype=bool)
            self.counterHash = np.zeros((board.shape[0], board.shape[1]), dtype=int)
            
            def pull(next, cur, goalIndex):
                testFrom = [next[0] + next[0] - cur[0], next[1] + next[1] - cur[1]]

                if not 0 <= testFrom[0] < board.shape[0] or not 0 <= testFrom[1] < board.shape[1]:
                    return
                '''
                0  1 -> 01
                0 -1 -> 00
                1  0 -> 10
                -1 0 -> 11
                '''
                # if next[0] - cur[0] < 0: or no movement
                direction = 0
                if next[0] - cur[0] > 0:
                    direction = 1
                if next[1] - cur[1] > 0:
                    direction = 2
                if next[1] - cur[1] < 0:
                    direction = 3
            
                # print(f"direction{direction}")

                if visited[next[0]][next[1]][direction] == True:
                    return
                else:
                    visited[next[0]][next[1]][direction] = True

                if board[next[0]][next[1]] == g.WALL:
                    return

                if board[testFrom[0]][testFrom[1]] == g.WALL:
                    #print(f"deadlock found: cur{cur} next{next} testFrom {testFrom} goalIndex{goalIndex}")
                    #printDeadlockBoard(board, self.deadlockByGoals[goalIndex], cur)
                    return
                
                self.deadlockByGoals[goalIndex][next[0]][next[1]] = False # mark that deadlock doesn't exist

                # print(f"good tile found: cur{cur} next{next} testFrom {testFrom} goalIndex{goalIndex}")
                # printDeadlockBoard(board, self.deadlockByGoals[goalIndex], testFrom)
                neighbors = getNeigbors(board, next)
                for n in neighbors:
                    if n != None: 
                        pull(n, next, goalIndex)

            for i, goal in enumerate(goals):
                visited = np.zeros((board.shape[0], board.shape[1], 4), dtype=bool)
                pull(goal, goal, i)
            
            # generate a simple deadlock table
            for grid in self.deadlockByGoals:
                for i,x in enumerate(grid):
                    for j,y in enumerate(x):
                        if self.deadlockMarked[i][j] == True and y == False:
                            self.deadlockMarked[i][j] = False
            # generate a count table
            for grid in self.deadlockByGoals:
                for i,x in enumerate(grid):
                    for j,y in enumerate(x):
                        if y == False:
                            self.counterHash[i][j]+=1
            # convert count table to hash by region
            # a region is a cell with a limit and all reachable neigbors with the same limit
            # store each region's name and limit in separate list

            visited = np.zeros(self.counterHash.shape, dtype=bool)

            def labelCountToHash(curMove, boxLimit, name, visited):
                if visited[curMove[0]][curMove[1]]:
                    return # visited already
                if self.counterHash[curMove[0]][curMove[1]] != boxLimit:
                    return # wrong area, reachable box count doesn't match
                visited[curMove[0]][curMove[1]] = True
                

                self.counterHash[curMove[0]][curMove[1]] = name # [i][j]aka hash -> name

                for nextMove in getNeigbors(board, curMove):
                    if nextMove:
                        labelCountToHash(nextMove, boxLimit, name, visited) # visit all neigbors
                return boxLimit

            # Mark all deadlock cells first. 0 is their capacity. We'll use it as their name as well
            for i in range(self.counterHash.shape[0]):
                for j in range(self.counterHash.shape[1]):
                    if self.counterHash[i][j] == 0: 
                        visited[i][j] = True

            # Name cells starting at 1
            # cells named 0 represent deadlock cells with 0 box limit
            self.hashNameToBoxLimitCount.append(0)
            name = 1
            for i in range(self.counterHash.shape[0]):
                for j in range(self.counterHash.shape[1]):
                    if visited[i][j]:
                        continue # skip over deadlock cells and cells we've named already
                    boxLimit = self.counterHash[i][j]
                    self.hashNameToBoxLimitCount.append(boxLimit) # record the number of boxes
                    labelCountToHash([i,j], boxLimit, name, visited) # replace number of boxes with name instead
                    
                    name+=1 # or name = len(hashToLimit)

            # debuggging
            # for i, table in enumerate(self.deadlockByGoals):
            #     print(f"\ngoal {i} deadlock table")
            #     printDeadlockBoard(board, table, goals[i])
            # print("\ncompiled deadlock table")
            # printDeadlockBoard(board, self.deadlockMarked, goals[0])
            # print("\ncounter table")
            # output = self.counterHash.tolist()
            # for i in output:
            #     print(i)

        def checkIfCountDeadlock(self, boxCounter, oldBoxPos, newBoxPos):
            oldHash = self.counterHash[oldBoxPos[0]][oldBoxPos[1]]
            newHash = self.counterHash[newBoxPos[0]][newBoxPos[1]]
            if oldHash == newHash:
                return False # box is not moving to a new area
            if boxCounter[newHash] +1 > newHash:
                return True
            return False

    #class variables
    deadlock = None
    board = np.zeros((0,0))
    originalBoard = np.zeros((0,0))
    startPosition = None
    goals = None
    visitedStates = dict()
    time = g.TIME_LIMIT
    failedDueToTimeout = False
    
    def __init__(self, sokoban :Sokoban):
        self.board =  copy.deepcopy(sokoban.board)
        self.originalBoard =  copy.deepcopy(sokoban.board)
        self.startPosition = sokoban.playerPosition
        self.goals = sokoban.goals
        self.deadlock = self.Deadlock(self.board, self.goals)
        self.visitedStates = dict()

    def dfsSolver(self):
        startTime = time.time()
        path = list()
        self.visitedStates = dict()

        # count deadlock box Count
        boxCount = [0] * (len(self.deadlock.hashNameToBoxLimitCount))
        for i, row in enumerate(self.board):
            for j, elem in enumerate(row):
                if elem == g.BOXES:
                    boxCount[self.deadlock.counterHash[i][j]]+=1

        def finished():
            for goal in self.goals:
                if not self.board[goal[0]][goal[1]] == g.BOXES:
                    return False
            return True

        def dfs(newPosition):
            if time.time() - startTime  > g.TIME_LIMIT:
                self.failedDueToTimeout = True
                return False
        
            if finished():
                print("Finished solving")
                return True
            
            moves, normalized = self.generateAllMoves(newPosition, self.board)
            
            # I"m not sure about this
            key = self.getState(self.board, normalized)
            if self.visitedStates.setdefault(key, False):
                # print(f"this is a visited state with move {newPosition}")
                return False
            self.visitedStates[key] = True

            # print(f"Possible moves {moves}")
            # print("self.board state, all possible moves marked with a '.' ")
            # printBoard(self.board,moves, None)

            for move in moves:
                path.append(move)

                def moveBox(ob, nb):
                    self.board[nb[0],nb[1]] = g.BOXES
                    newLimit =  self.deadlock.counterHash[nb[0],nb[1]]
                    oldLimit =  self.deadlock.counterHash[ob[0],ob[1]]
                    boxCount[newLimit]+=1
                    boxCount[oldLimit]-=1
                    self.board[ob[0],ob[1]] = g.EMPTY
                    return ob

                newPos = None
                if move[2] == g.UP and not self.deadlock.checkIfCountDeadlock(boxCount, [move[0]-1,move[1]], [move[0]-2,move[1]]):
                    newPos = moveBox([move[0]-1,move[1]], [move[0]-2,move[1]])
                if move[2] == g.DOWN and not self.deadlock.checkIfCountDeadlock(boxCount, [move[0]+1,move[1]], [move[0]+2,move[1]]):
                    newPos = moveBox([move[0]+1,move[1]], [move[0]+2,move[1]])
                if move[2] == g.LEFT and not self.deadlock.checkIfCountDeadlock(boxCount, [move[0],move[1]-1], [move[0],move[1]-2]):
                    newPos = moveBox([move[0],move[1]-1], [move[0],move[1]-2])
                if move[2] == g.RIGHT and not self.deadlock.checkIfCountDeadlock(boxCount, [move[0],move[1]+1], [move[0],move[1]+2]):
                    newPos = moveBox([move[0],move[1]+1], [move[0],move[1]+2])
                
                if newPos == None: # go next move if deadlock state encountered
                    # print("Deadlock detected")
                    path.pop()
                    continue
                
                # print(f"Box moved {move} \nhere's self.board state")
                # printBoard(self.board,None, newPos)

                if dfs(newPos):
                    return True
                path.pop()

                if move[2] == g.UP:
                    self.board[move[0]-2,move[1]] = g.EMPTY
                    self.board[move[0]-1,move[1]] = g.BOXES
                if move[2] == g.DOWN:
                    self.board[move[0]+2,move[1]] = g.EMPTY
                    self.board[move[0]+1,move[1]] = g.BOXES
                if move[2] == g.LEFT:
                    self.board[move[0],move[1]-2] = g.EMPTY
                    self.board[move[0],move[1]-1] = g.BOXES
                if move[2] == g.RIGHT:
                    self.board[move[0],move[1]+2] = g.EMPTY
                    self.board[move[0],move[1]+1] = g.BOXES

            return False

        if dfs(self.startPosition):
            return path


    '''
    returns a list of moves in [y,x,direction]
    (y,x) is front of a box
    the box will be the new location of the player
    also return the normalized position of the player for
    use it state space based on position parameter passed to 
    '''
    def generateAllMoves(self, position, board):
        # find connected whitespace
        cur = position
        visited = np.zeros((board.shape))
        connectedSpace = list()
        boxes = list()
        visitedBoxes = np.zeros((board.shape))

        def isValidConnectedSpace(cur):
            if cur != None and  0 <= cur[0] < board.shape[0] and 0 <= cur[1] < board.shape[1]:
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
            possible_neighbors = getNeigbors(board, curTile)
            for i in possible_neighbors:
                if isValidConnectedSpace(i) and not visited[i[0]][i[1]]:
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

        minElemY = min(connectedSpace, key=lambda x: x[0])
        normalized = min(filter( lambda x: x[0]== minElemY[0], connectedSpace), key=lambda x: x[1])
        # found all connected space
        # now we need to find all neighboring boxes of the connected space
        pushable = [] #check whether box can be pushed
        
        # print(f"normalized:{normalized}")
        for box in boxes:
            neighbors = getNeigbors(board, box)
            # print(f"Box{box} neribors:{neighbors}")
            # neighbors: up, down, left, right
            opposite = [1,0,3,2]
            for i,n in enumerate(neighbors):
                # print(f"neigbor:{n}, visited: {visited[n[0]][n[1]]}, oppositEmpty: {isEmpty(neighbors[opposite[i]])}")
                if n == None:
                    continue
                if visited[n[0]][n[1]] and neighbors[opposite[i]]!= None and isEmpty(neighbors[opposite[i]]):
                    n[2] = opposite[i] # if n is valid, that there is a box's empty space adjacent,
                    #you're UP, that means you need to push DOWN
                    pushable.append(n)
                    
        #print(pushable)
        return pushable, normalized

    '''
    given some board state with boxes and the player's position,
    return a unique bitVector representation that will represent the state
    of the game
    currently size 6 -> 64 for array
    '''
    def getState(self, board, position):
        bvBox = BitVector(size = 0)
        POSITION_SIZE = 6
        for index, x in np.ndenumerate(board):
            if( x == g.BOXES):
                bvBox = bvBox + BitVector(intVal=1)
            else:
                bvBox = bvBox + BitVector(intVal=0)
        
        bvPos = BitVector(intVal = position[0], size = POSITION_SIZE) + BitVector(intVal = position[1], size = POSITION_SIZE)
        ret = bvBox + bvPos
        ret.pad_from_right(8 -ret.length()%8)
        hexString = ret.get_bitvector_in_ascii()
        return hexString

    '''
    uses BFS to find a path from origin to move
    '''
    def getMoves(self, moveList):
        # print("\nconverting move list to directions on keyboard\n")
        tempBoard =  copy.deepcopy(self.originalBoard)
        ret = str()
        prev = self.startPosition
        for move in moveList:
            path = self.bfsPath(prev, move, tempBoard)
            # print(f"path obtained: {path}")
            ret += path
            ret += numToLetMove(move[2])
            # print(f"Current move History: {ret}")
            if move[2] == g.UP:
                prev = [move[0]-1,move[1]]
                boxLoc = [move[0]-2,move[1]]
            if move[2] == g.DOWN:
                prev = [move[0]+1,move[1]]
                boxLoc = [move[0]+2,move[1]]
            if move[2] == g.LEFT:
                prev = [move[0],move[1]-1]
                boxLoc = [move[0],move[1]-2]
            if move[2] == g.RIGHT:
                prev = [move[0],move[1]+1]
                boxLoc = [move[0],move[1]+2]
            tempBoard[prev[0]][prev[1]]= g.EMPTY
            tempBoard[boxLoc[0]][boxLoc[1]]=g.BOXES
        return ret

    def bfsPath(self, origin, dest, board):
        if origin[0] == dest[0] and origin[1] == dest[1]:
            return  ""
        visited = [[None for i in range(board.shape[1])] for j in range(board.shape[0]) ]
        q = deque()
        visited[origin[0]][origin[1]] = True

        neighbors = getNeigbors(board, origin)
        for n in neighbors:
            if board[n[0]][n[1]] != g.EMPTY or visited[n[0]][n[1]]:
                continue
            else:
                temp = list(origin)
                temp.append(n[2])
                visited[n[0]][n[1]] = temp
                q.append(n)
        
        while(len(q)):
            cur = q.popleft()
            if cur[0] == dest[0] and cur[1] == dest[1]:
                # print(f"Destination from{origin} to {dest} found")
                path = list() # trace back path
                while ( visited[cur[0]][cur[1]] != True):
                    path.append(visited[cur[0]][cur[1]][2]) # get only the direction
                    cur = visited[cur[0]][cur[1]]
                path.reverse()
                ret = str()
                for i in path:
                    ret += numToLetMove(i)
                # print(ret)
                return ret

            neighbors = getNeigbors(board, cur)
            for n in neighbors:
                if board[n[0]][n[1]] != g.EMPTY or visited[n[0]][n[1]]:
                    # print(f"n {n} board: {board[n[0]][n[1]]} and visited: { visited[n[0]][n[1]]}")
                    continue
                else:
                    cur[2] = n[2]
                    visited[n[0]][n[1]] = copy.deepcopy(cur)
                    q.append(n)
                
            if visited[cur[0]][cur[1]] == None:
                continue
        # print("no path found through BFS")
        return ""
            
def getNeigbors(board, tile):
        #up, down, left, right
        ret= []
        ret.append([tile[0] - 1, tile[1], g.UP] if tile[0] - 1 >= 0  else None)
        ret.append([tile[0] + 1, tile[1], g.DOWN] if tile[0] + 1 < board.shape[0] else None)
        ret.append([tile[0], tile[1] - 1, g.LEFT] if tile[1] - 1 >= 0 else None)
        ret.append([tile[0], tile[1] + 1, g.RIGHT] if tile[1] + 1 < board.shape[1] else None)
        return ret

def numToLetMove(i):
    if i == g.UP:
       return 'U'
    if i == g.DOWN:
        return'D'
    if i == g.LEFT:
        return'L'
    if i == g.RIGHT:
        return 'R'

def printBoard(board, potentialMoves, playerLocation):
    output = board.tolist()
    if potentialMoves != None:
        for loc in potentialMoves:
            output[loc[0]][loc[1]] = '.'
    if playerLocation != None:
        output[playerLocation[0]][playerLocation[1]] = 'P'
    for i in output:
        for j in i:
            if j != 0:
                print(j,end="")
            else:
                print(" ",end="")
        print()

def printDeadlockBoard(board, deadlock, playerLocation):
    output = board.tolist()
    for i,x in enumerate(deadlock):
        for j,y in enumerate(x):
            if board[i][j]!= g.WALL and deadlock[i][j]== True:
                output[i][j] = 'X'
    output[playerLocation[0]][playerLocation[1]] = 'P'
    for i in output:
        for j in i:
            if j == 1 or j == 'X' or j == 'P':
                print(j, end="")
            else:
                print(" ", end="")
        print()
    
if __name__ == '__main__':
    fileLoc = None
    # fileLoc= 'maps/3.txt'
    if fileLoc == None:
        if len(sys.argv) == 1:
            fileLoc  = input("Please enter file location: ")
        else:
            fileLoc = sys.argv[1]
    
    ai =AI(Sokoban(fileLoc))
    locations, position =  ai.generateAllMoves(ai.startPosition, ai.board)
    print(f"start location:{ai.startPosition}")
    print("Starting board")
    printBoard(ai.board, None ,ai.startPosition)
    printDeadlockBoard(ai.board,ai.deadlock.deadlockMarked ,ai.startPosition)
    path = ai.dfsSolver()
    try:
        with open("moveHistory.txt", "w") as f:
            for move in path:
                f.write(f"{move}\n")
    except:
        print("Error writing moveHistory file")

    string = ai.getMoves(path)

    try:
        with open("autoMove.txt", "w") as f:
            f.write(f"{string}\n")
    except:
        print("Error writing autoMove file")
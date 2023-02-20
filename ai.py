import numpy as np
import globals as g
import time
import sokoban_game
from BitVector import BitVector


'''Solves a sokoban boad through dfs'''
class AI:
    '''This class detects deadlocks. Grids that are deadzone will be marked
    with g.DEADLOCK'''
    class Deadlock:
        deadlockByGoals = np.array((0,0))
        deadlockMarked = np.array((0,0))

        def __init__(self, board, goals):
            self.deadlockByGoals = np.ones((len(goals), board.shape[0], board.shape[1]), dtype=bool)
            self.deadlockMarked = np.ones((board.shape[0], board.shape[1]), dtype=bool)
            
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
            
                print(f"direction{direction}")

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
                
                self.deadlockByGoals[goalIndex][next[0]][next[1]] = False # mark possible
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
            # debuggging
            for i, table in enumerate(self.deadlockByGoals):
                print(f"\ngoal {i} deadlock table")
                printDeadlockBoard(board, table, goals[i])
            print("\ncompiled deadlock table")
            printDeadlockBoard(board, self.deadlockMarked, goals[0])

    #class variables
    deadlock = None
    board = np.zeros((0,0))
    startPosition = None
    goals = None
    
    def __init__(self, nparray):
        game = sokoban_game.Sokoban(nparray)
        self.board =  game.board
        self.startPosition = game.playerPosition
        self.goals = game.goals
        self.deadlock = self.Deadlock(self.board, self.goals)

    def dfsSolver(self):
        startTime = time.time()
        path = list()
        board = self.board
        visitedStates = dict()

        def finished(board):
            for goal in self.goals:
                if not board[goal[0]][goal[1]] == g.BOXES:
                    return False
            return True        

        def dfs(newPosition):
            if time.time() - startTime  > g.TIME_LIMIT:
                return False

            if finished(board):
                return True
            moves, normalized = self.generateAllMoves(newPosition, board)
            print(f"Possible moves {moves}")
            print("Board state, all possible moves marked with a '.' ")
            printBoard(board,moves, newPosition)
            
            # I"m not sure about this
            key = self.getState(board, normalized)
            if visitedStates.setdefault(key):
                return False
            visitedStates[key] = True

            for move in moves:
                path.append(move)
                if move[2] == g.UP:
                    board[move[0]-2,move[1]] = g.BOXES
                    board[move[0]-1,move[1]] = g.EMPTY
                    newPos = [move[0]-1,move[1]]
                if move[2] == g.DOWN:
                    board[move[0]+2,move[1]] = g.BOXES
                    board[move[0]+1,move[1]] = g.EMPTY
                    newPos =[move[0]+1,move[1]] 
                if move[2] == g.LEFT:
                    board[move[0],move[1]-2] = g.BOXES
                    board[move[0],move[1]-1] = g.EMPTY
                    newPos = [move[0],move[1]-1]
                if move[2] == g.RIGHT:
                    board[move[0],move[1]+2] = g.BOXES
                    board[move[0],move[1]+1] = g.EMPTY
                    newPos = [move[0],move[1]+1]
                print(f"Box moved {move} \nhere's board state")
                printBoard(board,None, newPos)

                if dfs(newPos):
                    return True

                path.pop()
                if move[2] == g.UP:
                    board[move[0]-2,move[1]] = g.EMPTY
                    board[move[0]-1,move[1]] = g.BOXES
                if move[2] == g.DOWN:
                    board[move[0]+2,move[1]] = g.EMPTY
                    board[move[0]+1,move[1]] = g.BOXES
                if move[2] == g.LEFT:
                    board[move[0],move[1]-2] = g.EMPTY
                    board[move[0],move[1]-1] = g.BOXES
                if move[2] == g.RIGHT:
                    board[move[0],move[1]+2] = g.EMPTY
                    board[move[0],move[1]+1] = g.BOXES

            return False

        return dfs(self.startPosition)
    '''
    returns a list of moves in [y,x,direction]
    (y,x) is front of a box
    the box will be the new location of the player
    also return the normalized position of the player for
    use it state space based on position parameter passed to 
    '''
    def generateAllMoves(self, position, board):
        #find connected whitespace
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
        #found all connected space
        #now we need to find all neighboring boxes of the connected space
        pushable = [] #check whether box can be pushed
        
        # print(f"normalized:{normalized}")
        for box in boxes:
            neighbors = getNeigbors(board, box)
            #print(f"Box{box} neribors:{neighbors}")
            opposite = [1,0,3,2]
            for i,n in enumerate(neighbors):
                # print(f"neigbor:{n}, visited: {visited[n[0]][n[1]]}, oppositEmpty: {isEmpty(neighbors[opposite[i]])}")
                if n == None:
                    continue
                if visited[n[0]][n[1]] and neighbors[opposite[i]]!= None and isEmpty(neighbors[opposite[i]]):
                    n.append(opposite[i]) # if n is valid, and you're UP, that means you need to push DOWN
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

def getNeigbors(board, tile):
        #up, down, left, right
        ret= []
        ret.append([tile[0] - 1, tile[1]] if tile[0] - 1 < board.shape[0] else None)
        ret.append([tile[0] + 1, tile[1]] if tile[0] + 1 >= 0 else None)
        ret.append([tile[0], tile[1] - 1] if tile[1] - 1 >= 0 else None)
        ret.append([tile[0], tile[1] + 1] if tile[1] + 1 < board.shape[1] else None)
        return ret
def printBoard(board, potentialMoves, playerLocation):
    output = board.tolist()
    if potentialMoves != None:
        for loc in potentialMoves:
            output[loc[0]][loc[1]] = '.'
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
    file = "sokoban01.txt"
    ai =AI((sokoban_game.Sokoban.readFile(file)))
    locations, position =  ai.generateAllMoves(ai.startPosition, ai.board)
    print(f"start location:{ai.startPosition}")
    print("Starting board")
    printBoard(ai.board, None ,ai.startPosition)
    printDeadlockBoard(ai.board,ai.deadlock.deadlockMarked ,ai.startPosition)
    #print(ai.dfsSolver())



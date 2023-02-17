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
    startPosition = None
    goals = None

    
    def __init__(self, nparray):
        game = sokoban_game.Sokoban(nparray)
        self.board =  game.board
        self.startPosition = game.playerPosition
        self.goals = game.goals
        deadlock = Deadlock(self.board, self.goals)

    def dfsSolver(self):
        startTime = time.time()
        path = list()
        board = self.board

        def finished(board):
            for goal in self.goals:
                if not board[goal[0]][goal[1]] == g.BOXES:
                    return False
            return True        

        def dfs(move):
            if time.time() - startTime  > g.TIME_LIMIT:
                return False

            if finished(board):
                return True
            if move[2] == g.UP:
                position=(move[0]-1,move[1])
            if move[2] == g.DOWN:
                position=(move[0]+1,move[1])
            if move[2] == g.LEFT:
                position=(move[0],move[1]-1)
            if move[2] == g.RIGHT:
                position=(move[0],move[1]+1)

            moves = self.generateAllMoves(position,board)

            for move in moves:
                path.append(move)
                if move[2] == g.UP:
                    board[move[0]+2,move[1]] = g.BOXES
                    board[move[0]+1,move[1]] = g.EMPTY
                if move[2] == g.DOWN:
                    board[move[0]-2,move[1]] = g.BOXES
                    board[move[0]-1,move[1]] = g.EMPTY
                if move[2] == g.LEFT:
                    board[move[0],move[1]-2] = g.BOXES
                    board[move[0],move[1]-1] = g.EMPTY
                if move[2] == g.RIGHT:
                    board[move[0]+2,move[1]+2] = g.BOXES
                    board[move[0]+1,move[1]+1] = g.EMPTY


                if dfs(move):
                    return True

                path.pop()
                if move[2] == g.UP:
                    board[move[0]+2,move[1]] = g.BOXES
                    board[move[0]+1,move[1]] = g.EMPTY
                if move[2] == g.DOWN:
                    board[move[0]-2,move[1]] = g.BOXES
                    board[move[0]-1,move[1]] = g.EMPTY
                if move[2] == g.LEFT:
                    board[move[0],move[1]-2] = g.BOXES
                    board[move[0],move[1]-1] = g.EMPTY
                if move[2] == g.RIGHT:
                    board[move[0]+2,move[1]+2] = g.BOXES
                    board[move[0]+1,move[1]+1] = g.EMPTY
                position = (move[0],move[1])

            return False

        moves = self.generateAllMoves(self.startPosition, board)
        for move in moves:
            if dfs(move):
                return path
        return None
    
    '''
    returns a list of moves in [y,x,direction]
    '''
    def generateAllMoves(self, position, board):
        #find connected whitespace
        cur = position
        visited = np.zeros((board.shape))
        connectedSpace = list()
        boxes = list()
        visitedBoxes = np.zeros((board.shape))

        def isValidConnectedSpace(cur):
            if 0 <= cur[0] < board.shape[0] and 0 <= cur[1] < board.shape[1]:
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

        #return boxes
        #found all connected space
        #now we need to find all neighboring boxes of the connected space
        pushable = [] #check whether box can be pushed
        pushVisited = np.zeros((board.shape[0],board.shape[1],4))
        for box in boxes:
            neighbors = self.getNeigbors(box)
            # print(f"Box{box} neribors:{neighbors}")
            opposite = [1,0,3,2]
            for i,n in enumerate(neighbors):
                # print(f"neigbor:{n}, visited: {visited[n[0]][n[1]]}, oppositEmpty: {isEmpty(neighbors[opposite[i]])}")
                if pushVisited[n[0]][n[1]][opposite[i]]:
                        continue
                if visited[n[0]][n[1]] and isEmpty(neighbors[opposite[i]]):
                    n.append(opposite[i])
                    pushable.append(n)
                    pushVisited[n[0]][n[1]][[opposite[i]]]=1
        print(pushable)

    def getNeigbors(self, tile):
        #up, down, left, right
        return [[tile[0]+1, tile[1]], [tile[0]-1, tile[1]], [tile[0], tile[1]-1], [tile[0], tile[1]+1]]        
    
if __name__ == '__main__':
    file = "sokoban01.txt"
    ai =AI((sokoban_game.Sokoban.readFile(file)))
    locations =  ai.generateAllMoves(ai.startPosition, ai.board)
    print(f"start location:{ai.startPosition}")
    output = ai.board.tolist()
    for loc in locations:
        print(loc)
        output[loc[0]][loc[1]] = '.'
    output[ai.startPosition[0]][ai.startPosition[1]] = 'P'
    for i in output:
        for j in i:
            if j != 0:
                print(j,end="")
            else:
                print(" ",end="")
        print()
    print(ai.dfsSolver())



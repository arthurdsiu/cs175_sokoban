from ai import AI
from sokoban_game import Sokoban
import globals
import os
import sys

if __name__ == '__main__':
    folder = ""
    AUTO_MOVE_FILE_NAME = 'autoMove.txt'
    if len(sys.argv) == 1:
        folder  = input("No folder location for maps provided in cmdline\nPlease enter file location: ")
        print(f'Going to use {folder} as folder for map testing')
    else:
        folder = str(sys.argv[1])

    timeLimit = 3 # 3 second time limit
    globals.TIME_LIMIT = timeLimit
    print(f"Timeout limit is {timeLimit}")
    totalSolved= 0
    total = 0
    for filename in os.listdir(folder):
        # filename = "17.txt"
        f = os.path.join(folder, filename)
        game = None
        ai = None
        game =Sokoban(f)
        ai = AI(game)
        print(f"Calling DFS solver on file {f}, board shape {game.board.shape}")
        moveList = ai.dfsSolver()
        if moveList:
            print(f"DFS success, checking solution")
            moveString = ai.getMoves(moveList)
            # print(f"move string: {moveString}")
            game.autoMove(moveString)
            if game.completed:
                print("\nMap succesfully solved")
                totalSolved += 1
            else:
                 print("Error, DFS return true, but game state is incomplete, exiting program")
                 exit()
        else:
            if ai.failedDueToTimeout:
                print("DFS Timed out ")
            else:
                print("DFS failed to find solution, unsolvable map?")
        total +=1
        print(f'Status: {totalSolved}/{total}')
        
    print(f"Testing finished: {totalSolved}/{total} passed")
    

             

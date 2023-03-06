import sys
import getch
import globals as g
from sokoban_reader import read_sokoban
from sokoban_game import Sokoban

if __name__ == '__main__':
    if len(sys.argv) == 1:
        str  = input("No file location provided in cmdline\nPlease enter file location: ")
        print(str)
        game = Sokoban(str)
    else:
        game = Sokoban(sys.argv[1])
    
    cont = True
    while(cont):
        if game.completed:
            print("you won! Here's your move History")
            print(game.moveHistory)
            outputLocation = "move.txt"
            print(f"writing move history to {outputLocation}")
            try:
                with open(outputLocation, "w") as f:
                    f.write(game.moveHistory)
            except FileNotFoundError:
                print("Error Writing to File")
            exit()
        char = getch.getch()
        print("l to load a move file to auto play:\
\nq to go back\
\nwasd to navigate the maze")
        if(char == 'l'):
            input_location = input("Enter move file: ")
            try:
                with open(input_location, "r") as f:
                    input_lines = [i.strip() for i in f.readlines()]
            except FileNotFoundError:
                print("Error Accessing File")
            game.autoMove(input_lines[0])
        if(char == 'q'):
            cont = False
        if(char == 'w'):
            game.movePlayer(g.UP)
        if(char == 'a'):
            game.movePlayer(g.LEFT)
        if(char == 's'):
            game.movePlayer(g.DOWN)
        if(char == 'd'):
            game.movePlayer(g.RIGHT)
        game.printBoard()


        

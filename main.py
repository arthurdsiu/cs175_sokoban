import sys
import getch
import globals as g
from sokoban_reader import read_sokoban
from sokoban_game import Sokoban

if __name__ == '__main__':
    if len(sys.argv) == 1:
        result = read_sokoban(input("Please enter file location: "))
    else:
        result, board = read_sokoban(sys.argv[1])
    #print(result)
    #print(board)
    #n_boxes = result["n_boxes"]
    #print(f"The number of boxes in this sokoban is {n_boxes}")
    game = Sokoban(board)
    cont = True
    while(cont):
        char = getch.getch()
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
        game.board[game.playerPosition[0]][game.playerPosition[1]]= 9
        game.printBoard()
        game.board[game.playerPosition[0]][game.playerPosition[1]]= 0


        

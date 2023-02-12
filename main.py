import sys
from sokoban_reader import read_sokoban
from sokoban_game import Sokoban

if __name__ == '__main__':
    if len(sys.argv) == 1:
        str  = input("Please enter file location: ")
        print(str)
        result, board = read_sokoban(str)
    else:
        result, board = read_sokoban(sys.argv[1])
    print(result)
    print(board)
    #n_boxes = result["n_boxes"]
    #print(f"The number of boxes in this sokoban is {n_boxes}")
    game = Sokoban(board)
    print(game.board)
    print(game.playerPosition)

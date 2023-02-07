import sys
from sokoban_reader import read_sokoban

if __name__ == '__main__':
    if len(sys.argv) == 1:
        result = read_sokoban(input("Please enter file location: "))
    else:
        result, board = read_sokoban(sys.argv[1])
    print(result)
    print(board)
    #n_boxes = result["n_boxes"]
    #print(f"The number of boxes in this sokoban is {n_boxes}")

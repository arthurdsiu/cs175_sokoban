import sys
import getch
import globals as g
from sokoban_reader import read_sokoban
from sokoban_game import Sokoban

def print_sokoban(markers: set, space: set, boxes: set, init_loc: list, board_size: list):
    beyond_9 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
    head = ''
    for _ in range(len(str(board_size[0])) + 1):
        head += ' '
    for i in range(1, board_size[1] + 1):
        if i < 10:
            head += str(i)
        else:
            head += beyond_9[i-10]
    print(head)
    for i, y in enumerate(range(1, board_size[0] + 1)):
        line_str = ''
        for _ in range(len(str(board_size[0])) - len(str(i+1))):
            line_str += ' '
        line_str += f'{i+1}|'
        for x in range(1, board_size[1] + 1):
            if f"{y},{x}" in markers:
                line_str += '.'
            elif f"{y},{x}" in boxes:
                line_str += '$'
            elif f"{y},{x}" in space:
                line_str += '#'
            elif [y, x] == init_loc:
                line_str += '@'
            else:
                line_str += ' '
        print(line_str)


def in_bound(board_size: list, test_point: list) -> bool:
    return 0 < test_point[0] <= board_size[0] and 0 < test_point[1] <= board_size[1]


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sokoban_board, soko = read_sokoban(input("Please enter file location: "))
    else:
        sokoban_board, soko = read_sokoban(sys.argv[1])


    # sokoban_board = read_sokoban("sokoban01.txt")

    space = set()
    boxes = set()

    # Add all non-empty squares space set
    for i in range(sokoban_board['n_wallsquares']):
        space.add(f"{sokoban_board['wallsquares'][i*2]},{sokoban_board['wallsquares'][i*2+1]}")

    for i in range(sokoban_board['n_boxes']):
        space.add(f"{sokoban_board['boxes'][i*2]},{sokoban_board['boxes'][i*2+1]}")
        boxes.add(f"{sokoban_board['boxes'][i*2]},{sokoban_board['boxes'][i*2+1]}")

    # No zero indexing in given sokoban format
    # Points [y, x]

    connected_whitespace = set()

    print_sokoban(connected_whitespace, space, boxes, sokoban_board['initlocation'], sokoban_board['size'])

    def search(init_loc: [], display_movement=False):
        connected_whitespace.add(f"{init_loc[0]},{init_loc[1]}")

        if display_movement:
            print_sokoban(connected_whitespace, space, boxes, sokoban_board['initlocation'], sokoban_board['size'])
            print()

        possible_neighbors = [[init_loc[0]+1, init_loc[1]], [init_loc[0]-1, init_loc[1]], [init_loc[0], init_loc[1]+1], [init_loc[0], init_loc[1]-1]]
        possible_neighbors = [i for i in possible_neighbors if in_bound(sokoban_board['size'], i) and f"{i[0]},{i[1]}" not in space]
        unsearched_neighbors = [i for i in possible_neighbors if f"{i[0]},{i[1]}" not in connected_whitespace]
        for neighbor in unsearched_neighbors:
            search(neighbor)

    search(sokoban_board['initlocation'])

    print()

    print_sokoban(connected_whitespace, space, boxes, sokoban_board['initlocation'], sokoban_board['size'])

    print()

    for i in range(sokoban_board['n_storagelocations']):
        location = [sokoban_board['boxes'][i*2],sokoban_board['boxes'][i*2+1]]
        possible_neighbors = [[location[0]+1, location[1]], [location[0]-1, location[1]], [location[0], location[1]+1], [location[0], location[1]-1]]
        opposites = [possible_neighbors[1], possible_neighbors[0], possible_neighbors[3], possible_neighbors[2]]
        pushable = []
        for i in range(4):
            pushable.append(in_bound(sokoban_board['size'], possible_neighbors[i]) and in_bound(sokoban_board['size'], opposites[i]) and f"{possible_neighbors[i][0]},{possible_neighbors[i][1]}" in connected_whitespace and f"{opposites[i][0]},{opposites[i][1]}" not in space)

        if True in pushable:
            directions = ['U', 'D', 'L', 'R']
            out_str = f'({location[1]}, {location[0]})'
            for i in range(4):
                if pushable[i]:
                    out_str += directions[i]
            print(out_str)

    # game = Sokoban(soko)
    # cont = True
    # while(cont):
    #     if game.completed:
    #         print("you won!")
    #         exit()
    #     char = getch.getch()
    #     if(char == 'q'):
    #         cont = False
    #     if(char == 'w'):
    #         game.movePlayer(g.UP)
    #     if(char == 'a'):
    #         game.movePlayer(g.LEFT)
    #     if(char == 's'):
    #         game.movePlayer(g.DOWN)
    #     if(char == 'd'):
    #         game.movePlayer(g.RIGHT)
    #     game.printBoard()














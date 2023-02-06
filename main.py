from sokoban_reader import read_sokoban

if __name__ == '__main__':
    n_boxes = read_sokoban(input("Please enter file location: "))["n_boxes"]
    print(f"The number of boxes in this sokoban is {n_boxes}")

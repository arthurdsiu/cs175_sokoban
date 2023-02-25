import numpy as np

#Note: It's assumed that the file will never have conflicting coordinates
#this function won't work correctly if that happens. This includex boxes on top of goals
def read_sokoban(input_location: str) -> dict:
    """Reads sokoban file"""
    try:
        with open(input_location, "r") as f:
            input_lines = [i.strip() for i in f.readlines()]
    except FileNotFoundError:
        print("Error Accessing File")
        return

    input_split = list()
    for line in input_lines:
        row = list()
        for num in line.split():
            row.append(int(num))
        input_split.append(row)        
    #print(input_split)
    #print(f"Sokoban board size: {input_split[0][0]} {input_split[0][1]} ")
    try:
        result = dict()
        result["size"] = [int(i) for i in input_lines[0].split(" ")]
        result["n_wallsquares"] = int(input_lines[1].split(" ")[0])
        result["wallsquares"] = [int(i) for i in input_lines[1].split(" ")[1:]]
        result["n_boxes"] = int(input_lines[2].split(" ")[0])
        result["boxes"] = [int(i) for i in input_lines[2].split(" ")[1:]]
        result["n_storagelocations"] = int(input_lines[3].split(" ")[0])
        result["storagelocations"] = [int(i) for i in input_lines[3].split(" ")[1:]]
        result["initlocation"] = [int(i) for i in input_lines[4].split(" ")]
    except Exception as E:
        print(f"Error Parsing File\n{E}")
    return result
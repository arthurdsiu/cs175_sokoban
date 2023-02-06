def read_sokoban(input_location: str) -> dict:
    """Reads sokoban file"""
    try:
        with open(input_location, "r") as f:
            input_lines = [i.strip() for i in f.readlines()]
    except FileNotFoundError:
        print("Error Accessing File")
        return

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
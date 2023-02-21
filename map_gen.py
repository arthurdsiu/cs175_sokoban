import sys
import os
'''
; dennoates a new map
\n
# = wall
. = storage
$ = box
@ = player location
\n
'''
if __name__ == '__main__':
    if len(sys.argv) == 1:
        fileLoc  = input("Please enter file location: ")
        
    else:
        fileLoc = sys.argv[1]

    mapNum = None
    rowIndex = None
    box = None
    wall = None
    storage = None
    playerLocation = None
    rowSize = None
    colSize = None
    outputLocation = os.getcwd() + "/maps/"
    
    def dumpMap():
        try:
            with open(os.path.join(outputLocation, str(mapNum)+".txt"), "w") as o:
                o.write(f"{rowIndex+1} {colSize}\n")

                def writeLists(someList):
                    o.write(f"{len(someList)} ")
                    for elem in someList:
                        o.write(f"{elem[0]+1} {elem[1]+1} ")
                    o.write("\n")

                writeLists(wall)
                writeLists(box)
                writeLists(storage)
                o.write(f"{playerLocation[0]} {playerLocation[1]}")
                
        except Exception as e:
            print(f"Failed to write out map {mapNum}: {e}")
    try:
        with open(fileLoc, "r") as f:
            for line in f.readlines():
                start= False
                if line == "\n":
                    if start:
                        start = False
                        continue
                    else:
                        start = True
                        continue

                if line[0] == ";":
                    if mapNum != None:
                        dumpMap()
                    mapNum = int(line.split()[1])
                    rowIndex =0
                    box = list()
                    wall = list()
                    storage = list()
                    playerLocation = list()
                    colSize = 0
                    continue

                for colIndex, char in enumerate(line):
                    if char == '#':
                        wall.append([rowIndex,colIndex])
                    if char == '.':
                        storage.append([rowIndex,colIndex])
                    if char == '$':
                        box.append([rowIndex,colIndex])
                    if char == '@' or char == '+':
                        playerLocation = [rowIndex,colIndex]
                colSize = max (len(line),colSize )
                rowIndex+=1
                

    except FileNotFoundError:
        print("Error Accessing File")

    print("finished")
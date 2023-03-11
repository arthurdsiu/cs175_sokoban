import sys
import os
'''
; dennoates a new map
\n
# = wall
. = storage
$ = box
* = box on storage
@ = player location
\n
'''
if __name__ == '__main__':
    fileLoc = "map_raw"
    if len(sys.argv) == 1:
        print(f"Running map script on default folder location: {fileLoc}")
        
    else:
        fileLoc = sys.argv[1]
        print(f"Running map script on custom folder location: {fileLoc}")
    
    rawMapsDir = os.path.join(os.getcwd(), fileLoc)
    
    for dirName in os.listdir(rawMapsDir):
        rawMapFile = os.path.join(rawMapsDir, dirName) # file to read from
        if os.path.isfile(rawMapFile):
            outputPath = os.path.join(os.getcwd(), dirName.split('.')[0]) # folder to write to
            

            if not os.path.exists(outputPath):
                print(f'Path does not exist, creating directory {outputPath}')
                os.mkdir(outputPath)

            try:
                with open(rawMapFile, "r") as f:
                    rowIndex =0
                    colSize = 0
                    wall = list()
                    box = list()
                    storage = list()
                    playerLocation = list()
                    
                    mapNum = None
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

                                def dumpMap(rowIndex, colSize, wall, box, storage, playerLocation):
                                    try:
                                        with open(os.path.join(outputPath, str(mapNum)+".txt"), "w") as o:
                                            o.write(f"{rowIndex+1} {colSize}\n")

                                            def writeLists(someList):
                                                o.write(f"{len(someList)} ")
                                                for elem in someList:
                                                    o.write(f"{elem[0]+1} {elem[1]+1} ")
                                                o.write("\n")

                                            writeLists(wall)
                                            writeLists(box)
                                            writeLists(storage)
                                            o.write(f"{playerLocation[0]+1} {playerLocation[1]+1}")
                                            
                                    except Exception as e:
                                        print(f"Failed to write out map {mapNum}: {e}")

                                dumpMap(rowIndex, colSize, wall, box, storage, playerLocation) # write out previous map
                            # clear out old map/ init variables if first map
                            rowIndex =0
                            colSize = 0
                            wall = list()
                            box = list()
                            storage = list()
                            playerLocation = list()
                            
                            mapNum = int(line.split()[1])
                            continue

                        for colIndex, char in enumerate(line):
                            if char == '#':
                                wall.append([rowIndex,colIndex])
                            if char == '.':
                                storage.append([rowIndex,colIndex])
                            if char == '$':
                                box.append([rowIndex,colIndex])
                            if char == '*':
                                storage.append([rowIndex,colIndex])
                                box.append([rowIndex,colIndex])
                            if char == '@' or char == '+':
                                playerLocation = [rowIndex,colIndex]
                        colSize = max (len(line),colSize )
                        rowIndex+=1
                        

            except FileNotFoundError as e:
                print(f"Error Accessing File {e}")

    print("finished")
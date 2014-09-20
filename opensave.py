def saveToFile(save_as, miniblocks):
    output_file = open(save_as, "w+")
    for b in miniblocks:
        output_file.write(" ".join([str(b.p1.x), str(b.p1.z), str(b.p1.y),
                         str(b.p2.x), str(b.p2.z), str(b.p2.y)]) + "\n")
    output_file.close()

def loadFromFile(load_from, miniblocks):
    miniblocks = []
    input_file = open(load_from, "r")
    for line in input_file:
        miniblocks.append([int(token) for token in line.split(" ")])
    return

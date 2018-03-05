


def read_file(path):
    sequenceFile = open(path, "r")
    sequenceStrings = sequenceFile.readlines()
    sequenceFile.close()
    print(sequenceStrings)

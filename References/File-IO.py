

def totalChars(listOfStrs):
    total = 0
    for i in range(len(listOfStrs)):
        total = len(listOfStrs[i]) + total
    return total


def main():
    myFile = open("FileIn", "r")
    allLines = myFile.readlines()
    myFile.close()

    for i in range(len(allLines)):
        print(allLines[i], end=" ")
    print()
    # testList = ["we\n", " \n", "were\n"]
    charCount = totalChars(allLines)
    print(charCount)


main()


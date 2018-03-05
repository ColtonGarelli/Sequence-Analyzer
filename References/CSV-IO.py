def calcAvg(grades):
    total = 0
    length = 0
    for row in range(len(grades)):
        for column in range(len(grades[row])):
            total += grades[row][column]
            length += 1
    return total / length


def makeNumList(aStr):
    # if last character is \n, get rid of it
    if aStr[len(aStr) - 1] == "\n":
        newStr = aStr[0:len(aStr) - 1]
    else:
        newStr = aStr
    # split up all the numbers by the commas
    myList = newStr.split(",")
    for i in range(len(myList)):
        myList[i] = int(myList[i])
    return myList


def main():
    '''
    testStr = "8,10,7,8,6\n"
    testList = makeNumList(testStr)
    print("Should be [8, 10, 7, 8, 6]:", testList)
    '''

    gradeFile = open("171-48-grades.csv", "r")
    gradeStrings = gradeFile.readlines()
    gradeFile.close()

    print(gradeStrings)
    gradeInts = []
    for i in range(len(gradeStrings)):
        gradeInts.append(makeNumList(gradeStrings[i]))

    for i in range(len(gradeInts)):
        print(gradeInts[i])

    # loop through 2nd student's grades
    total = 0
    for i in range(len(gradeInts[1])):
        total += gradeInts[1][i]
    print(total)

    # loop through the 1st quiz grades
    quizTotal = 0
    for i in range(len(gradeInts)):
        quizTotal += gradeInts[i][0]
    print(quizTotal)

    myAvg = calcAvg(gradeInts)
    print(myAvg)


main()

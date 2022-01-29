# Date: Month: 03 Day: 08 Year: 2021
# Author: Ivanoiu Alexandru Paul and Ali Mohsen Alagrami

import copy


# This function create the initial matrix starting from the input string
def createMatrix(stringInput):
    theGrid = [[-1] * 9 for i in range(0, 9)]
    stringInput = stringInput.replace(" ", "")
    for i in range(0, 9):
        for j in range(0, 9):
            if stringInput[i * 9 + j] != ".":
                theGrid[i][j] = int(stringInput[i * 9 + j])
            else:
                theGrid[i][j] = -1
    for arr in theGrid:
        print(arr)
    return theGrid


# This function create the domain matrix that contains the domain of each cell
def createDomainMatrix():
    matrixDomains = []
    for i in range(0, 9):
        matrixDomains.append([])
        for j in range(0, 9):
            matrixDomains[i].append([i for i in range(1, 10)])
    return matrixDomains


def printDomain(matrixDomains):
    for i in range(0, 9):
        for j in range(0, 9):
            print(matrixDomains[i][j], end=" ")
        print("\n")


# This function does the propagation
def propagation(specificRow, specificColumn, matrixValue, domain):
    # This is how I find the positions for each square
    startingPossitionRowBloc = specificRow - specificRow % 3
    startingPossitionColBloc = specificColumn - specificColumn % 3

    domain[specificRow][specificColumn] = [matrixValue]

    # Columns propagation
    for i in range(0, 9):
        if matrixValue in domain[specificRow][i]:
            if specificColumn != i:
                domain[specificRow][i].remove(matrixValue)

    # Row propagation
    for j in range(0, 9):
        if matrixValue in domain[j][specificColumn]:
            if specificRow != j:
                domain[j][specificColumn].remove(matrixValue)

    # Block propagation
    for o in range(startingPossitionRowBloc, startingPossitionRowBloc + 3):
        for p in range(startingPossitionColBloc, startingPossitionColBloc + 3):
            if matrixValue in domain[o][p]:
                if (o != specificRow) or (p != specificColumn):
                    domain[o][p].remove(matrixValue)
    return domain


# This function together with the propagation function propagate the values for the first time. This function is used
# just once at the beginning
def cleaningDomain(matrix, domain):
    for i in range(9):
        for j in range(9):
            if matrix[i][j] != -1:
                domain[i][j] = [matrix[i][j]]
                domain = propagation(i, j, matrix[i][j], domain)


def backTracking(domain, rows, cols):
    # I am at the end of the game
    if rows == 8 and cols == 8:
        print("Solution")
        for i in range(0, 9):
            for j in range(0, 9):
                print(domain[i][j], end=" ")
            print("\n")
        return True

    # I am at the end of a column and I have to go a next row
    elif cols == 9:
        backTracking(copy.deepcopy(domain), rows + 1, 0)

    # If I have an empty domain of a cell this means that at some point I put a wrong number in a place so I have to
    # go back
    elif len(domain[rows][cols]) == 0:
        return False

    else:
        # If the domain has more than one value I do not know which is the right one and I have to try them one by one
        # but I know that for that specific cell every value of the domain in this moment is a valid value
        for h in domain[rows][cols]:
            backTracking(copy.deepcopy(propagation(rows, cols, h, copy.deepcopy(domain))), rows, cols + 1)


def main():
    stringInputMatrix = ".....3.17 .15..9..8 .6....... 1....7... ..9...2.. ...5....4 .......2.5.. 6..34. 34. 2.. ..."
    stringInputMatrix2 = "... 26. 7.1 68. .7. .9. 19. ..4 5.. 82. 1.. .4. ..4 6.2 9.. .5. ..3 .28 ..9 3.. .74 .4. .5. .36 7.3 .18 ..."
    stringInputMatrix3 = ".2. 6.8 ... 58. ..9 7.. ... .4. ... 37. ... 5.. 6.. ... ..4 ..8 ... .13 ... .2. ... ..9 8.. .36 ... 3.6 .9."

    GRID = createMatrix(stringInputMatrix3)

    # Now that we have the entire grip of numbers we need the domains of each single cell
    Domains = createDomainMatrix()

    # Once we have the domain too we can print it
    print("####Domain before cleaning####")
    printDomain(Domains)

    # Once we have the domain we can do the first propagation to "clean" the domain of each cell
    cleaningDomain(GRID, Domains)

    print("####Domain after cleaning####")
    printDomain(Domains)

    # Once I have the domain cleaned I can start working on that numbers to change them and solve the sudoku
    backTracking(Domains, 0, 0)


if __name__ == "__main__":
    main()

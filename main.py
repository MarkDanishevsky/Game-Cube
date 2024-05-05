from time import sleep
from button_input import take_input
from display import setLightTo, clearScreen
from publish_moves import send_string

def printGrid(grid: dict) -> list:
    out = []
    for row in range(TOTALHEIGHT, 0, -1):
        firstLine = '+----' * TOTALWIDTH + '+'
        secondLine = '|'
        for col in range(1, TOTALWIDTH + 1):
            if grid[(row, col)] in [YELLOWDISPLAY, REDDISPLAY, GREENDISPLAY]:
                secondLine += ' ' + grid[(row, col)] + ' |'
            else:
                secondLine += ' ' + grid[(row, col)] + '  |'
        out.extend([firstLine, secondLine])
    out.append('+----' * TOTALWIDTH + '+')
    return out

def printGridLED(grid: dict) -> None:
    for row in range(TOTALHEIGHT, 0, -1):
        for col in range(1, TOTALWIDTH + 1):
            if grid[(row, col)] == YELLOWDISPLAY:
                setLightTo(coordinate=(row, col), colour=YELLOW)
            elif grid[(row, col)] == REDDISPLAY:
                setLightTo(coordinate=(row, col), colour=RED)
            elif grid[(row, col)] == GREENDISPLAY:
                setLightTo(coordinate=(row, col), colour=GREEN)
            else:
                setLightTo(coordinate=(row, col), colour=EMPTY)

def placeMove(col: int, grid: dict, currentlyPlacingYellow: bool) -> dict:
    for row in range(TOTALHEIGHT, 0, -1):
        if grid[(row, col)] != INITIAL:
            grid[(row + 1, col)] = YELLOWDISPLAY if currentlyPlacingYellow else REDDISPLAY
            return grid, row + 1
        else:
            grid[(row, col)] = YELLOWDISPLAY if currentlyPlacingYellow else REDDISPLAY
            print('\n'.join(printGrid(grid=grid)))
            printGridLED(grid=grid)
            sleep(0.1)
            grid[(row, col)] = INITIAL
        
    grid[(1, col)] = YELLOWDISPLAY if currentlyPlacingYellow else REDDISPLAY
    return grid, 1

def isWithinBounds(cord: tuple) -> bool:
    return 1 <= cord[0] <= TOTALHEIGHT and 1 <= cord[1] <= TOTALWIDTH

def moveIsValid(col: int, grid: dict) -> bool:
    return grid[(6, col)] == INITIAL

def moveIsWin(row: int, col: int, currentlyPlacingYellow: bool, grid: dict) -> tuple:
    # Going down, going up, going left, going right
    upDownChecks = [[(row - 1, col), (row - 2, col), (row - 3, col)], [(row + 1, col), (row + 2, col), (row + 3, col)], [(row, col - 1), (row, col - 2), (row, col - 3)], [(row, col + 1), (row, col + 2), (row, col + 3)]]

    # Going up and right, up and left, down and right, down and left
    diagonalChecks = [[(row + 1, col + 1), (row + 2, col + 2), (row + 3, col + 3)], [(row + 1, col - 1), (row + 2, col - 2), (row + 3, col - 3)], [(row - 1, col + 1), (row - 2, col + 2), (row - 3, col + 3)], [(row - 1, col - 1), (row - 2, col - 2), (row - 3, col - 3)]]

    totalChecks = upDownChecks + diagonalChecks

    colour = (YELLOWDISPLAY if currentlyPlacingYellow else REDDISPLAY)
    for cord1, cord2, cord3 in totalChecks:
        if isWithinBounds(cord=cord1) and isWithinBounds(cord=cord2) and isWithinBounds(cord=cord3) and grid[cord1] == colour and grid[cord2] == colour and grid[cord3] == colour:
            return True, (cord1, cord2, cord3)
    return False, []

def flashWinner(grid: dict, cord: tuple, cord1: tuple, cord2: tuple, cord3: tuple) -> None:
    flash = grid.copy()
    flash[cord], flash[cord1], flash[cord2], flash[cord3] = INITIAL, INITIAL, INITIAL, INITIAL
    flashDisplay = printGrid(grid=flash)
    gridDisplay = printGrid(grid=grid)
    while True:
        print('\n'.join(flashDisplay))
        printGridLED(grid=flash)

        sleep(1)

        print('\n'.join(gridDisplay))
        printGridLED(grid=grid)

        sleep(1)
        
def filled(grid: dict) -> bool:
    for key, value in grid.items():
        if value == INITIAL:
            return False
    return True

def takeColumn(grid: dict) -> int:
    selectorAt = 4
    grid[(8, selectorAt)] = GREENDISPLAY
    print('\n'.join(printGrid(grid=grid)))
    printGridLED(grid=grid)
    button = int(take_input())
    while button != 4:
        if button == -1:
            pass
        elif button == -2:
            playGame()
        else:
            grid[(8, selectorAt)] = INITIAL
            if button in [3, 5]:
                selectorAt = selectorAt + 1 if selectorAt != 7 else 1
            elif button in [1, 2]:
                selectorAt = selectorAt - 1 if selectorAt != 1 else 7
            grid[(8, selectorAt)] = GREENDISPLAY

            print('\n'.join(printGrid(grid=grid)))
            printGridLED(grid=grid)

            button = int(take_input())

    grid[(8, selectorAt)] = INITIAL
    return selectorAt

def playGame() -> None:
    grid = dict([((x, y), INITIAL) for y in range(1, TOTALWIDTH + 1) for x in range(1, TOTALHEIGHT + 1)])
    clearScreen()
    currentlyPlacingYellow = True #Yellow goes first
    moves = [] #log of all moves
    while not filled(grid=grid):
        colMove = takeColumn(grid=grid)
        while not(moveIsValid(col=colMove, grid=grid)):
            colMove = takeColumn(grid=grid)
        moves.append(colMove)
        grid, row = placeMove(col=colMove, grid=grid, currentlyPlacingYellow=currentlyPlacingYellow)
        won = moveIsWin(row=row, col=colMove, currentlyPlacingYellow=currentlyPlacingYellow, grid=grid)
        if won[0]:
            send_string(string=str(moves)[1:-1])
            flashWinner(cord=(row, colMove), cord1=won[1][0], cord2=won[1][1], cord3=won[1][2], grid=grid)
            break
        currentlyPlacingYellow = not(currentlyPlacingYellow)
        print('\n'.join(printGrid(grid=grid)))
        printGridLED(grid=grid)
        
    if filled(grid=grid):
        print('Tie')

def off() -> None:
    clearScreen()
    while True:
        if int(take_input()) == -1:
            playGame()

TOTALHEIGHT, TOTALWIDTH = 8, 8
YELLOWDISPLAY, REDDISPLAY, GREENDISPLAY, INITIAL = '🟡', '🔴', '🟢', ' '

RED = (255, 0, 0) #only one LED on
YELLOW = (125, 125, 0) #only two LED's on
GREEN = (0, 255, 0) # green
EMPTY = (0, 0, 0) #Changing this might fry the pi
try:
    clearScreen()
    playGame()

except KeyboardInterrupt:
    pass
    clearScreen()
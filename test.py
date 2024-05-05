from time import sleep
#from button_input import take_input
#from display import setLightTo, clearScreen

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
"""
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
"""
def takeColumn() -> int:
    selectorAt = 4
    button = int(input())
    while button != 4:
        grid[(8, selectorAt)] = INITIAL
        if button in [3, 5]:
            selectorAt = selectorAt + 1 if selectorAt != 7 else 1
        elif button in [1, 2]:
            selectorAt = selectorAt - 1 if selectorAt != 1 else 7
        grid[(8, selectorAt)] = GREENDISPLAY
        print(grid)
        print('\n'.join(printGrid(grid)))

        #printGridLED(grid=grid)

        button = int(input())
    grid[(8, selectorAt)] = INITIAL
    return selectorAt


TOTALHEIGHT, TOTALWIDTH = 8, 8
YELLOWDISPLAY, REDDISPLAY, GREENDISPLAY, INITIAL = '🟡', '🔴', '🟢', ' '

RED = (255, 0, 0) #only one LED on
YELLOW = (125, 125, 0) #only two LED's on
GREEN = (0, 255, 0) # green
EMPTY = (0, 0, 0) #Changing this might fry the pi

grid = dict([((x, y), INITIAL) for y in range(1, TOTALWIDTH + 1) for x in range(1, TOTALHEIGHT + 1)])
#printGridLED(grid)
print('\n'.join(printGrid(grid)))

takeColumn()

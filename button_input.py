from time import sleep, time
import RPi.GPIO as GPIO
from display import clearScreen

DELAY = 0.1
INPIN1 = 29
INPIN2 = 38
INPIN3 = 37
INPIN4 = 11
INPIN5 = 36
#INPIN6 = 33
#INPIN7 = 32

DOUBLE_PRESS_THRESHOLD = 0.6 #sec

GPIO.setmode(GPIO.BOARD)
GPIO.setup(INPIN1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(INPIN2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(INPIN3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(INPIN4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(INPIN5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(INPIN6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(INPIN7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def take_input() -> int:
    try:
        center_button_last_pressed = 0 # INPIN4
        while True:
            readVals = []
            if list(map(lambda x: GPIO.input(x), [INPIN1, INPIN2, INPIN3, INPIN4, INPIN5])) != readVals: # Different
                readVals = [INPIN1, INPIN2, INPIN3, INPIN4, INPIN5]
                readVals = list(map(lambda x: GPIO.input(x), readVals))

                if readVals[3] == 1:
                    center_button_last_pressed = time()
                    while time() - center_button_last_pressed <= DOUBLE_PRESS_THRESHOLD:
                        if GPIO.input(INPIN4) == 0:
                            while time() - center_button_last_pressed <= DOUBLE_PRESS_THRESHOLD:
                                if GPIO.input(INPIN4) == 1:
                                    print('DOUBLE CLICK')
                                    return -2 #Center button double tap
                    print('SINGLE CLICK')
                    return 4

                if sum(readVals) == 3:
                    return -1 #Three buttons pressed
                else:
                    for pin in range(1, len(readVals) + 1):
                        if readVals[pin - 1] == 1:
                            return pin
                        
                sleep(DELAY)

    except KeyboardInterrupt:
            GPIO.cleanup()
            clearScreen()

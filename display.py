import time
from rpi_ws281x import Adafruit_NeoPixel, Color

# LED strip configuration:
LED_COUNT      = 8 * 8      # Number of LED pixels.
LED_PIN        = 21      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

# Initialize the library (must be called once before other functions).
strip.begin()

def conversion(coordinate: tuple) -> int:
    r, c = coordinate
    return (r - 1) * 8 + ((8 - c) if r % 2 == 0 else (c - 1))

def setLightTo(coordinate: tuple, colour: tuple) -> None:
    r, g, b = colour
    strip.setPixelColor(conversion(coordinate=coordinate),Color(r, g, b))
    strip.show()  # Update the strip with the new colors

def clearScreen() -> None:
    for led in range(LED_COUNT):
        strip.setPixelColor(led, Color(0, 0, 0))
    strip.show()

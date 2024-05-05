from Adafruit_IO import Client

aio = Client('USER_NAME', 'KEY')

FEED_NAME = 'connect-4-ai-training-database'

def send_string(string: str) -> None:
    aio.send_data(FEED_NAME, string)
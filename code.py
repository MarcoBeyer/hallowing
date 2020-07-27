
import board
import busio
import digitalio
import time
import touchio
import displayio
import audioio

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

uart = busio.UART(board.TX, board.RX, baudrate=9600)
wave_file = open("Rockface.wav", "rb")
wave = audioio.WaveFile(wave_file)
audio = audioio.AudioOut(board.A0)

splash = displayio.Group()
board.DISPLAY.show(splash)

brightness_down = touchio.TouchIn(board.TOUCH2)
brightness_up = touchio.TouchIn(board.TOUCH3)

max_brightness = 0.5

with open('Yoshi.bmp', "rb") as f:
    try:
        odb = displayio.OnDiskBitmap(f)
    except ValueError:
        print("Image unsupported {}".format('Yoshi.bmp'))
    face = displayio.TileGrid(odb, pixel_shader=displayio.ColorConverter(), x=0, y=0)
    splash.append(face)
    # Wait for the image to load.
    board.DISPLAY.refresh()

audio.play(wave)

while True:
    data = uart.readline()

    if data is not None:
        data_string = bytes.decode(data, 'utf-8')
        print(data_string)
    if brightness_up.value:
        max_brightness += 0.1
    elif brightness_down.value:
        max_brightness -= 0.1
    if max_brightness < 0:
        max_brightness = 0
    elif max_brightness >= 1:
        max_brightness = 1.0
    board.DISPLAY.brightness = max_brightness
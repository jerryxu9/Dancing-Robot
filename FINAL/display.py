############################## Start of display.py ##############################
import board
import displayio
import digitalio
import storage
import lib.adafruit_sdcard
import lib.adafruit_st7735r
import canvas

# Creates a canvas to display content on LCD
class TFTDisplay():
    def __init__(self, spi):
        self._on = False

        self._display = self._init_display(spi)
        self._init_sdcard(spi)
        self._canvas = canvas.TFTCanvas(self._display)

    #initializing the display     
    def _init_display(self, spi):
        displayio.release_displays()
        display_bus = displayio.FourWire(spi, command=board.D10, chip_select=board.D7, reset=board.D9)
        return lib.adafruit_st7735r.ST7735R(display_bus, width=128, height=128, rowstart=1, colstart=2)

    # Allows us to interface with SD card where we stores some of our files which didn't fit on ItsyBitsy
    def _init_sdcard(self, spi):
        cs = digitalio.DigitalInOut(board.D12)
        sdcard = lib.adafruit_sdcard.SDCard(spi, cs)
        vfs = storage.VfsFat(sdcard)
        storage.mount(vfs, "/sd")

    # Returns whether display is on or off
    @property
    def on(self):
        return self._on
    
    # Turns the display on or off
    @on.setter
    def on(self, value):
        self._on = value

    # Returns the canvas
    @property
    def canvas(self):
        return self._canvas
############################## End of display.py ##############################
import os
import time
import displayio

class Graphic():
    def get_name(self):
        pass

    def _find_between(self, string, first, last):
        try:
            start = string.index( first ) + len( first )
            end = string.index( last, start )
            return string[start:end]
        except ValueError:
            return ""      
        

class Image(Graphic):
    def __init__(self, image_file):
        self._image_file = image_file

        bitmap_file = open(image_file, "rb")
        bitmap = displayio.OnDiskBitmap(bitmap_file)
        self._tile_grid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter())

    def get_name(self):
        return self._find_between(self._image_file, "/", ".")

    @property
    def tile_grid(self):
        return self._tile_grid
    

class GIF(Graphic):
    def __init__(self, directory):
        self._directory = directory
        
        self._frames = []
        self._load_frames()

    def _load_frames(self):
        #all gif frames are named "<name>-<frame_number>.bmp"
        for image_file in sorted(os.listdir(self._directory), key=lambda x: int(self._find_between(x, '-', '.bmp'))):
            image = Image(self._directory + "/" + image_file)
            self._frames.append(image)

    def get_name(self):
        return self._directory.replace("/", "")

    @property
    def frames(self):
        return self._frames

class Graphics():
    def __init__(self, display):
        self._display = display

        self._group = displayio.Group()

    def clear(self):
        self._group = displayio.Group()

    def draw_image(self, image):
        try:
            self._group.index(image.tile_grid)
        except ValueError:
            self._group.append(image.tile_grid)
        
        self._display.show(self._group)

    def remove_image(self, image):
        try:
            self._group.remove(image.tile_grid)
        except:
            pass

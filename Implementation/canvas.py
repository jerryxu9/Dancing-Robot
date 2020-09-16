import time

import graphics

#Uses a design pattern similar to Swing (Java)
class TFTCanvas():
    def __init__(self, display):
        self._display = display
        
        self._graphics = graphics.Graphics(display)
        self._components = []
    
    def clear(self):
        self._components.clear()
        self._graphics.clear()

    @property
    def current_component(self):
        return self._components[0] #only supporting 1 component at a time

    def add_component(self, component):
        self.clear() #let's not support multiple components on a 2" display
        self._components.append(component)

    def remove_component(self, component):
        self._components.remove(component)

    #display the current image
    def update(self):
        for component in self._components:
            component.paint(self._graphics)
            
class TFTComponent():
    def paint(self, graphics):
        pass

class GIFComponent(TFTComponent):
    def __init__(self, gif):
        self._gif = gif

        self._delay = 0.1
        self._current_frame = 0
        self._current_time = time.monotonic()
        self._previous_time = self._current_time
    
    #not passing in current_time here to keep all graphics decoupled as images do not require a timestamp
    def paint(self, graphics):
        self._current_time = time.monotonic()
        if(self._current_time - self._previous_time >= self._delay):
            self._current_frame = self._current_frame + 1
            self._previous_time = self._current_time
        
        if (self._current_frame >= len(self._gif.frames)):
            self._current_frame = -1

        if (self._current_frame != 0):
            graphics.remove_image(self._gif.frames[self._current_frame - 1])

        if (self._current_frame < len(self._gif.frames)):
            graphics.draw_image(self._gif.frames[self._current_frame])

class ImageComponent(TFTComponent):
    def __init__(self, image):
        self._image = image

    def paint(self, graphics):
        graphics.draw_image(self._image)


    
        
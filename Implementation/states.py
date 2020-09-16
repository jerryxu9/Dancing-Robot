import logger

import dance
import components
import graphics
import canvas

class State():
    def __init__(self, name, biped):
        self._name = name
        self._biped = biped
        self._pause = False
    
    @property
    def name(self):
        return self._name

    def on_enter(self):
        print("State Changed to " + self.name)
        #Logger.LOG.info("State changed to " + self.name)
        pass

    def pause(self):
        self._pause = True

    def unpause(self):
        self._pause = False

    def on_key_change(self, key):
        for servo in self._biped.servos():
            servo.reset()

    def update(self, current_time):
        if (self._pause == True):
            print("ok")
            return
        pass

    def on_finish(self):
        self._biped.state = Waiting(self._biped)
        pass
        
class Waiting(State):
    def __init__(self, biped):
        super().__init__("Waiting", biped)
    
    def on_enter(self):
        smile_image = graphics.Image("/sd/images/smile.bmp")
        component = canvas.ImageComponent(smile_image)
        self._biped.display.canvas.add_component(component)

        self._biped.buzzer.off()

    def on_key_change(self, key):
        super().on_key_change(key)

        new_dance = components.Keys.to_dance(key)
        if (new_dance != None):
            self._biped.state = Dancing(self._biped, new_dance)
        
    def update(self, current_time):
        super().update(current_time)
        
class Dancing(State):
    def __init__(self, biped, dance_):
        super().__init__("Dancing", biped)
        self._current_dance = dance.Dance(biped, dance_ + ".sequence")
        
    @property
    def current_dance(self):
        return self._current_dance
    
    @current_dance.setter
    def current_dance(self, value):
        self._current_dance = value

    def on_enter(self):
        audio_gif = graphics.GIF("/audio/")
        component = canvas.GIFComponent(audio_gif)
        self._biped.display.canvas.add_component(component)

    def on_key_change(self, key):
        super().on_key_change(key)

        if (key == components.Keys.EIGHT):
            canvas_ = self._biped.display.canvas
            if (isinstance(canvas_.current_component, canvas.GIFComponent)):
                song_image = graphics.Image("/songs/" + self._current_dance.song + ".bmp")
                component = canvas.ImageComponent(song_image)
                canvas_.add_component(component)
            else:
                audio_gif = graphics.GIF("/audio/")
                component = canvas.GIFComponent(audio_gif)
                canvas_.add_component(component)

        new_dance = components.Keys.to_dance(key)
        if (self._current_dance == None):
            self._current_dance = dance.Dance(self._biped, new_dance + ".sequence")

        if (new_dance != None and self._current_dance.song != new_dance):
            self._current_dance = dance.Dance(self._biped, new_dance + ".sequence")

    def update(self, current_time):
        if (self._pause == True):
            return

        if (self._current_dance.finished):
            self.on_finish()
            return
        
        self._current_dance.step(current_time)

    def on_finish(self):
        super().on_finish()
        for servo in self._biped.servos:
            servo.reset()

class Aggress(State):
    def __init__(self, biped):
        super().__init__("Aggress", biped)
        self._previous_time = 0
        self._delay = 0.2
    
    def on_enter(self):
        self._biped.buzzer.frequency(components.Note.notes['ZERO'])

        angry_gif = graphics.GIF("/angry/")
        component = canvas.GIFComponent(angry_gif)
        self._biped.display.canvas.add_component(component)

    def on_key_change(self, key):
        super().on_key_change(key)

    def update(self, current_time):
        super().update(current_time)

        time_elapsed = current_time - self._previous_time
        led = self._biped.get_led(5)
        if (time_elapsed >= self._delay):
            if (led.is_on()):
                led.off()
            else:
                led.on()
            self._previous_time = current_time
        
        #set leds
        #play scary sounds
        #set servos to defense
        
    def on_finish(self):
        super().on_finish()
        self._biped.get_led(5).off()
        
        

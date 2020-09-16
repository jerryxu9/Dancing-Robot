############################## Start of states.py ##############################
# This files creates a state machine for the biped and creates the illusion of milti-threading by moving between states very 
# quickly

import logger
import dance
import components
import graphics
import canvas

# State class which has properties which adds versatility to the state machine, allowing it to pause, update and check when done
class State():
    def __init__(self, name, biped):
        self._name = name
        self._biped = biped
        self._pause = False
    
    @property
    def name(self):
        return self._name

    def on_enter(self):
        for servo in self._biped.servos:
            servo.reset()
        #Logger.LOG.info("State changed to " + self.name)
        pass

    def pause(self):
        self._pause = True

    def unpause(self):
        self._pause = False

    def on_key_change(self, key):
        pass

    def update(self, current_time):
        if (self._pause == True):
            return
        pass

    def on_finish(self):
        self._biped.state = Waiting(self._biped)
        pass

# The state machine is in the waiting state (displaying images but not moving) until a key on the keypad is pressed
class Waiting(State):
    def __init__(self, biped):
        super().__init__("Waiting", biped)
    
    def on_enter(self):
        super().on_enter()

        smile_image = graphics.Image("/sd/images/smile.bmp")
        component = canvas.ImageComponent(smile_image)
        self._biped.display.canvas.add_component(component)

        self._biped.buzzer.off()

    def on_key_change(self, key):
        super().on_key_change(key)

        new_dance = components.Keys.to_dance(key)
        if (new_dance != None):
            song = new_dance[0]
            dance = new_dance[1]
            if (new_dance != "none"):
                self._biped.state = Dancing(self._biped, song, dance)
        
    def update(self, current_time):
        super().update(current_time)

# The state machine is in the dancing state when a key on the keypad is pressed and picks a dance move depending on the key 
# pressed while still continually checking if any keys get pressed
class Dancing(State):
    def __init__(self, biped, song_, dance_):
        super().__init__("Dancing", biped)
        self._current_dance = dance.Dance(biped, "sequences/" + song_ + ".sequence", "sequences/" + dance_ + ".sequence")
        
    @property
    def current_dance(self):
        return self._current_dance
    
    @current_dance.setter
    def current_dance(self, value):
        self._current_dance = value

    def on_enter(self):
        super().on_enter()

        audio_gif = graphics.GIF("/audio/")
        component = canvas.GIFComponent(audio_gif, 0.5)
        self._biped.display.canvas.add_component(component)

    def on_key_change(self, key):
        super().on_key_change(key)

        if (key == components.Keys.HASHTAG):
            canvas_ = self._biped.display.canvas
            if (isinstance(canvas_.current_component, canvas.GIFComponent)):
                song_image = graphics.Image("/sd/songs/" + self._current_dance.song + ".bmp")
                component = canvas.ImageComponent(song_image)
                canvas_.add_component(component)
            else:
                audio_gif = graphics.GIF("/audio/")
                component = canvas.GIFComponent(audio_gif, 0.5)
                canvas_.add_component(component)

        new_dance = components.Keys.to_dance(key)
        if (new_dance != None):
            if (new_dance != "none"):
                song = new_dance[0]
                dance_ = new_dance[1]

                if ((new_dance != None and self._current_dance.song != new_dance) or self._current_dance == None):
                    self._current_dance = dance.Dance(self._biped, "sequences/" + song + ".sequence", "sequences/" + dance_ + ".sequence")
            else:
                self._biped.state = Waiting(self._biped)

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

# The state machine is in the aggress state when an object gets too close to the sonar, causing the red LEDs to turn on and 
# display an angry image on the LCD
class Aggress(State):
    def __init__(self, biped):
        super().__init__("Aggress", biped)
        self._previous_time = 0
        self._delay = 0.2
    
    def on_enter(self):
        super().on_enter()
        
        self._biped.buzzer.frequency(components.Note.notes['ZERO'])

        angry_gif = graphics.GIF("/angry/")
        component = canvas.GIFComponent(angry_gif, 0.1)
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
############################## Start of states.py ##############################
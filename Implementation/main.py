import board
import time 

import exceptions
import states
import components
import display

class Biped():
    def __init__(self):
        spi = board.SPI()

        shifter = components.Shifter(board.D3, spi)
        self._leds = {
            "1": components.LED(shifter, 1),
            "2": components.LED(shifter, 2),
            "3": components.LED(shifter, 3),
            "4": components.LED(shifter, 4),
            "5": components.LED(shifter, 5)
        }
        self._servos = {
            "D5": components.Servo(board.D5),
            "SCL": components.Servo(board.SCL),
            "SDA": components.Servo(board.SDA),
            "D0": components.Servo(board.D0)
        }
        self._buzzer = components.Buzzer(board.A1)
        self._keypad = components.KeyPad()
        self._sonic_sensor = components.SonicSensor(board.A4, board.A5)
        self._display = display.TFTDisplay(spi)
        #self.shifter_in = ShifterIn(board.D0, board.D13, board.D11, board.D1)

        self.state = states.Waiting(self)
        self._previous_state = None

    def get_servo(self, servo_pin):
        if not self._servos.get(servo_pin):
            raise exceptions.ServoNotConnected

        return self._servos[servo_pin]
    
    def servos(self):
        return self._servos.values()

    def get_led(self, led_pin):
        return self._leds[str(led_pin)]

    @property
    def buzzer(self):
        return self._buzzer

    @property
    def keypad(self):
        return self._keypad

    @property
    def sonic_sensor(self):
        return self._sonic_sensor

    @property
    def display(self):
        return self._display

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        self._state.on_enter()

    @property
    def previous_state(self):
        return self._previous_state

    @previous_state.setter
    def previous_state(self, value):
        self._previous_state = value

biped = Biped()

current_time = time.monotonic()

#sonar
sonar_distance = 21
previous_sonar_time = current_time

#keypad
key_pressed = biped.keypad.get_pressed()
previous_key_pressed = key_pressed
previous_key_time = current_time
keypad_delay = 0.5

delay = 0.27
next_time = time.monotonic() + delay
while (biped.keypad.get_pressed() is not components.Keys.ZERO):
    time.sleep(max(0, next_time - time.monotonic()))
    current_time = time.monotonic()

    #keypad
    key_pressed = biped.keypad.get_pressed()
    if ((key_pressed != None and key_pressed != previous_key_pressed) or (current_time - previous_key_time >= keypad_delay)):
        biped.state.on_key_change(key_pressed)
        previous_key_pressed = key_pressed
        previous_key_time = current_time
    
    #sonar
    if (current_time - previous_sonar_time >= 0.1):
        try:
            sonar_distance = biped.sonic_sensor.start(current_time)
            if (sonar_distance != None):
                if (sonar_distance <= 20):
                    if (biped.state.name != "Aggress"):
                        biped.previous_state = biped.state
                        biped.state = states.Aggress(biped)
                elif ((biped.previous_state != None) and (biped.previous_state.name != biped.state.name)):
                    biped.state.on_finish()
                    biped.state = biped.previous_state
                    biped.previous_state = None
        except RuntimeError:
            pass
        previous_time = current_time

    biped.state.update(current_time)
    biped.display.canvas.update()

    next_time += (time.monotonic() - next_time) // delay * delay + delay
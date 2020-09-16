########## Start of main.py ##########

import board
import time 
import exceptions
import states
import components
import display

# Initializes all components of the biped including LEDs, servos, buzzer, keypad, sonar, display and the state machine we will 
# use to combine all these elements
class Biped():

    # Class constructor, sets SPI and LED and Servo pins on the shifter, initializes the rest of the components
    def __init__(self):
        spi = board.SPI()
        spi.try_lock()
        spi.configure(baudrate=500000)
        spi.unlock()

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

    # Getter method to check if servos are correctly connected
    def get_servo(self, servo_pin):
        if not self._servos.get(servo_pin):
            raise exceptions.ServoNotConnected

        return self._servos[servo_pin]
    
    # Returns servo properties
    @property
    def servos(self):
        return self._servos.values()

    # Getter method which returns at led_pin
    def get_led(self, led_pin):
        return self._leds[str(led_pin)]

    # Returns LED properties
    @property
    def leds(self):
        return self._leds.values()

    # Getter method for buzzer
    @property
    def buzzer(self):
        return self._buzzer

    # Getter method for keypad
    @property
    def keypad(self):
        return self._keypad

    # Getter method for sonar
    @property
    def sonic_sensor(self):
        return self._sonic_sensor

    # Getter method for LCD
    @property
    def display(self):
        return self._display

    # Getter method for current state
    @property
    def state(self):
        return self._state

    # Setter method for current state
    @state.setter
    def state(self, value):
        self._state = value
        self._state.on_enter()

    # Getter method for previous state
    @property
    def previous_state(self):
        return self._previous_state

    # Setter method for previous state
    @previous_state.setter
    def previous_state(self, value):
        self._previous_state = value

# Creates an instantiation of Biped
biped = Biped()

# Records current time to be used to switch between states
current_time = time.monotonic()

# Set global variable for sonar
sonar_distance = 21
previous_sonar_time = current_time

# Set global variables for keypad
key_pressed = biped.keypad.get_pressed()
previous_key_pressed = key_pressed
previous_key_time = current_time
keypad_delay = 1

# Sets the time delay value between states
delay = 0.2
next_time = time.monotonic() + delay

# Waits until key on keypad is pressed to move to next state and continually checks sonar
while (biped.keypad.get_pressed() is not components.Keys.ZERO):
    # Sets current time variable
    time.sleep(max(0, next_time - time.monotonic()))
    current_time = time.monotonic()

    # Checks which keys are pressed on the keypad, and updates next state depending on the key pressed
    key_pressed = biped.keypad.get_pressed()
    if (key_pressed != None and current_time - previous_key_time >= keypad_delay):
        biped.state.on_key_change(key_pressed)
        previous_key_pressed = key_pressed
        previous_key_time = current_time
    
    # Checks sonar readings and acts based on its values, going into an "Aggress" state if anything gets too close
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

    # Goes to the next state in the state machine
    biped.state.update(current_time)
    biped.display.canvas.update()

    next_time += (time.monotonic() - next_time) // delay * delay + delay
########## End of main.py ##########

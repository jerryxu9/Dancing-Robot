import board
import pulseio
import digitalio
import time

import lib.adafruit_hcsr04 
import lib.adafruit_motor.servo
import lib.adafruit_matrixkeypad
import lib.adafruit_74hc595

class SonicSensor():
    def __init__(self, trigger, echo):
        self._trigger = digitalio.DigitalInOut(trigger)
        self._trigger.direction = digitalio.Direction.OUTPUT

        self._echo = pulseio.PulseIn(echo)
        self._echo.pause()
        self._echo.clear()

        self._previous_distance = 30
        self._previous_trigger_time = 0
        self._previous_echo_time = 0

        self._in_progress = False
        self._counter = 0

    def start(self, current_time):
        if (self._in_progress == True):
            return self.poll(current_time)

        self._echo.clear()

        self._trigger.value = True
        if (current_time - self._previous_trigger_time >= 0.0001):
            self._trigger.value = False
            self._previous_trigger_time = current_time
        else:
            return None
        
        self._echo.resume()
        self._previous_echo_time = current_time
        self._in_progress = True

    def poll(self, current_time):
        if not self._echo:
            return None

        self._echo.pause()

        if (self._echo[0] >= 65535):
            self._previous_distance = 200

        self._in_progress = False
        self._previous_distance = self._echo[0] * 0.017
        return self._previous_distance
class Servo():
    def __init__(self, pin):
        pwm = pulseio.PWMOut(pin, duty_cycle=2 ** 15, frequency=50)
        self._adafruit_servo = lib.adafruit_motor.servo.Servo(pwm)

    def duty_rotate(self, duty_cycle):
        self._adafruit_servo.angle = self._angle(duty_cycle)

    def angle_rotate(self, angle):
        self._adafruit_servo.angle = angle
        
    def _angle(self, duty_cycle):	
        if duty_cycle is None:
            return None
        
        return 18 * (duty_cycle - 2.5)
    
    def reset(self):
        self.angle_rotate(90)
    
class Keys():
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    STAR = 10
    HASHTAG = 11
    
    @classmethod
    def to_dance(cls, key):
        #circuitpython microcontrollers don't support "enum" from the python standard library
        if key is cls.ONE:
            return "shapeofyou"
        elif key is cls.TWO:
            return "badguy"
        elif key is cls.THREE:
            return "dance1"
        elif key is cls.FOUR:
            return "dance4"
        elif key is cls.FIVE:
            return "dance5"
        elif key is cls.SIX:
            return "dance6"
        
        return None

    @classmethod
    def from_list(cls, list):
        key_pressed = None
            
        if (len(list) == 5):
            list.remove('1')
            list.remove('4')
            list.remove('7')
            list.remove('10')
            key_pressed = list[0]
        elif (len(list) == 1):
            key_pressed = list[0]

        if (len(list) >= 4 or len(list) == 0 or len(list) == 3 or len(list) == 2):
            return None

        return int(key_pressed)

class KeyPad():
    def __init__(self):
        self._cols = [digitalio.DigitalInOut(x) for x in (board.D13, board.D11, board.D1)]
        self._rows = [digitalio.DigitalInOut(x) for x in (board.D2, board.A2, board.A3, board.D4)]
        self._keys = (('1', '2', '3'),
                      ('4', '5', '6'),
                      ('7', '8', '9'),
                      ('10', '0', '11'))
        self._keypad = lib.adafruit_matrixkeypad.Matrix_Keypad(self._rows, self._cols, self._keys)
        self.pressed = Keys.ONE
        #init keypad (interface with pins)

    def get_pressed(self):
        keys = self._keypad.pressed_keys
        return Keys.from_list(keys)
    
class Shifter():
    def __init__(self, latch, spi):
        self._latch = digitalio.DigitalInOut(latch)
        self._shift_register = lib.adafruit_74hc595.ShiftRegister74HC595(spi, self._latch)

    def get_pin(self, pin):
        return self._shift_register.get_pin(pin)

class LED():
    def __init__(self, shifter, pin):
        self._led = shifter.get_pin(pin)

    def is_on(self):
        return self._led.value == True

    def on(self):
        self._led.value = True
        
    def off(self):
        self._led.value = False
        
class Buzzer():	
    def __init__(self, pin):
        self._buzzer = pulseio.PWMOut(pin, variable_frequency=True)
        self._buzzer.duty_cycle = 2**15
    
    def frequencyVal(self):
        return self._buzzer.frequency

    def frequency(self, value):
        self._buzzer.frequency = value
        
    def off(self):
        self.frequency(Note.notes["ZERO"])
        
class Note():
    notes = {
        "B0": 31,
        "C1": 33,
        "CS1": 35,
        "D1": 37,
        "DS1": 39,
        "E1": 41,
        "F1": 44,
        "FS1": 46,
        "G1": 49,
        "GS1": 52,
        "A1": 55,
        "AS1": 58,
        "B1": 62,
        "C2": 65,
        "CS2": 69,
        "D2": 73,
        "DS2": 78,
        "E2": 82,
        "F2": 87,
        "FS2": 93,
        "G2": 98,
        "GS2": 104,
        "A2": 110,
        "AS2": 117,
        "B2": 123,
        "C3": 131,
        "CS3": 139,
        "D3": 147,
        "DS3": 156,
        "E3": 165,
        "F3": 175,
        "FS3": 185,
        "G3": 196,
        "GS3": 208,
        "A3": 220,
        "AS3": 233,
        "B3": 247,
        "C4": 262,
        "D4": 294,
        "CS4": 277,
        "DS4": 311,
        "E4": 330,
        "F4": 349,
        "FS4": 370,
        "G4": 392,
        "GS4": 415,
        "A4": 440,
        "AS4": 466,
        "B4": 494,
        "C5": 523,
        "CS5": 554,
        "D5": 587,
        "DS5": 622,
        "E5": 659,
        "F5": 698,
        "FS5": 740,
        "G5": 784,
        "GS5": 831,
        "A5": 880,
        "AS5": 932,
        "B5": 988,
        "C6": 1047,
        "CS6": 1109,
        "D6": 1175,
        "DS6": 1245,
        "E6": 1319,
        "F6": 1397,
        "FS6": 1480,
        "G6": 1568,
        "GS6": 1661,
        "A6": 1760,
        "AS6": 1865,
        "B6": 1976,
        "C7": 2093,
        "CS7": 2217,
        "D7": 2349,
        "DS7": 2489,
        "E7": 2637,
        "F7": 2794,
        "FS7": 2960,
        "G7": 3136,
        "GS7": 3322,
        "A7": 3520,
        "AS7": 3729,
        "B7": 3951,
        "C8": 4186,
        "CS8": 4435,
        "D8": 4699,
        "DS8": 4978,
        "ZERO": 1000000
    }

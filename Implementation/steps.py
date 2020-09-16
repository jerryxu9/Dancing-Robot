import exceptions
import logger

class Step():
    def __init__(self, seconds):
        self._seconds = seconds
    
    @property
    def seconds(self):
        return self._seconds
    
    @property
    def async_(self):
        pass
    
    def execute(self, biped):
        pass
    
    def dispose(self, biped):
        pass
    
class AsyncStep(Step):
    def __init__(self, seconds):
        super().__init__(seconds)
        self._start_time = None
        
    @property
    def async_(self):
        return True
    
    @property
    def start_time(self):
        return self._start_time
    
    @start_time.setter
    def start_time(self, value):
        self._start_time = value
        
class SyncStep(Step):
    def __init__(self, seconds):
        super().__init__(seconds)
    
    @property
    def async_(self):
        return False
    
        
class LEDStep(AsyncStep):
    def __init__(self, seconds, led_pins):
        super().__init__(seconds)
        self._led_pins = led_pins
        
    def execute(self, biped):
        for led_pin in self._led_pins:
            led = biped.get_led(led_pin)
            led.on()
    
    def dispose(self, biped):
        for led_pin in self._led_pins:
            led = biped.get_led(led_pin)
            led.off()
    
class BuzzerStep(SyncStep):
    def __init__(self, seconds, counter, buzzer_pins, frequency):
        super().__init__(seconds)
        self._buzzer_pins = buzzer_pins
        self._frequency = frequency
        self._counter = counter
        
    def execute(self, biped):
        for buzzer_pin in self._buzzer_pins:
            buzzer = biped.buzzer
            buzzer.frequency(self._frequency)
            
    def dispose(self, biped):
        for buzzer_pin in self._buzzer_pins:
            buzzer = biped.buzzer
            buzzer.off()

class ServoStep(SyncStep):
    def __init__(self, seconds, servo_pins):
        super().__init__(seconds)
        self._servo_pins = servo_pins
    
    @property
    def servo_pins(self):
        return self._servo_pins
    
class RotationalStep(ServoStep):
    def __init__(self, seconds, servo_pins):
        super().__init__(seconds, servo_pins)
        
    @property	
    def angle(self):
        pass
    
    def execute(self, biped):
        for servo_pin in self._servo_pins:
            try:
                servo = biped.get_servo(servo_pin)
                servo.duty_rotate(self.angle)
            except exceptions.ServoNotConnected:
                return#Logger.LOG.critical("Servo pin " + str(servo_pin) + " not connected")
    
class PauseStep(RotationalStep):
    def __init__(self, seconds, servo_pins):
        super().__init__(seconds, servo_pins)

    @property
    def angle(self):
        return None
            
class RotateStep(RotationalStep):
    def __init__(self, seconds, servo_pins, angle):
        super().__init__(seconds, servo_pins)
        self._angle = angle
    
    @property
    def angle(self):
        return self._angle
    
    
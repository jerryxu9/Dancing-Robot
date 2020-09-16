############################## Start of steps.py ##############################

import exceptions
import logger
import time

# Parent class of BuzzerStep and ServoStep
class Step():
    def __init__(self, seconds):
        self._seconds = seconds
    
    @property
    def seconds(self):
        return self._seconds

    def execute(self, biped):
        pass
    
    def dispose(self, biped):
        pass

# Allows buzzer action to be executed or to be turned off
class BuzzerStep(Step):
    def __init__(self, seconds, frequency):
        super().__init__(seconds)
        self._frequency = frequency
        
    def execute(self, biped):
        biped.buzzer.frequency(self._frequency)
            
    def dispose(self, biped):
        buzzer = biped.buzzer
        buzzer.off()

# Allows servo move to be executed or turned off, parent class of RotationalStep and PauseStep
class ServoStep(Step):
    def __init__(self, seconds, servo_pins):
        super().__init__(seconds)
        self._servo_pins = servo_pins
    
    @property
    def servo_pins(self):
        return self._servo_pins

# A certain type of servo step where the foot is rotated, parent class of RotateStep
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
                angle_ = servo.current_angle + servo.get_delta(self.angle, self._seconds)
                if (angle_ >= 180):
                    angle_ = 179
                elif (angle_ <= 0):
                    angle_ = 1
                servo.angle_rotate(angle_)
            except exceptions.ServoNotConnected:
                return#Logger.LOG.critical("Servo pin " + str(servo_pin) + " not connected")

# A certain type of servo step where the movement is paused
class PauseStep(RotationalStep):
    def __init__(self, seconds, servo_pins):
        super().__init__(seconds, servo_pins)

    @property
    def angle(self):
        return None

# This step rotates foot of biped
class RotateStep(RotationalStep):
    def __init__(self, seconds, servo_pins, angle):
        super().__init__(seconds, servo_pins)
        self._angle = angle
    
    @property
    def angle(self):
        return self._angle
############################## end of steps.py ################################
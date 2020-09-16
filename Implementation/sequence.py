from Steps import *
from Components import Note

class Sequence():
    def __init__(self, sequence_file_name):
        self._sequence_file_name = sequence_file_name
        self._length = 0
        self._steps = self._load_steps()
        
    def _load_steps(self):
        steps = []
        counter = 0
        with open(self._sequence_file_name) as sequence_file:
            for line in sequence_file.readlines():
                counter = counter + 1
                step = self._interpret_line(counter, line)
                if step is not None:
                    steps.append(step)
        return steps
        
    def _interpret_line(self, counter, line):
        if ":" not in line:
            return None
        
        operation = line.split(":")
        command = operation[0]
        pins = operation[1].split(",")
        seconds = float(operation[2])
        
        if ("async" not in command):
            self._length = self._length + 1
        
        if ("rotate" in command):
            angle = float(operation[3])
            seconds = seconds
            return RotateStep(seconds, pins, angle)
        elif ("pause" in command):
            seconds = 0
            return PauseStep(seconds, pins)
        elif ("LED" in command):
            return LEDStep(seconds, pins)
        elif ("buzzer" in command):
            note = operation[3].strip()
            seconds = seconds / 2.7
            return BuzzerStep(seconds, counter, pins, Note.notes.get(note))
        
        return None
    
    @property
    def length(self):
        return self._length
    
    @property
    def steps(self):
        return self._steps
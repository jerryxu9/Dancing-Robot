############################## Start of sequence.py ##############################

from Steps import *
from Components import Note

# The sequence class determines which step to take based on the sequence read from the dance sequence files
class Sequence():
    def __init__(self, sequence_file_name):
        self._sequence_file_name = sequence_file_name
        self._length = 0
        self._steps = self._load_steps()
        self._tempo = 0
        
    # Reads values from sequence text files and stores in a list
    def _load_steps(self):
        steps = []
        with open(self._sequence_file_name) as sequence_file:
            for line in sequence_file.readlines():
                step = self._interpret_line(line)
                if step is not None:
                    steps.append(step)
        return steps
        
    # Parses the values from the sequence text files and interprets the commands
    def _interpret_line(self, line):
        if ":" not in line:
            return None
        
        operation = line.split(":")
        command = operation[0]

        if ("tempo" in command):
            self._tempo = float(operation[1])
            return None
        elif ("buzzer" in command):
            seconds = float(operation[1]) / self._tempo
            note = operation[2].strip()
            return BuzzerStep(seconds, Note.notes.get(note))

        pins = operation[1].split(",")
        seconds = float(operation[2])

        if ("rotate" in command):
            angle = float(operation[3])
            seconds = seconds
            return RotateStep(seconds, pins, angle)
        elif ("pause" in command):
            return PauseStep(seconds, pins)
        elif ("LED" in command):
            return LEDStep(seconds, pins)
        
        return None
    
    # Getter method which returns the current step to execute
    @property
    def steps(self):
        return self._steps
############################## End of sequence.py ##############################
import time
import board
import pulseio
aaaaa
class Buzzer():
  def __init__(self):
    self.buzz()

  def buzz(self):

    # Define a list of tones/music notes to play.
    TONE_FREQ = [ 262,  # C
                  262,  # C
                  294,  # D
                  262,  # C
                  349,  # F
                  330,  # E

                  262,  # C
                  262,  # C
                  294,  # D
                  262,  # C
                  392,  # G
                  349,  # F

                  262,
                  262,
                  523,
                  392,
                  349,
                  349,
                  330,
                  294,

                  466,
                  466,
                  440,
                  349,
                  392,
                  349 ]

    # Create piezo buzzer PWM output.
    buzzer = pulseio.PWMOut(board.A1, variable_frequency=True)

    # Start at the first note and start making sound.
    buzzer.frequency = TONE_FREQ[0]
    buzzer.duty_cycle = 2**15  # 32768 value is 50% duty cycle, a square wave.

    # Main loop will go through each tone in order up and down.
    while True:
        # Play tones going from start to end of list.
        for i in range(len(TONE_FREQ)):
            buzzer.frequency = TONE_FREQ[i]
            time.sleep(0.5)  # Half second delay.
        # Then play tones going from end to start of list.
        for i in range(len(TONE_FREQ)-1, -1, -1):
            buzzer.frequency = TONE_FREQ[i]
            time.sleep(0.5)



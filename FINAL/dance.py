############################## Start of dance.py ##############################

import sequence
import time
import random

# Controls the dancing of the biped by taking biped, song_file and dance_file as parameters to determine sequence of moves
class Dance():
	# Constructor initializes instance variables of the class
	def __init__(self, biped, song_file, dance_file):
		self._biped = biped
		self._song = song_file.split(".")[0].replace("_song", '').replace("sequences/", '')
		self._song_sequence = sequence.Sequence(song_file)
		self._dance_sequence = sequence.Sequence(dance_file)

		self._finished = False
		
		self._song_step_number = 0
		self._current_song_step = self._song_sequence.steps[0]
		self._previous_song_step_time = 0.0

		self._dance_step_number = 0
		self._current_dance_step = self._dance_sequence.steps[0]
		self._previous_dance_step_time = 0.0

	# Getter method which returns the name of the song
	@property
	def song(self):
		return self._song
		
	# Executes current dance step by using the current time to determine which step to do next from the dance_file
	def step(self, current_time):
		self._current_song_step.execute(self._biped)
		self._current_dance_step.execute(self._biped)
		
		if (self._current_song_step.seconds <= current_time - self._previous_song_step_time):
			self._song_step_number += 1
			if (self._song_step_number >= len(self._song_sequence.steps) - 1):
				self._finished = True
				return

			self._current_song_step = self._song_sequence.steps[self._song_step_number]
			self._previous_song_step_time = current_time

		if (self._current_dance_step.seconds <= current_time - self._previous_dance_step_time):
			self._dance_step_number += 1
			if (self._dance_step_number >= len(self._dance_sequence.steps) - 1):
				self._dance_step_number = 0

			for servo_pin in self._current_dance_step.servo_pins:
				servo = self._biped.get_servo(servo_pin)
				if (self._current_dance_step.angle != None):
					servo.start_angle = self._current_dance_step.angle

			self._current_dance_step = self._dance_sequence.steps[self._dance_step_number]
			self._previous_dance_step_time = current_time

		for led in self._biped.leds:
			if led.pin == 5:
				continue

			on = bool(random.getrandbits(1))
			if (on):
				led.on()
			else:
				led.off()
		
	# Getter method which returns whether current dance move is finished or not
	@property
	def finished(self):
		return self._finished
############################## End of dance.py ################################
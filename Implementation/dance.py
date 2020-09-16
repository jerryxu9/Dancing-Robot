import sequence
import time

class Dance():
	def __init__(self, biped, dance_file):
		self._biped = biped
		self._song = dance_file.split(".")[0]
		self._sequence = sequence.Sequence(dance_file)
		#print(self._sequence.length)
		
		self._current_async_steps = []

		self._finished = False
		
		self._step_number = 0
		self._current_step = self._sequence.steps[0]
		self._previous_step_time = 0.0

	@property
	def song(self):
		return self._song
		
	def step(self, current_time):
		if (not self._current_step.async_):
			self._current_step.execute(self._biped)
		
		if (self._current_step.seconds <= current_time - self._previous_step_time):
			self._step_number = self._step_number + 1
			if self._step_number >= self._sequence.length - 1:
				self._finished = True
				return

			self._current_step = self._sequence.steps[self._step_number]

			if (self._current_step.async_):
				self._current_step.start_time = current_time
				self._current_async_steps.append(self._current_step)
			
			self._previous_step_time = current_time
		
		for index in range(len(self._current_async_steps) - 1, -1, -1):
			async_step = self._current_async_steps[index]
			if (async_step.seconds <= current_time - async_step.start_time):
				async_step.dispose(self._biped)
				del self._current_async_steps[index]
			else:
				async_step.execute(self._biped)
			
	@property
	def current_step(self):
		return self._current_step
	
	@property
	def finished(self):
		return self._finished
	
		
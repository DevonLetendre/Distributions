from random import randrange

'''
The Distribution class models a distribution and provides methods
which allow a user to interact with the distribution. 

'''

class Distribution:	
	def __init__(self):
		self.dict = {}
		self.eventspace = 0
		self._L = []
		self.flag = None
		self.leftoff_at = 1
		self.slider_begin = 0
		self.slider_end = 0

	def _numevent(self, e):
		#Factotred out repetition
		return self.dict[e][1] - self.dict[e][0] + 1

	def add(self, e, multiplicity = 1):
		'''
		Updates the Distribution to add the event e. The second parameter,
		multiplicity counts how many "copies" of e to add. The default 
		multiplicity is 1, i.e. single events.
		'''
		self.flag = True
		self.eventspace += multiplicity

		if e in self.dict:
			temp = self.dict[e]
			self.dict[e] = [self.leftoff_at, self.leftoff_at + 
							multiplicity + self._numevent(e) - 1]
			self.leftoff_at = self.leftoff_at + self._numevent(e) + multiplicity
		else:
			self.dict[e] = [self.leftoff_at, self.leftoff_at + multiplicity - 1]
			self.leftoff_at = self.leftoff_at + multiplicity

	def count(self, e):
		'''
		Returns the number of events that are e.
		'''
		return self._numevent(e)

	def prob(self,e):
		'''
		Return the fraction of the total events that are e .
		'''
		if self.eventspace > 0:
			return (self._numevent(e))/ self.eventspace
		else:
			raise ZeroDivisionError 

	def sample(self):
		'''
		Returns an event from the distribution. The returned results are 
		randomly selected and the probability of a given an event e 
		is prob(e).
		'''
		if self.flag:
			self._L = sorted(self.dict.items(), key=lambda x: x[1])
			self.slider_begin = self._L[0][1][0]
			self.slider_end = self._L[-1][1][1]
			self.flag = False
			
		return self._modified_bs(randrange(self.slider_begin, self.slider_end + 1))
	
	def _modified_bs(self, rand):
		'''
		A modified binary search
		'''
		left = 0 
		right = len(self._L)

		while True:
			mid = (right + left) // 2
			if rand >= self._L[mid][1][0] and rand <= self._L[mid][1][1]:
				return self._L[mid][0]
			elif rand < self._L[mid][1][0]:
				right = mid
			elif rand > self._L[mid][1][1]:
				left = mid

	def __len__(self):
		'''
		Returns the number of distinct events.
		'''
		return len(self.dict)

	def __str__(self):
		return str(self.dict)


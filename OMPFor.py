import random
import functools

class OMPFor(object):
	"""implementation for openmp for directive - OMPFor"""
	def __init__(self, args = tuple(), kwargs = dict()):
		super(OMPFor, self).__init__()
		self.__args = args
		self.__kwargs = kwargs
		self.__numProcs = kwargs["poolCount"]
		self.__procId = kwargs["procId"]

	def __call__(self, target):
		""" decorator function for the target For function """

		def wrapper(iterable, *args, **kwargs):

			if not hasattr(iterable, '__len__'):
				iterable = list(iterable)

			self.__iterable = iterable
			chunks = self.__getChunks()

			# current processess chunk of iterable
			chunk = self.__iterable[sum(chunks[:self.__procId]) : sum(chunks[:self.__procId + 1])]

			# execute the target function
			target(chunk, *self.__args, **self.__kwargs)

		return functools.wraps(target) (wrapper)	

	def __getChunks(self):
		""" get the chunks to be executed by each process """
		
		chunk, extra = divmod(len(self.__iterable), self.__numProcs)
		chunks = [chunk for i in range(self.__numProcs)]
		if extra:
			randIndex = random.randint(0, self.__numProcs - 1)
			chunks[randIndex] = chunks[randIndex] + extra
		return chunks

		
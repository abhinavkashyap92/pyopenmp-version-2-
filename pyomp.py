import OMPPool
import functools
import random

class OMPParallel(object):
	"""implemantation for parallel directive - OMPParallel"""
	def __init__(self, numprocs = None, condition = True, private = tuple(), shared = tuple(), firstprivate = tuple()):
		super(OMPParallel, self).__init__()
		self.numprocs = numprocs
		self.private = private
		self.shared = shared
		self.firstprivate = firstprivate
		self.condition = condition

	def __call__(self, target):
		""" decorator function for the target function """

		def wrapper(*args, **kwargs):
			# check the condition
			if not self.condition:
				# condition is false so dont create team of processes
				apply(target, args, kwargs)
			else:
				# condition is true, create team of processes
				pool = OMPPool.OMPPool(numprocs = self.numprocs, target = target, args = args, kwargs = kwargs)
				pool.start()
				pool.join()

		return functools.wraps(target) (wrapper)

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

class OMPMaster(object):

	def __init__(self,args=tuple(),kwargs = tuple()):
		self.__args = args
		self.__kwargs = kwargs
		self.proc_id = kwargs["procId"]

	def __call__(self,function):

		def wrapper(*args,**kwargs):

			if self.proc_id == 0:
				function(*self.__args,**self.__kwargs)
			else:
				pass

		return wrapper

if __name__ == '__main__':
	
	list_ = [1,2,3,4,5,6,7,8]
	@OMPParallel(numprocs = 4)
	def parallel_block(*args,**kwargs):
		print "Hello world"
		@OMPFor(args = args, kwargs = kwargs)
		def for_block(list_ ,*args,**kwargs):
			for i in list_:
				print i
		for_block(list_)

	parallel_block()

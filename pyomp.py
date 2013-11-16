from OMPPool import *
import functools
import random
from clauses import *

class OMPParallel(object):
	"""implemantation for parallel directive - OMPParallel"""
	def __init__(self, numprocs = None, condition = True, private = None, shared = None, firstprivate = None):
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
				if self.private: 
					self.private = ClausePrivate(self.private).make_junk()
					print "self.private: ",self.private
					
				
				OMPParallel.pool = OMPPool(numprocs = self.numprocs, target = target, args = args, kwargs = kwargs)
				OMPParallel.pool.start()
				OMPParallel.pool.join()

		return functools.wraps(target) (wrapper)

	@classmethod
  	def returnPool(cls):
  		return OMPParallel.pool

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
		self.procId = kwargs["procId"]

	def __call__(self,function):

		def wrapper(*args,**kwargs):
			if self.procId == 0:
				function(*self.__args,**self.__kwargs)
			else:
				pass
		return wrapper

class OMPSingle(OMPParallel):
	def __init__(self,args=tuple(),kwargs= tuple()):
		self.__args = args
		self.__kwargs = kwargs
		self.__procId = kwargs["procId"]
		self.__numProcs = kwargs["poolCount"]
		self.__randomProcessNumber = kwargs["randomProcessNumber"]
		self.__pool = OMPParallel.returnPool()
		self.__eventForSingleExecution = kwargs["eventForSingleExecution"]
		self.__eventForSingleEncounter = kwargs["eventForSingleEncounter"]		

	def __call__(self, function):
		def wrapper(*args, **kwargs):
			if self.__procId == self.__numProcs - 1:
				self.__eventForSingleEncounter.set()

			self.__eventForSingleEncounter.wait()
			if self.__procId == self.__randomProcessNumber:
				function(*self.__args,**self.__kwargs)
				self.__eventForSingleExecution.set()			

			else:
				self.__pool.getProcessForID(self.__procId).wait(self.__eventForSingleExecution)
			
		return wrapper

	

if __name__ == '__main__':
	
	
	list_ = [1,2,3,4,5,6,7,8]
	private_dict = {"m":1,"n":2}
	@OMPParallel(numprocs =2,private= private_dict)
	def parallel_block(*args,**kwargs):
		print "hello world"
		@OMPSingle(args = args, kwargs = kwargs)
		def single_block(*args,**kwargs):
			print "inside single block", kwargs["procId"]
		single_block()
		print "After single block: ",kwargs["procId"]
		
		@OMPSingle(args=args,kwargs=kwargs)
		def single_block2(*args,**kwargs):
			print "inside the single block 2: ",kwargs["procId"]
		single_block2()
		print "after the single block 2: ",kwargs["procId"]

	parallel_block()

	@OMPParallel(numprocs=3)
	def foo(*args,**kwargs):
		@OMPFor(args= args, kwargs=kwargs)
		def for_block(a,*args,**kwargs):
			for i in a:
				print str(i) + ": "+ str(kwargs["procId"])
		for_block(list_)

	foo()

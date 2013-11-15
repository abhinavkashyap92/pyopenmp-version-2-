import OMPPool
import functools

class OMPParallel(object):
	"""implemantation for parallel directive - OMPParallel"""
	def __init__(self, numprocs = None, condition = False, private = tuple(), shared = tuple(), firstprivate = tuple()):
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

if __name__ == '__main__':
	
	@OMPParallel(numprocs = 10, condition = True)
	def parallel_block(*args, **kwargs):
		print "hello"

	parallel_block()
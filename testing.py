from pyomp import *

def main():
	@OMPParallel(numprocs = 10, condition = True)
	def parallel_block(*args, **kwargs):
		a = [i for i in range(20, 80, 3)]
		@OMPFor(args=args, kwargs=kwargs)
		def for_block(a, *args, **kwargs):
			for i in a:
				print str(i) + " process ID: " + str(kwargs["procId"])

		for_block(a)
if __name__ == '__main__':
	main()
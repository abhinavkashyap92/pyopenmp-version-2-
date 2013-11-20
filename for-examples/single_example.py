import sys
sys.path.insert(0, "../")
from pyomp import *


def main():

	@OMPParallel(numprocs = 4)
	def parallel_block(*args,**kwargs):
		print "inside parallel block"
		@OMPSingle(args=args,kwargs=kwargs)
		def single_block(*args,**kwargs):
			print "inside first single block id: ",kwargs["procId"]
		single_block()
		print "after the first single block"
	parallel_block()



if __name__ == '__main__':
	main()
import sys
sys.path.insert(0, "../")
from pyomp import *


def main():

	@OMPParallel(numprocs = 4)
	def parallel_block(*args,**kwargs):
		print "inside parallel block"
		@OMPMaster(args=args,kwargs=kwargs)
		def master_block(*args,**kwargs):
			print "inside first master block id: ",kwargs["procId"]
		master_block()
	parallel_block()



if __name__ == '__main__':
	main()
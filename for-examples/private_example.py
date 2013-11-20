import sys
sys.path.insert(0, "../")
from pyomp import *
from clauses import *

def main():

	private_dict = {"a":1,"b":2}

	@OMPParallel(numprocs = 4,private=private_dict)
	def parallel_block(*args,**kwargs):
		private_dict["a"] = 0
		print str(private_dict) + ": " + str(kwargs["procId"])
	parallel_block()


if __name__ == '__main__':
	main()
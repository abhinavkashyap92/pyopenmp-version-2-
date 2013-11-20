import sys
import time
import random
sys.path.insert(0, '../')
from src.pyomp import * 

def fill_list(size):
	arr = []
	for i in range(size):
		arr.append([])
		for j in range(size):
			arr[i].append(random.randint(1,100))

	return arr
	
def print_list(a):
	print "["
	for i in a:
		print "\t" + str(i)
	print "]"

def main():

	a = fill_list(500)
	b = fill_list(500)
	c = fill_list(500)

	#create a team of processes
	@OMPParallel(numprocs=4)
	def parallel_blk(*args, **kwargs):

		# for directive to share the work
		@OMPFor(args=args, kwargs=kwargs)
		def for_blk_one(a, *args, **kwargs):
			for i in range(kwargs["start"], kwargs["end"]):
				for j in range(len(b)):
					sum = 0 
					for k in range(len(a)):
						sum = sum + a[i][k] * b[k][j]
					c[i][j] = sum
		for_blk_one(a)	
	parallel_blk()
if __name__ == '__main__':
	start = time.time()
	main()
	print str(time.time() - start) + "seconds"

import sys
sys.path.insert(0, "../")
from pyomp import *

def main():

	a = [
			list(range(1, 4, 1)), 
	 		list(range(4, 7, 1)), 
	 		list(range(7, 10, 1))
	 	]
	b = [
			list(range(1, 4, 1)), 
	 		list(range(4, 7, 1)), 
	 		list(range(7, 10, 1))
	 	]
	c = [
			list(range(3)),
			list(range(3)), 
			list(range(3))
		]

	#create a team of processes
	@OMPParallel(numprocs=4)
	def parallel_blk(*args, **kwargs):

		# for directive to share the work
		@OMPFor(args=args, kwargs=kwargs)
		def for_blk_one(a, *args, **kwargs):
			if not kwargs["start"] == kwargs["end"]:
				for i in range(kwargs["start"], kwargs["end"]):
					arr1 = a[i]
					for j in range(len(b)):
						arr2 = [item[j] for item in b]
						sum = 0 
						for k in range(len(a)):
							sum = sum + arr1[k] * arr2[k]
						c[i][j] = sum
				print "procId: " + str(kwargs["procId"]) + "\tc: " + str(c)
		for_blk_one(a)	
	parallel_blk()
if __name__ == '__main__':
	main()
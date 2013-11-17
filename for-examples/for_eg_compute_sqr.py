from pyomp import *

def main():
	
	list_ = list(range(1, 10, 1))
	res = list(range(9))

	@OMPParallel(numprocs=4)
	def foo(*args,**kwargs):

		@OMPFor(args= args, kwargs=kwargs)
		def for_block(a,*args,**kwargs):
			for i in range(kwargs["start"], kwargs["end"]):
				res[i] = a[i] ** 2
				print "processId: " + str(kwargs["procId"]) + "\ta: " + \
				str(a[i]) + "\tres: " + str(res[i]) 
			
		for_block(list_)
			
	foo()
if __name__ == '__main__':
	main()
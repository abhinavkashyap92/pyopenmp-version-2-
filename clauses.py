import random
"""
	*Private class for implementing the private clause
	*
	* 
"""

class ClausePrivate(object):

	"""
		* Parmeters
			- private_args(type - list) - the arguments which have to be private for each process
			
	"""
	def __init__(self,private_args):
		self.__args = private_args

	def  make_junk(self):
		return_list = list()
		args_len = len(self.__args)
		for i in xrange(args_len):
			random.seed()
			self.__args[i] = random.randint(0,10000)

		return self.__args

if __name__ == "__main__":

	private_list = [1,2,3]
	privateObj = ClausePrivate(private_list)
	print privateObj.make_junk()
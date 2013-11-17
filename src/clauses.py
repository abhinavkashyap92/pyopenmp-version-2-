import random
import multiprocessing
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
		for key in self.__args.keys():
			random.seed()
			self.__args[key] = random.randint(0,10000)

		return self.__args
if __name__ == "__main__":

	private_list = [1,2,3]
	privateObj = ClausePrivate(private_list)
	print privateObj.make_junk()

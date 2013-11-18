import time
import random
def fill_list(size):
	arr = []
	for i in range(size):
		arr.append([])
		for j in range(size):
			arr[i].append(j)

	return arr
	
def print_list(a):
	print "["
	for i in a:
		print "\t" + str(i) + ","
	print "]"

def main():
	a = fill_list(500)
	b = fill_list(500)
	c = fill_list(500)

	for i in range(len(a)):
		for j in range(len(b)):
			sum = 0
			for k in range(len(a)):
				sum = sum + a[i][k] * b[k][j]
			c[i][j] = sum

if __name__ == '__main__':
	start = time.time()
	main()
	print str(time.time() - start) + "seconds"

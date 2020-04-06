import numpy as np


def generate_flow_matrix(file_name):

	# As the lines do not have the same separation pattern, one must deal with each one separately
	file = open(file_name, 'r')
	lines = file.readlines()

	cities_flow = []
	codes = []

	# For each file line, discard the text and keep only the numbers of city codes and flow 
	for line in lines:
		# break line into list
		line = line.split()
		only_numbers = []
		for i in range(len(line)):

			# Checks whether it is an integer
			try:
				val = int(line[i])
				only_numbers.append(val)

				if(i < len(line)-1):
					codes.append(val)

			# Checks whether it is a float number
			except ValueError:
				try:
					val = float(line[i])
					only_numbers.append(val)

					if(i < len(line)-1):
						codes.append(val)
				except:
					pass

		# if list not empty, append to the cities
		if(only_numbers):
			cities_flow.append(only_numbers)




	# List only ordered unique codes for cities
	codes = np.array(codes)
	codes = np.unique(codes)

	# Numer of unique cities
	N = len(codes)

	print('ORIGINAL DATA: N=', N)

	# flow matrix
	flow_matrix = np.zeros((N,N))

	for flow in cities_flow:
		lin = np.where(codes == flow[0])[0][0]
		col = np.where(codes == flow[1])[0][0]

		flow_matrix[lin,col] = flow[2]

	return flow_matrix, codes
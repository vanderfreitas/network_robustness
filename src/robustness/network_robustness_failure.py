# -*- coding: utf-8 -*-

import igraph as ig
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib



########### LOADING INPUT FILES ##############
import sys
sys.path.append('../')
from data_files import Input_files

in_files = Input_files('../../') 
f_matrix_original = np.genfromtxt(in_files.get_network_file_name(),delimiter=';')
codes = np.genfromtxt(in_files.get_codes_file_name())
##############################################


relative_path = '../../results/' + in_files.get_project_name() + '/robustness/'



print('ROBUSTNESS: FAILURES')

N = len(codes)

data = np.genfromtxt('../../results/' + in_files.get_project_name() + '/metrics/avg_std.csv', delimiter=';') 

avg = data[0]
std = data[1]



# 3 thresholds
for thresh in [0, avg, avg+std]:
	f_matrix = f_matrix_original.copy()

	# Apply threshold
	for row in range(N):
		for col in range(N):
			if f_matrix[row][col] < thresh:
				f_matrix[row][col] = 0


	# Create graph, A.astype(bool).tolist() or (A / A).tolist() can also be used.
	g_original = ig.Graph.Adjacency( (f_matrix > 0.0).tolist())
	N = g_original.vcount()

	# Convert to undirected graph
	g_original = g_original.as_undirected()

	g_original.vs['label'] = codes  # or a.index/a.columns

	
	# random failures
	P_infty = np.zeros(N)

	number_removed = np.zeros(N)
	for i in range(g_original.vcount()):
		number_removed[i] = i / float(N)

	# Runs it 10 times
	simulations = 100

	P_infty_baseline = 0.0
	for sim in range(simulations):

		# Compute the network robustness to random failures ##

		# Make a copy of the network
		g = g_original.copy()

		# Find larger component
		cl = g.components()
		P_infty_baseline = float(max(cl.sizes()))

		P_infty[0] += 1.0

		count = 1
		while(g.vcount() > 1):
			index = int(random.random() * g.vcount())
			g.delete_vertices(index)

			cl = g.components()
			P_infty[count] += float(max(cl.sizes())) / P_infty_baseline 
			
			count = count + 1
		#######################################################

	# Compute the average
	P_infty = P_infty / float(simulations)

	# Save data to disk
	file = open(relative_path + 'robustness_failure_' + str(thresh) + '.csv', 'w')
	for i in range(N):
		file.write(str(number_removed[i]) + '\t' + str(P_infty[i]) + '\n')
	file.close()



	R = sum(P_infty) / N
	V = 0.5 - R

	file_out = open(relative_path + 'robustness_failure_R_V_' + str(thresh) + '.csv', 'w')
	#print(str(thresh) + ';' + str(R)  + ';' + str(V) )
	file_out.write(str(thresh) + ';' + str(R)  + ';' + str(V) + '\n')
	file_out.close()

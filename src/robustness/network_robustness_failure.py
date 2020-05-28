# -*- coding: utf-8 -*-

import igraph as ig
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib


from robustness import *



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

	

	# robustness
	number_removed,P_infty = robustness_failure_node(g_original, simulations=100)


	# Save data to disk
	file = open(relative_path + 'robustness_failure_' + str(thresh) + '.csv', 'w')
	for i in range(len(number_removed)):
		file.write(str(number_removed[i]) + '\t' + str(P_infty[i]) + '\n')
	file.close()



	R = sum(P_infty[1:]) / N
	V = 0.5 - R

	file_out = open(relative_path + 'robustness_failure_R_V_' + str(thresh) + '.csv', 'w')
	#print(str(thresh) + ';' + str(R)  + ';' + str(V) )
	file_out.write(str(thresh) + ';' + str(R)  + ';' + str(V) + '\n')
	file_out.close()

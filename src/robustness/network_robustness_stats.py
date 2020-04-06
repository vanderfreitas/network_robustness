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


N = len(codes)


relative_path_in = '../../results/' + in_files.get_project_name() + '/metrics/'
relative_path = '../../results/' + in_files.get_project_name() + '/robustness/'



print('ROBUSTNESS: ATTACKS USING THE NETWORK STATISTICS')




N = len(codes)

data = np.genfromtxt('../../results/' + in_files.get_project_name() + '/metrics/avg_std.csv', delimiter=';') 

avg = data[0]
std = data[1]


stats = ['degree', 'vuln']




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

	
	number_removed = np.zeros(N)
	for i in range(g_original.vcount()):
		number_removed[i] = i / float(N)
		

	for stat in stats:
		# Make a copy of the network
		g = g_original.copy()

		# Find larger component
		cl = g.components()
		P_infty_baseline = float(max(cl.sizes()))

		#print(relative_path_in + stat + '_' + str(thresh) + '.csv')
		st_data = np.genfromtxt(relative_path_in + stat + '_' + str(thresh) + '.csv', delimiter=';')


		# Compute the nodes' degrees and sort them
		stat_array = []
		for i in range(len(st_data)):
			stat_array.append( ( codes[i], float(st_data[i,1]) ) )


		dtype = [('label', int), ('stat', float)]
		stat_array = np.array(stat_array, dtype=dtype)
		stat_array = np.sort(stat_array, order='stat')
		stat_array = np.flip(stat_array)

		#print(stat_array)



		# Remove the node with higher degree (consider the degrees computed at the beginning)
		P_infty = np.zeros(N)
		P_infty[0] += 1.0

		count = 1
		while(g.vcount() > 1):
			index = g.vs.find(label=stat_array[count-1][0]).index
			#print "index: ", index
			g.delete_vertices(index)

			cl = g.components()
			P_infty[count] = float(max(cl.sizes())) / P_infty_baseline # / P_infty_baseline)
			count = count + 1
		#######################################################

		# Save data to disk
		file = open(relative_path + 'robustness_attack_' + stat + '_' + str(thresh) + '.csv', 'w')
		for i in range(N):
			file.write(str(number_removed[i]) + '\t' + str(P_infty[i]) + '\n')
		file.close()


		R = sum(P_infty) / N
		V = 0.5 - R

		file_out = open(relative_path + 'robustness_attack_' + stat + '_R_V_' + str(thresh) + '.csv', 'w')
		#print(str(thresh) + ';' + str(R)  + ';' + str(V) )
		file_out.write(str(thresh) + ';' + str(R)  + ';' + str(V) + '\n')
		file_out.close()
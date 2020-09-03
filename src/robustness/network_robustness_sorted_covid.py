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


N = len(codes)


relative_path_in = '../../results/sort_nodes_covid-19/'
relative_path = '../../results/' + in_files.get_project_name() + '/robustness/'



print('ROBUSTNESS: ATTACKS USING THE NETWORK STATISTICS')




N = len(codes)

data = np.genfromtxt('../../results/' + in_files.get_project_name() + '/metrics/avg_std.csv', delimiter=';') 

avg = data[0]
std = data[1]


# Three ways to measure the robustness
rob_measure_lbls = ["robustness_attack_sorted_covid_", "robustness_attack_sorted_covid_flow_sum_F_", "robustness_attack_sorted_covid_ncomp_"]



for ol in range(len(rob_measure_lbls)):

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
		

		if(in_files.get_project_name() == 'STATE'):
			file_name = relative_path_in + 'sorted_covid_cases_by_states.csv'
		elif(in_files.get_project_name() == 'SP'):
			file_name = relative_path_in + 'sorted_covid_cases_by_cities_SP.csv'
		elif(in_files.get_project_name() == 'MG'):
			file_name = relative_path_in + 'sorted_covid_cases_by_cities_MG.csv'
		else:
			file_name = relative_path_in + 'sorted_covid_cases_by_cities.csv'
		
		file_in = open(file_name, 'r')
		file_lines = file_in.readlines()
		file_in.close()

		data = []

		for i in range(len(file_lines)):
			ln = file_lines[i].strip()
			ln = ln.split(';')
			#print(ln)
			data.append( (int(ln[0]), int(ln[3])) )

		dtype = [('label', int), ('stat', int)]
		data = np.array(data, dtype=dtype)

		print(len(data))

		# robustness method
		if(ol == 0):
			number_removed,P_infty = robustness_stats_node(g_original, data)
		elif(ol == 1):
			number_removed,P_infty = robustness_flow_sum_F_stats_node(g_original, f_matrix, codes, data)
		elif(ol == 2):
			number_removed,P_infty = robustness_ncomp_stats_node(g_original, data)


		# Save data to disk
		file = open(relative_path + rob_measure_lbls[ol] + str(thresh) + '.csv', 'w')
		for i in range(len(number_removed)):
			file.write(str(number_removed[i]) + '\t' + str(P_infty[i]) + '\n')
		file.close()

		# complete the vector if there are missing cities (or states) with the worst case scenario
		# if only a few cities are missing, the differences are negligible
		P_infty_new = np.zeros(N+1)
		for i in range(N+1):
			if(i < len(P_infty)):
				P_infty_new[i] = P_infty[i]
			else:
				P_infty_new[i] = P_infty[-1]

		P_infty_new[-1] = 0.0

		R = sum(P_infty_new[1:]) / N
		V = 0.5 - R

		file_out = open(relative_path + rob_measure_lbls[ol] + 'R_V_' + str(thresh) + '.csv', 'w')
		file_out.write(str(thresh) + ';' + str(R)  + ';' + str(V) + '\n')
		file_out.close()
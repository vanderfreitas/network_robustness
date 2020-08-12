# -*- coding: utf-8 -*-

import igraph as ig
import numpy as np
import random



def total_flow(codes, labels, f_matrix):
	# compute the flow inside the component
	
	#first: find the indexes related to the labels
	ind = []
	for i in range(len(labels)):
		ind.append(np.where(codes == labels[i])[0][0])

	cl_flow = 0.0

	N = len(labels)

	for row in range(N):
		for col in range(N):
			cl_flow += f_matrix[ind[row], ind[col]]
	return cl_flow


def robustness_failure_node(g, simulations=50):
	N = g.vcount()

	number_removed = np.zeros(N+1)
	for i in range(g.vcount()):
		number_removed[i] = i / float(N)
	number_removed[N] = 1.0

	P_infty = np.zeros(N+1)

	# Find larger component
	cl = g.components()
	P_infty_baseline = float(max(cl.sizes()))

	for sim in range(simulations):
		g_copy = g.copy()
		P_infty[0] += 1.0

		count = 1
		while(g_copy.vcount() > 0):
			index = int(random.random() * g_copy.vcount())
			g_copy.delete_vertices(index)

			cl = g_copy.components()
			if(len(cl) > 0):
				P_infty[count] += float(max(cl.sizes())) / P_infty_baseline 
			else:
				P_infty[count] += 0.0

			count = count + 1

	# Compute the average
	P_infty = P_infty / float(simulations)

	return number_removed,P_infty


def robustness_failure_ncomp_node(g, simulations=50):
	N = g.vcount()

	number_removed = np.zeros(N+1)
	for i in range(g.vcount()):
		number_removed[i] = i / float(N)
	number_removed[N] = 1.0

	P_infty = np.zeros(N+1)

	# Find number of components
	cl = g.components()
	P_infty_baseline = float(len(cl.sizes()))

	for sim in range(simulations):
		g_copy = g.copy()
		P_infty[0] += 1.0

		count = 1
		while(g_copy.vcount() > 0):
			index = int(random.random() * g_copy.vcount())
			g_copy.delete_vertices(index)

			cl = g_copy.components()
			P_infty[count] += float(len(cl.sizes())) / P_infty_baseline 

			count = count + 1

	# Compute the average
	P_infty = P_infty / float(simulations)

	return number_removed,P_infty


def robustness_stats_node(g, stat_array):
	# Make a copy of the network
	g_copy = g.copy()

	N = g_copy.vcount()

	number_removed = np.zeros(N+1)
	for i in range(g.vcount()):
		number_removed[i] = i / float(N)
	number_removed[N] = 1.0


	P_infty = np.zeros(N+1)

	# Find larger component
	cl = g_copy.components()
	P_infty_baseline = float(max(cl.sizes()))

	P_infty[0] = 1.0

	count = 1
	while(g_copy.vcount() > 0 and count < len(stat_array)):
		index = g_copy.vs.find(label=stat_array[count-1][0]).index

		g_copy.delete_vertices(index)

		cl = g_copy.components()

		if(len(cl) > 0):
			P_infty[count] += float(max(cl.sizes())) / P_infty_baseline 
		else:
			P_infty[count] += 0.0

		count = count + 1

	if(count < g.vcount()):
		number_removed = number_removed[0:count]
		P_infty = P_infty[0:count]

	return number_removed,P_infty



def robustness_ncomp_stats_node(g, stat_array):
	# Make a copy of the network
	g_copy = g.copy()

	N = g_copy.vcount()

	number_removed = np.zeros(N+1)
	for i in range(g.vcount()):
		number_removed[i] = i / float(N)
	number_removed[N] = 1.0


	P_infty = np.zeros(N+1)


	P_infty[0] = 1.0
	cl = g_copy.components()
	P_infty_baseline = float(len(cl.sizes()))

	count = 1
	while(g_copy.vcount() > 0 and count < len(stat_array)):
		index = g_copy.vs.find(label=stat_array[count-1][0]).index

		g_copy.delete_vertices(index)

		cl = g_copy.components()
		P_infty[count] += float(len(cl.sizes())) / P_infty_baseline 

		count = count + 1

	if(count < g.vcount()):
		number_removed = number_removed[0:count]
		P_infty = P_infty[0:count]

	return number_removed,P_infty


def robustness_flow_sum_F_failure_node(g, f_matrix, codes, simulations=50):
	N = g.vcount()

	number_removed = np.zeros(N+1)
	for i in range(g.vcount()):
		number_removed[i] = i / float(N)
	number_removed[N] = 1.0

	P_infty = np.zeros(N+1)

	P_infty_baseline = float(np.sum(f_matrix))

	for sim in range(simulations):
		f_matrix_copy = f_matrix.copy()

		g_copy = g.copy()
		P_infty[0] += 1.0

		count = 1
		while(g_copy.vcount() > 0):
			index = int(random.random() * g_copy.vcount())
			
			# Remove the element from the flow matrix as well
			ind_in_the_original_matrix = np.where(codes == g_copy.vs[index]['label'])[0][0]
			f_matrix_copy[ind_in_the_original_matrix,:] = 0;
			f_matrix_copy[:,ind_in_the_original_matrix] = 0;

			g_copy.delete_vertices(index)

			P_infty[count] += float(np.sum(f_matrix_copy) ) / P_infty_baseline

			count = count + 1

	# Compute the average
	P_infty = P_infty / float(simulations)

	return number_removed,P_infty



def robustness_flow_sum_F_stats_node(g, f_matrix, codes, stat_array):
	# Make a copy of the network
	g_copy = g.copy()

	for i in range(len(stat_array)):
		index = g_copy.vs.find(label=stat_array[i][0]).index
		g_copy.vs[index]['size'] = stat_array[i][1] / 1000

	N = g_copy.vcount()

	number_removed = np.zeros(N+1)
	for i in range(g.vcount()):
		number_removed[i] = i / float(N)
	number_removed[N] = 1.0


	P_infty = np.zeros(N+1)

	P_infty_baseline = float(np.sum(f_matrix))

	f_matrix_copy = f_matrix.copy()

	P_infty[0] = 1.0

	count = 1
	while(g_copy.vcount() > 0 and count < len(stat_array)):
		index = g_copy.vs.find(label=stat_array[count-1][0]).index
		# Remove the element from the flow matrix as well
		ind_in_the_original_matrix = np.where(codes == g_copy.vs[index]['label'])[0][0]
		f_matrix_copy[ind_in_the_original_matrix,:] = 0;
		f_matrix_copy[:,ind_in_the_original_matrix] = 0;

		g_copy.delete_vertices(index)

		P_infty[count] = float(np.sum(f_matrix_copy)) / P_infty_baseline 

		count = count + 1

	if(count < g.vcount()):
		number_removed = number_removed[0:count]
		P_infty = P_infty[0:count]

	return number_removed,P_infty
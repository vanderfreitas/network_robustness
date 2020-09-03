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


relative_path_in = '../../results/' + in_files.get_project_name() + '/metrics/'
relative_path = '../../results/' + in_files.get_project_name() + '/robustness/'



print('EXPORT CITIES SORTED ACOORDING TO METRICS')



# Open the IBGE cities/states files ###############################
file_name_cities = '../../input_data/IBGE_geocode_cities.csv'

file_name_states = '../../input_data/IBGE_geocode_states.csv'


file_in = open(file_name_cities, 'r')
file_cities_lines = file_in.readlines()
file_in.close()

file_in = open(file_name_states, 'r')
file_states_lines = file_in.readlines()
file_in.close()

codes_ibge_cities = []
city_names = []

state_names = []
states_achron = []
codes_ibge_states = []

for i in range(len(file_cities_lines)):
	ln = file_cities_lines[i].strip()
	ln = ln.split(';')

	if(ln[0] not in codes_ibge_cities):
		codes_ibge_cities.append(int(ln[0]))
		city_names.append(ln[1])

codes_ibge_cities = np.array(codes_ibge_cities)


for i in range(len(file_states_lines)):
	ln = file_states_lines[i].strip()
	ln = ln.split(';')

	if(ln[0] not in codes_ibge_states):
		codes_ibge_states.append(int(ln[0]))
		state_names.append(ln[1])
		states_achron.append(ln[2])

codes_ibge_states = np.array(codes_ibge_states)
###########################################################




N = len(codes)

data = np.genfromtxt('../../results/' + in_files.get_project_name() + '/metrics/avg_std.csv', delimiter=';') 

avg = data[0]
std = data[1]



stats = ['strength', 'degree', 'betweenness', 'vuln']


# 3 thresholds
for thresh in [0, avg, avg+std]:

	for stat in stats:
		
		#print(relative_path_in + stat + '_' + str(thresh) + '.csv')
		st_data = np.genfromtxt(relative_path_in + stat + '_' + str(thresh) + '.csv', delimiter=';')

		# Compute the nodes' statistics and sort them
		stat_array = []
		for i in range(len(st_data)):
			stat_array.append( ( codes[i], float(st_data[i,1]) ) )

		dtype = [('label', int), ('stat', float)]
		stat_array = np.array(stat_array, dtype=dtype)
		stat_array = np.sort(stat_array, order='stat')
		stat_array = np.flip(stat_array)

		file_out = open(relative_path_in + 'ordered_' + stat + '_' + str(thresh) + '_city_names.csv', 'w')

		print(stat)

		for i in range(len(stat_array)):

			if(in_files.get_project_name() == 'STATE'):
				result = np.where(codes_ibge_states == int(stat_array[i][0]) )
			else:
				result = np.where(codes_ibge_cities == int(stat_array[i][0]) )

			if(len(result) > 0 and len(result[0]) > 0):
				ind = int(result[0][0])

				if(in_files.get_project_name() == 'STATE'):
					file_out.write(str(state_names[ind]) + '\n')
				elif(in_files.get_project_name() == 'SP' or in_files.get_project_name() == 'MG'):
					file_out.write(str(city_names[ind]) + '\n')
				else:
					# Find the corresponding state
					st_code_from_city_geocode = int( int(stat_array[i][0]) / 100000)
					st = np.where(codes_ibge_states == st_code_from_city_geocode)
					ind_st = int(st[0][0])
					file_out.write(str(city_names[ind] + ' (' + states_achron[ind_st] + ')' + '\n'))
				#file_out.write(str(codes_ibge[ind]) + ' ' + str(city_names[ind]) + '\n')
				#print(str(codes_ibge[ind]) + ' ' + str(city_names[ind]))
			#else:
			#	print(stat + '  ' + str(i) + '  ' + str(stat_array[i][0]) + '  ' + str(stat_array[i][1]))

		file_out.close()



if(in_files.get_project_name() == 'STATE'):
	file_name = '../../results/sort_nodes_covid-19/sorted_covid_cases_by_states.csv'
elif(in_files.get_project_name() == 'SP'):
	file_name = '../../results/sort_nodes_covid-19/sorted_covid_cases_by_cities_SP.csv'
elif(in_files.get_project_name() == 'MG'):
	file_name = '../../results/sort_nodes_covid-19/sorted_covid_cases_by_cities_MG.csv'
else:
	file_name = '../../results/sort_nodes_covid-19/sorted_covid_cases_by_cities.csv'

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

print(data)

file_out = open(relative_path_in + 'ordered_covid_cases.csv', 'w')

for i in range(len(data)):
	if(in_files.get_project_name() == 'STATE'):
		result = np.where(codes_ibge_states == int(data[i][0]) )
	else:
		result = np.where(codes_ibge_cities == int(data[i][0]) )

	if(len(result) > 0 and len(result[0]) > 0):
		ind = int(result[0][0])

		if(in_files.get_project_name() == 'STATE'):
			file_out.write(str(state_names[ind]) + '\n')
		elif(in_files.get_project_name() == 'SP' or in_files.get_project_name() == 'MG'):
			file_out.write(str(city_names[ind]) + '\n')
		else:
			# Find the corresponding state
			st_code_from_city_geocode = int( int(data[i][0]) / 100000)
			st = np.where(codes_ibge_states == st_code_from_city_geocode)
			ind_st = int(st[0][0])
			file_out.write(str(city_names[ind] + ' (' + states_achron[ind_st] + ')' + '\n'))
		#file_out.write(str(codes_ibge[ind]) + ' ' + str(city_names[ind]) + '\n')
		#print(str(codes_ibge[ind]) + ' ' + str(city_names[ind]))
	#else:
	#	print(str(i) + '  ' + str(data[i][0]) + '  ' + str(data[i][1]))

file_out.close()


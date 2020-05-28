import os
import numpy as np



########### LOADING INPUT FILES ##############
import sys
#sys.path.append('../')
from data_files import Input_files

in_files = Input_files('../') 
f_matrix_original = np.genfromtxt(in_files.get_network_file_name(),delimiter=';')
codes = np.genfromtxt(in_files.get_codes_file_name())
##############################################



# creating resulting folders
path_res = '../results/' + in_files.get_project_name() + '/'


try:
    os.makedirs('../results/sort_nodes_covid-19')
except OSError:
    pass
else:
    pass


folders = ['metrics', 'robustness']


for fd in folders:
	try:
	    os.makedirs(path_res + fd)
	except OSError:
	    pass
	else:
	    pass



# flow: average and std
N = len(codes)

# Considering only nonzero values
data = f_matrix_original[np.nonzero(f_matrix_original)] 

avg = np.mean(data)
std = np.std(data)

file_out = open('../results/' + in_files.get_project_name() + '/metrics/avg_std.csv', 'w')
file_out.write(str(avg) + ';' + str(std))
file_out.close()
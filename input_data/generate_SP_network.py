# -*- coding: utf-8 -*-

import numpy as np

import flow_matrix



# Load the flow matrix
f_matrix_original, codes = flow_matrix.generate_flow_matrix('roads.txt')  
N = len(f_matrix_original)	
#################################################


print('GENERATING SP NETWORK')

cities = []

#  35: SP
#  31: MG
code_state = 35 


for i in range(N):
	cod_s = int(int(codes[i]) / int(100000))

	if( (cod_s == code_state) and (codes[i] not in cities) ):
		cities.append(codes[i])

N_new = len(cities)
print('N=' + str(N_new))

f_state_net = np.zeros((N_new,N_new))


for row in range(N):
	cod_src = codes[row]
	ind_row = np.where(cod_src == cities)
	#print ind_row
	if(len(ind_row[0]) > 0):
		ind_row = ind_row[0][0]
		for col in range(N):
			#print(str(row) + ',' + str(col))
			cod_dst = codes[col]
			ind_col = np.where(cod_dst == cities)
			if(len(ind_col[0])>0):
				ind_col = ind_col[0][0]
				#print 'ind_row=', ind_row, '  ind_col=', ind_col

				if(ind_row != ind_col):
					f_state_net[ind_row,ind_col] = f_matrix_original[row,col]



file_out = open(str(code_state) + '_state_network.csv','w')

for row in range(N_new):
	file_out.write(str(f_state_net[row,0]))
	for col in range(1,N_new):
		file_out.write(';' + str(f_state_net[row,col]))
	file_out.write('\n')
file_out.close()


file_out = open(str(code_state) + '_state_network_codes.csv','w')
for i in range(N_new):
	file_out.write(str(cities[i]) + '\n')
file_out.close()
# -*- coding: utf-8 -*-

import numpy as np

import flow_matrix



# Load the flow matrix
f_matrix_original, codes = flow_matrix.generate_flow_matrix('roads.txt')  
N = len(f_matrix_original)		
#################################################



print('GENERATING THE STATES NETWORK (N=27)')


f_state_net = np.zeros((27,27))

# https://www.ibge.gov.br/geociencias/organizacao-do-territorio/estrutura-territorial/15774-malhas.html?=&t=sobre
codes_state_new = np.array([11,12,13,14,15,16,17,21,22,23,24,25,26,27,28,29,31,32,33,35,41,42,43,50,51,52,53])
#print(len(codes_state_new))


for row in range(N):
	cod_src = int(int(codes[row]) / int(100000))
	#print(cod_src)
	ind_row = np.where(cod_src == codes_state_new)
	#print ind_row
	if(len(ind_row[0]) > 0):
		ind_row = ind_row[0][0]
		for col in range(N):
			#print(str(row) + ',' + str(col))
			cod_dst = int(int(codes[col]) / int(100000))
			ind_col = np.where(cod_dst == codes_state_new)
			if(len(ind_col[0])>0):
				ind_col = ind_col[0][0]
				#print('ind_row=', ind_row, '  ind_col=', ind_col)

				if(ind_row != ind_col):
					f_state_net[ind_row,ind_col] += f_matrix_original[row,col]


file_out = open('states_network.csv','w')
N = len(codes_state_new)
for row in range(N):
	file_out.write(str(f_state_net[row,0]))
	for col in range(1,N):
		file_out.write(';' + str(f_state_net[row,col]))
	file_out.write('\n')
file_out.close()


file_out = open('states_network_codes.csv','w')
for i in range(N):
	file_out.write(str(codes_state_new[i]) + '\n')
file_out.close()
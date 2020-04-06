import igraph as ig
import numpy as np

from vuln_calculator import GraphMaking





def export_data(codes, data, name):
    file_out = open(name, 'w')
    for i in range(len(codes)):
        file_out.write(str(codes[i]) + ';' + str(data[i]) + '\n')
    file_out.close()




########### LOADING INPUT FILES ##############
import sys
sys.path.append('../')
from data_files import Input_files

in_files = Input_files('../../') 
f_matrix_original = np.genfromtxt(in_files.get_network_file_name(),delimiter=';')
codes = np.genfromtxt(in_files.get_codes_file_name())
##############################################

relative_path = '../../results/' + in_files.get_project_name() + '/metrics/'



print('METRICS: DEGREE AND VULNERABILITY')



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
    g = ig.Graph.Adjacency( (f_matrix > 0.0).tolist())
    N = g.vcount()

    # Convert to undirected graph
    g = g.as_undirected()

    g.vs['label'] = codes


    # degrees
    degrees = g.degree()
    export_data(codes, degrees, relative_path + 'degree_' + str(thresh) + '.csv')



    # Vulnerability indexes
    grp = GraphMaking(f_matrix)
    grp.create_graph(g)

    grp.vulnerability()
    export_data(codes, grp.vuln, relative_path + 'vuln_' + str(thresh) + '.csv')
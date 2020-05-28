import igraph as ig
import numpy as np

from vuln_calculator import GraphMaking





########### LOADING INPUT FILES ##############
import sys
sys.path.append('../')
from data_files import Input_files

in_files = Input_files('../../') 
f_matrix_original = np.genfromtxt(in_files.get_network_file_name(),delimiter=';')
codes = np.genfromtxt(in_files.get_codes_file_name())
##############################################


relative_path = '../../results/' + in_files.get_project_name() + '/metrics/'




def export_data(codes, data, stat, thresh):
    file_out = open(relative_path +  stat + '_' + str(thresh) + '.csv', 'w')
    for i in range(len(codes)):
        file_out.write(str(codes[i]) + ';' + str(data[i]) + '\n')
    file_out.close()

    # ordered version
    stat_array = []
    for i in range(len(data)):
        stat_array.append( ( codes[i], float(data[i]) ) )

    dtype = [('label', int), ('stat', float)]
    stat_array = np.array(stat_array, dtype=dtype)
    stat_array = np.sort(stat_array, order='stat')
    stat_array = np.flip(stat_array)
    
    file_stat = open(relative_path + 'ordered_' + stat + '_' + str(thresh) + '.csv', 'w')
    for i in range(len(stat_array)):
        file_stat.write(str(stat_array[i][0]) + ';' + str(stat_array[i][1]) + '\n')
    file_stat.close()
    




print('METRICS:')


N = len(codes)

data = np.genfromtxt('../../results/' + in_files.get_project_name() + '/metrics/avg_std.csv', delimiter=';') 

avg = data[0]
std = data[1]


# 3 thresholds
for thresh in [0, avg, avg+std]:
    print('  thresh=' + str(thresh))
    
    f_matrix = f_matrix_original.copy()


    # Apply threshold
    for row in range(N):
        for col in range(N):
            if f_matrix[row][col] < thresh:
                f_matrix[row][col] = 0


    print('   STRENGTH')
    node_str = np.zeros(N)
    for i in range(N):
        node_str[i] = np.sum( f_matrix[i,:] )

    export_data(codes, node_str, 'strength', thresh)


    
    # Create graph, A.astype(bool).tolist() or (A / A).tolist() can also be used.
    g = ig.Graph.Adjacency( (f_matrix > 0.0).tolist())
    N = g.vcount()

    # Convert to undirected graph
    g = g.as_undirected()

    g.vs['label'] = codes


    print('   DEGREE')
    degrees = g.degree()
    export_data(codes, degrees, 'degree', thresh)


    print('   BETWEENNESS')
    betweenness = g.betweenness(vertices=None, directed=False, cutoff=None)
    export_data(codes, betweenness, 'betweenness', thresh)    
    

    print('   VULNERABILITY')
    # Vulnerability indexes
    grp = GraphMaking(f_matrix)
    grp.create_graph(g)

    grp.vulnerability()
    export_data(codes, grp.vuln, 'vuln', thresh)
	

    '''
    # weighted metrics
    g = ig.Graph.Weighted_Adjacency(f_matrix.tolist(), mode=ig.ADJ_MAX)
    N = g.vcount()

    # Convert to undirected graph
    g = g.as_undirected()

    g.vs['label'] = codes

    betweenness = g.betweenness(vertices=None, directed=False, cutoff=None, weights='weight') 
    export_data(codes, betweenness, 'betweenness_weight', thresh)

    print('   WEIGHTED VULNERABILITY')
    grp = GraphMaking(f_matrix)
    grp.create_graph(g)
    grp.weighted_vulnerability()
    export_data(codes, grp.weighted_vuln, 'wVuln', thresh)

    print('   WEIGHTED ISOLATION')
    grp.weighted_isolation()
    export_data(codes, grp.infinities_weight, 'wIsolation', thresh)'''
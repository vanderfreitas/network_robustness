import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import string
import random
from matplotlib import rc


# Latex font --------------------
rc('text', usetex=True)
font = {'family' : 'normal',
         'weight' : 'bold',
         'size'   : 12}

rc('font', **font)
params = {'legend.fontsize': 14}
plt.rcParams.update(params)
# -------------------------------


########### LOADING INPUT FILES ##############
import sys
sys.path.append('../')
from data_files import Input_files

in_files = Input_files('../../') 
f_matrix_original = np.genfromtxt(in_files.get_network_file_name(),delimiter=';')
codes = np.genfromtxt(in_files.get_codes_file_name())
##############################################


N = len(codes)


relative_path_in = '../../results/' + in_files.get_project_name() + '/robustness/'
relative_path = '../../results/' + in_files.get_project_name() + '/'


data = np.genfromtxt('../../results/' + in_files.get_project_name() + '/metrics/avg_std.csv', delimiter=';') 

avg = data[0]
std = data[1]


print('PLOTTING ROBUSTNESS PICTURE')

stats = ['degree', 'vuln']


fig, ax = plt.subplots(2, 3)
fig.set_size_inches(10,2*(11/3.0))


for i in range(len(stats)+1):

	# One color for each stat
	cl = (random.random(), random.random(), random.random())


	# 3 thresholds
	ind = 0
	for thresh in [0, avg, avg+std]:

		if(i < len(stats)):
			file_name = relative_path_in + 'robustness_attack_' + str(stats[i]) + '_' + str(thresh) + '.csv'
			file_name_fs = relative_path_in + 'robustness_flow_strength_attack_' + str(stats[i]) + '_' + str(thresh) + '.csv'
			R_index = np.genfromtxt(relative_path_in + 'robustness_attack_' + str(stats[i]) + '_R_V_' + str(thresh) + '.csv', delimiter=';')
			R_index_fs = np.genfromtxt(relative_path_in + 'robustness_flow_strength_attack_' + str(stats[i]) + '_R_V_' + str(thresh) + '.csv', delimiter=';')
		else:
			file_name = relative_path_in + 'robustness_failure_' + str(thresh) + '.csv'
			file_name_fs = relative_path_in + 'robustness_flow_strength_failure_' + str(thresh) + '.csv' 
			R_index = np.genfromtxt(relative_path_in + 'robustness_failure_R_V_' + str(thresh) + '.csv', delimiter=';')
			R_index_fs = np.genfromtxt(relative_path_in + 'robustness_flow_strength_failure_R_V_' + str(thresh) + '.csv', delimiter=';')
			

		array_stats = np.genfromtxt(file_name, delimiter='\t')		
		array_stats_fs = np.genfromtxt(file_name_fs, delimiter='\t')



		if(i == 0):
			mk = 's'   
			cl='purple'
			lb=r'$\max(k)$' + r' (R=' + str("{:.3f}".format(R_index[1])) + r')'
			lb_flow=r'$\max(k)$' + r' (R=' + str("{:.3f}".format(R_index_fs[1])) + r')'
		elif(i==1):
			mk = '^'
			cl='orange'
			lb=r'$\max(V_k)$' + r' (R=' + str("{:.3f}".format(R_index[1])) + r')'
			lb_flow=r'$\max(V_k)$' + r' (R=' + str("{:.3f}".format(R_index_fs[1])) + r')'
		else:
			mk = 'o'
			cl='black'
			lb='failure' + r' (R=' + str("{:.3f}".format(abs(R_index[1]))) + r')'
			lb_flow='failure' + r' (R=' + str("{:.3f}".format(abs(R_index_fs[1]))) + r')'		


		# Sampling the data
		if(in_files.get_project_name() == 'BR'):
			step = 100
		elif(in_files.get_project_name() == 'SP'):
			step = 20
		else:
			step = 1

		ax[0][ind].plot(array_stats[::step,0], array_stats[::step,1], marker=mk, color=cl, label=lb)# marker=markers[i], color=colors[i])


		ax[1][ind].plot(array_stats_fs[::step,0], array_stats_fs[::step,1], marker=mk, color=cl, label=lb_flow)# marker=markers[i], color=colors[i], label=label_)

		ax[0][ind].legend(fontsize=10)
		ax[1][ind].legend(fontsize=10)
			
		ind += 1


# FORMAT
for i in range(3):
	ax[0][i].set_xlabel(r'$f$', fontsize=14)
	ax[0][i].set_ylabel(r'$P_\infty(f) / P_\infty(0)$', fontsize=14)

	ax[1][i].set_xlabel(r'$f$', fontsize=14)
	ax[1][i].set_ylabel(r'$P_\infty(f)^w / P_\infty(0)^w$', fontsize=14)

	ax[0][i].set_xlim([0,1])
	ax[0][i].set_ylim([0,1])

	ax[1][i].set_xlim([0,1])
	ax[1][i].set_ylim([0,1])

	ax[0][i].set_aspect(1.0)
	ax[1][i].set_aspect(1.0)

	ax[0][i].text(-0.1, 1.1, '('+string.ascii_lowercase[i]+')', transform=ax[0][i].transAxes, size=15, weight='bold')
	ax[1][i].text(-0.1, 1.1, '('+string.ascii_lowercase[i+3]+')', transform=ax[1][i].transAxes, size=15, weight='bold')



ax[1][2].legend(fontsize=10)


plt.tight_layout()

fig.savefig(relative_path + 'f_vs_Pinfty.pdf', dpi=100)
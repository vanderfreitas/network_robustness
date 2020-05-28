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
#f_matrix_original = np.genfromtxt(in_files.get_network_file_name(),delimiter=';')
codes = np.genfromtxt(in_files.get_codes_file_name())
##############################################


N = len(codes)


relative_path_in = '../../results/' + in_files.get_project_name() + '/robustness/'
relative_path = '../../results/' + in_files.get_project_name() + '/'


data = np.genfromtxt('../../results/' + in_files.get_project_name() + '/metrics/avg_std.csv', delimiter=';') 

avg = data[0]
std = data[1]


print('PLOTTING ROBUSTNESS PICTURE')


stats = ['strength', 'degree', 'vuln', 'betweenness'] #, 'isolation', 'wVuln', 'wIsolation']



fig, ax = plt.subplots(2, 3)
fig.set_size_inches(10,2*(11/3.0))



# Sampling the data
if(in_files.get_project_name() == 'BR'):
	step = 100
elif(in_files.get_project_name() == 'SP'):
	step = 20
elif(in_files.get_project_name() == 'MG'):
	step = 20
else:
	step = 1


colors = ['purple', 'orange', 'seagreen', 'steelblue', 'black', 'indianred']
markers = ['s', 'o', '^', 'P', '*', 'x']
lbls = [r'$\max(s)$', r'$\max(k)$', r'$\max(Vul)$', r'$\max(b)$', 'failure', 'RS']


# Figure out what is the highest f, from the COVID-19 cases
file_name = relative_path_in + 'robustness_attack_sorted_covid_0.csv'
array_stats = np.genfromtxt(file_name, delimiter='\t')
f_max = array_stats[-1,0]
f_max_ind = len(array_stats)-1





for i in range(len(stats)+2):


	# 3 thresholds
	ind = 0
	for thresh in [0, avg, avg+std]:

		if(i < len(stats)):
			file_name = relative_path_in + 'robustness_attack_' + str(stats[i]) + '_' + str(thresh) + '.csv'
			file_name_fs = relative_path_in + 'robustness_flow_attack_' + str(stats[i]) + '_' + str(thresh) + '.csv'
			file_name_fs_F = relative_path_in + 'robustness_flow_attack_sum_F_' + str(stats[i]) + '_' + str(thresh) + '.csv'
			
			R_index = np.genfromtxt(relative_path_in + 'robustness_attack_' + str(stats[i]) + '_R_V_' + str(thresh) + '.csv', delimiter=';')
			R_index_fs = np.genfromtxt(relative_path_in + 'robustness_flow_attack_' + str(stats[i]) + '_R_V_' + str(thresh) + '.csv', delimiter=';')
			R_index_fs_F = np.genfromtxt(relative_path_in + 'robustness_flow_attack_sum_F_' + str(stats[i]) + '_R_V_' + str(thresh) + '.csv', delimiter=';')
		elif(i==len(stats)):
			file_name = relative_path_in + 'robustness_failure_' + str(thresh) + '.csv'
			#file_name_fs = relative_path_in + 'robustness_flow_failure_' + str(thresh) + '.csv' 
			file_name_fs_F = relative_path_in + 'robustness_flow_sum_F_failure_' + str(thresh) + '.csv' 
			
			R_index = np.genfromtxt(relative_path_in + 'robustness_failure_R_V_' + str(thresh) + '.csv', delimiter=';')
			#R_index_fs = np.genfromtxt(relative_path_in + 'robustness_flow_failure_R_V_' + str(thresh) + '.csv', delimiter=';')
			R_index_fs_F = np.genfromtxt(relative_path_in + 'robustness_flow_sum_F_failure_R_V_' + str(thresh) + '.csv', delimiter=';')
		else:

			# Set the limits for the cases
			file_name = relative_path_in + 'robustness_attack_sorted_covid_' + str(thresh) + '.csv'
			file_name_fs = relative_path_in + 'robustness_attack_sorted_covid_flow_' + str(thresh) + '.csv'
			file_name_fs_F = relative_path_in + 'robustness_attack_sorted_covid_flow_sum_F_' + str(thresh) + '.csv'

			R_index = np.genfromtxt(relative_path_in + 'robustness_attack_sorted_covid_R_V_' + str(thresh) + '.csv', delimiter=';')
			R_index_fs = np.genfromtxt(relative_path_in + 'robustness_attack_sorted_covid_flow_R_V_' + str(thresh) + '.csv', delimiter=';')
			R_index_fs_F = np.genfromtxt(relative_path_in + 'robustness_attack_sorted_covid_flow_sum_F_R_V_' + str(thresh) + '.csv', delimiter=';')


			array_stats = np.genfromtxt(file_name, delimiter='\t')	
			ax[0][ind].fill_between(array_stats[::step,0], array_stats[::step,1], color='indianred', alpha=0.3)

			print(f_max, f_max_ind, 'res (Y comp): ', array_stats[-1,1])
			#array_stats = np.genfromtxt(file_name_fs, delimiter='\t')	
			#ax[1][ind].fill_between(array_stats[::step,0], array_stats[::step,1], color='indianred', alpha=0.3)

			array_stats = np.genfromtxt(file_name_fs_F, delimiter='\t')	
			ax[1][ind].fill_between(array_stats[::step,0], array_stats[::step,1], color='indianred', alpha=0.3)
			

		array_stats = np.genfromtxt(file_name, delimiter='\t')		
		#array_stats_fs = np.genfromtxt(file_name_fs, delimiter='\t')
		array_stats_fs_F = np.genfromtxt(file_name_fs_F, delimiter='\t')

		# Compute R
		#size = len(array_stats[1:f_max_ind+1,1])
		#print(array_stats[f_max_ind,0], f_max, array_stats[0,1])
		#print('ind, size', f_max_ind, size+1)
		#R_index = np.sum(array_stats[1:f_max_ind+1,1]) / float(size)



		mk = markers[i]
		cl = colors[i]

		if(i<len(stats)+2):
			lb = lbls[i] + r' (R=' + str("{:.3f}".format(R_index[1])) + r')'
			#lb_flow = lbls[i] + r' (R=' + str("{:.3f}".format(R_index_fs[1])) + r')'
			lb_flow_F = lbls[i] + r' (R=' + str("{:.3f}".format(R_index_fs_F[1])) + r')'
		else:
			lb = lbls[i]
			#lb_flow = lbls[i]
			lb_flow_F = lbls[i]

		
		ax[0][ind].plot(array_stats[::step,0], array_stats[::step,1], marker=mk, color=cl, label=lb)# marker=markers[i], color=colors[i])
		#ax[1][ind].plot(array_stats_fs[::step,0], array_stats_fs[::step,1], marker=mk, color=cl, label=lb_flow)# marker=markers[i], color=colors[i])
		ax[1][ind].plot(array_stats_fs_F[::step,0], array_stats_fs_F[::step,1], marker=mk, color=cl, label=lb_flow_F)# marker=markers[i], color=colors[i])


		#ax[ind].plot(array_stats_fs[::step,0], array_stats_fs[::step,1], marker=mk, color=cl, label=lb_flow)# marker=markers[i], color=colors[i], label=label_)

		ax[0][ind].legend(fontsize=8)
		#ax[1][ind].legend(fontsize=8)
		ax[1][ind].legend(fontsize=8)
			
		ind += 1


# FORMAT
for i in range(3):
	ax[0][i].set_xlabel(r'$f$', fontsize=14)
	ax[0][i].set_ylabel(r'$P_\infty(f) / P_\infty(0)$', fontsize=14)

	ax[0][i].set_xlim([0,1])
	ax[0][i].set_ylim([0,1])


	ax[0][i].set_aspect(1.0)

	ax[0][i].text(-0.1, 1.1, '('+string.ascii_lowercase[i]+')', transform=ax[0][i].transAxes, size=15, weight='bold')


	'''
	ax[1][i].set_xlabel(r'$f$', fontsize=14)
	ax[1][i].set_ylabel(r'$P_\infty(f)^{(w)} / P_\infty(0)^{(w)}$', fontsize=14)

	ax[1][i].set_xlim([0,1])
	ax[1][i].set_ylim([0,1])


	ax[1][i].set_aspect(1.0)

	ax[1][i].text(-0.1, 1.1, '('+string.ascii_lowercase[i+3]+')', transform=ax[1][i].transAxes, size=15, weight='bold')
	'''

	ax[1][i].set_xlabel(r'$f$', fontsize=14)
	ax[1][i].set_ylabel(r'$\left \| W \right \|(f) / \left \| W \right \|(0)$', fontsize=14)

	ax[1][i].set_xlim([0,1])
	ax[1][i].set_ylim([0,1])


	ax[1][i].set_aspect(1.0)

	ax[1][i].text(-0.1, 1.1, '('+string.ascii_lowercase[i+3]+')', transform=ax[1][i].transAxes, size=15, weight='bold')
	

#ax[2].legend(fontsize=10)


plt.tight_layout()

fig.savefig(relative_path + 'f_vs_Pinfty.pdf', dpi=100)
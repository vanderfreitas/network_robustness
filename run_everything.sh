cd input_data
python generate_BR_network.py
python generate_SP_network.py
python generate_states_network.py

cd ../src/metrics
python net_stats.py

cd ../sort_nodes
python sort_nodes_according_to_covid.py

cd ../robustness
python network_robustness_failure.py
python network_robustness_flow_failure_sum_F.py
python network_robustness_flow_stats_sum_F.py
python network_robustness_sorted_covid_cases_flow_sum_F.py
python network_robustness_stats.py

cd ../attack_failures
python plot_R_parcial.py
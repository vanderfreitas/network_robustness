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
python network_robustness_stats.py
python network_robustness_sorted_covid.py

cd ../plot
python plot_R.py
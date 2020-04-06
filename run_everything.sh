cd src
python setup.py


cd metrics
python net_stats.py


cd ../robustness
python network_robustness_failure.py
python network_robustness_stats.py
python network_robustness_flow_strength_failure.py
python network_robustness_flow_strength_stats.py

cd ../attack_failures
python plot.py
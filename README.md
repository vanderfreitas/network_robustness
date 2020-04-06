# Robustness analysis in an inter-cities mobility network: modeling municipal, state and federal initiatives as failures and attacks

**Abstract**: Motivated by the challenge related to the COVID-19 epidemic and the seek for optimal containment strategies, we present a robustness analysis into an inter-cities mobility complex network. We abstract municipal initiatives as nodes' failures and the federal actions as targeted attacks. The geo(graphs) approach is applied to visualize the geographical graph and produce maps of topological indexes, such as degree and vulnerability. A Brazilian data of 2016 is considered a case study, with more than five thousand cities and twenty-seven states. Based on the Network Robustness index, we show that the most efficient attack strategy shifts from a topological degree-based, for the all cities network, to a topological vulnerability-based, for a network considering the Brazilian States as nodes. Moreover, our results reveal that individual municipalities' actions do not cause a high impact on mobility restrain since they tend to be punctual and disconnected to the country scene as a whole. Oppositely, the coordinated isolation of specific cities is key to detach entire network areas and thus prevent a spreading process to prevail.


**Collaborators**: Vander L. S. Freitas, Jeferson Feitosa, Catia S. N. Sepetauskas and Leonardo B. L. Santos.


Dependencies (tested on Python 3.6.10 :: Anaconda, Inc.):
* matplotlib
* igraph
* numpy



To generate the three networks from the raw data:
```
bash generate_networks.sh
```

To run all the simulations for each network:
- Set the network in the file: *simulations_input.txt*
```
bash run_everything.sh
```


If you use this code, please cite the paper:

**FREITAS, V. L. S.; FEITOSA, J.; SEPETAUSKAS, C. S. N.; SANTOS, L. B. L. (2020). Robustness analysis in an inter-cities mobility network: modeling municipal, state and federal initiatives as failures and attacks.** 

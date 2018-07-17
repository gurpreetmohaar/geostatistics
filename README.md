# Modelling uncertainity in geostatistics
This jupyter notebook is meant to model uncertainity realted to domain classification in earth sciences. 
settings can be changed in config.yml file

Parameters: 

1) filepath: "ZaldivarBH.txt"    # This is the data source with coordinates and statistical variable CUT, ASCU in this case
2) Window_size: size of window in data points
3) overlap: this determines the jump or the slide overlap
4) slide_along: data will be sorted in this direction and uncertainity will only be modelled in this direction
5) num_clusters: this determines number of states in markov chain

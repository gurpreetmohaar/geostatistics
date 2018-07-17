# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 17:31:03 2018
This script is used to perform a unidirectional window slide on 3D geological data and extract statistical features from each block.
Parameters: Window size, Overlap
@author: GMohaar

Steps: 
1) Sort along a single direction where you would like to slide the window
2) Read window size and overlap settings from config file
3) Slide window and from each block , calculate statistical features
4) return feature vector with block number as Id.    
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 09:16:08 2018

@author: GMohaar
"""
import sys
sys.modules[__name__].__dict__.clear()
import pandas as pd
import yaml
import os
from scipy.stats import kurtosis
from scipy.stats import skew

#Clear all variables and memory and change working directory
#change it to your personal directory here

os.chdir('C:\Mohaar\Personal\Queens\Thesis\Python\Zaldivar\Zaldivar')

#read data and windowing settings from YML
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
file_name = cfg['filepath']
window_size = cfg['window_size']
overlap = cfg['overlap']
num_clusters = cfg['num_clusters'] 
data  = pd.read_csv(file_name,delim_whitespace=True)
sort_along = cfg['slide_along'] #bydefault set to east. go to config file if want to slide along other directions.
data = data.drop(['ID','BLAST', 'BHS','FAULT'], axis = 1)
data = data.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
#Class window_slide, This class defines properties of windowing
class Window_slide:
    def __init__(self, dataframe, window_size, overlap):
        self._validate(dataframe, window_size, overlap)
        self.df = dataframe
        self._window_size = window_size
        self._overlap = overlap
        self._window_start_index = 0
        self._window_data = None

    def slide(self):
        self._window_data = self.df.iloc[self._window_start_index:self._window_start_index + self._window_size,:]
        if len(self._window_data) == self._window_size:
            self._window_start_index = self._next_window_start_index()
        return self._window_data

    def _validate(self, dataframe, window_size, overlap):
        list_length = len(dataframe)
        if list_length == 0:
            raise ValueError('List cannot be empty')
        if list_length < window_size:
            raise ValueError('Bucket size should be smaller than list size')
        if overlap >= window_size:
            raise ValueError('Overlap count should be lesser than bucket_size')

    def current_position(self):
        if self._window_start_index == 0:
            raise RuntimeError('Slide window first')
        start = (self._window_start_index - self._window_size) + self._overlap
        end = (start + self._window_size) - 1
        if len(self._window_data) < self._window_size:
            start = self._window_start_index
            end = self._list_length() - 1
        return start, end

    def reached_end_of_list(self):
        return len(self._window_data) < self._window_size

    def _list_length(self):
        return len(self.df)

    def _next_window_start_index(self):
        return (self._window_start_index) + self._overlap

# extract-features function calculates kurtosis, mean, skewness, st ddev of different attributtes and append them 
def extract_features(window_matrix):    
     rtypes =  window_matrix.RT.nunique()
     ctypes = window_matrix.CODE.nunique()
     kurtosis_cut =  kurtosis(window_matrix.CUT)
     kurtosis_ascu = kurtosis(window_matrix.ASCU)
     skewness_cut = skew(window_matrix.CUT)
     skewness_ascu = skew(window_matrix.ASCU)
     mean_north = window_matrix.NORTH.mean()
     mean_east = window_matrix.EAST.mean()
     mean_elev = window_matrix.ELEV.mean()
     mean_cut = window_matrix.CUT.mean()
     mean_ascu = window_matrix.ASCU.mean()
     std_ascu = window_matrix.ASCU.std()
     std_cut = window_matrix.CUT.std()
     std_north = window_matrix.NORTH.std()
     std_east = window_matrix.EAST.std()
     std_elev = window_matrix.ELEV.std()
     df = pd.DataFrame({'rock_types': [rtypes], 'code_types': [ctypes],'kurtosis_CUT':[kurtosis_cut], 'kurtosis_ASCU': [kurtosis_ascu], 'skewness_CUT': [skewness_cut], 'skewness_ASCU':[skewness_ascu],'mean_north': [mean_north] ,'mean_east': [mean_east],'mean_elev': [mean_elev],'mean_cut': [mean_cut],'mean_ascu': [mean_ascu],'std_north': [std_north],'std_east': [std_east],'std_elev': [std_elev],'std_cut': [std_cut],'std_ascu': [std_ascu] })      
     return(df)


'''Execution logic goes below'''
#Data should be sorted in one direction either x,y,z
sorted_data = data.sort_values(sort_along)
#initialise class : window
window = Window_slide(sorted_data,window_size,overlap)
features_single_block = pd.DataFrame();
while True:
    window_matrix = window.slide()
    if len(window_matrix ==window_size):
        #print("TO BE DEVELOPED ...extracting features for block i .... Printing data in block" ,window_matrix )
        features_single_block = features_single_block.append(extract_features(window_matrix), ignore_index=True)
        if window.reached_end_of_list(): break
#Only keep complete cases
feature_set = pd.DataFrame(features_single_block.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False))

###k means clustering
from sklearn.cluster import KMeans
#change number of clusters in config file, current setting is 10  
kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(feature_set)
state = pd.DataFrame(kmeans.labels_)
cluster_result = pd.concat([feature_set, state], axis=1)

kmeans.cluster_centers_
state_vec = pd.DataFrame(state)
state_vec.plot()
#####plot states
import seaborn as sns
# use the function regplot to make a scatterplot
sns.regplot(x=cluster_result['mean_cut'], y=cluster_result.iloc[:,-1])
#sns.plt.show()

############################################################
#Below code provides the state transtition matrix

import pandas as pd
#transitions = ['A', 'B', 'B', 'C', 'B', 'A', 'D', 'D', 'A', 'B', 'A', 'D'] * 2
df = pd.DataFrame(columns = ['state', 'next_state'])
for i, val in enumerate(state[:-1]): # We don't care about last state
    df_stg = pd.DataFrame(index=[0])
    df_stg['state'], df_stg['next_state'] = state[i], state[i+1]
    df = pd.concat([df, df_stg], axis = 0)
cross_tab = pd.crosstab(df['state'], df['next_state'])
cross_tab.div(cross_tab.sum(axis=1), axis=0)
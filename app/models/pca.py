import numpy as np
import pandas as pd

from sklearn.decomposition import PCA



class ComponentsReduction:

    def __init__(self, df):
        # NOTE: make sure to use copy() to avoid changing the original dataframe
        self.df = df
        self.original_df = df.copy()
    
    def set_data_frame(self, df):
        self.df = df
        self.original_df = df.copy()
    
    def select_columns(self, columns):
        self.df = self.df[columns]
    
    def normalize_column_data(self, column_name, method):
        self.df[column_name] = self.df[column_name].apply(method)
    
    def scale_to_range_zero_one(self, column_name, min, max):
        self.df[column_name] = self.df[column_name].apply(lambda val: (val - min) / (max - min))
    
    def invert_percentage(self, column_name):
        self.df[column_name] = self.df[column_name].apply(lambda x: (100-x)/100)

    def apply_pca(self, threshold, starting_from=0):
        pca = PCA(threshold)
        pca.fit(self.df.iloc[starting_from:])
        pca_data = pca.transform(self.df)
        pca_df = pd.DataFrame(pca_data)
        return pca_df

    
    

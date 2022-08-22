import numpy

import pandas
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import os







class FullRecommender:
    # model based on cosine similarity calculation


    def __init__(self, df):
        self.df = df
        self.original_df = df.copy()


    def get_data_frame(self, df, **kwargs): # private method for internal use
        if 'drop' in kwargs:
            for a in kwargs['drop']:
                df = df.drop(a, axis=1)
        if 'parameters' in kwargs:
            df = df[kwargs['parameters']]

        return df

    def set_features(self, features, id_col, drop=False):
        if drop:
            self.df = self.get_data_frame(self.df,drop=features)
        else:
            self.df = self.get_data_frame(self.df,parameters=features)

    def clean_data(self, cleaning_method):
        self.df = cleaning_method(self.df)

    def run(self, id):
        pass # TODO: implement this method


    def combine_dimensions(self, features):
        '''
        type: private
        use PCA to reduce the features to less dimensions
        
        :param features: list of features to be reduced
        '''
        pass

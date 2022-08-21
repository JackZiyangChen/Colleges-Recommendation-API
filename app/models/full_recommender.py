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


    def get_data_frame(self, df, id_column, **kwargs): # private method for internal use
        if 'drop' in kwargs:
            for a in kwargs['drop']:
                df = df.drop(a, axis=1)
        if 'parameters' in kwargs:
            df = df[[id_column] + kwargs['parameters']]

        return df.set_index(id_column)

    def set_features(self, features, id_col, drop=False):
        if drop:
            self.df = self.get_data_frame(self.df,id_col,drop=features)
        else:
            self.df = self.get_data_frame(self.df,'id_col',parameters=features)

    def clean_data(self, cleaning_method):
        pass #TODO implement method with PCA technique

    def run(self, id):
        pass # TODO: implement this method


    def combine_dimensions(self, features):
        '''
        type: private
        use PCA to reduce the features to less dimensions
        
        :param features: list of features to be reduced
        '''
        pass

    def vectorize_data(self, features):
        '''
        type: private
        use CountVectorizer to vectorize the string data from features

        :param features: list of features to be vectorized
        :return: dataframe column with vectorized data
        '''

        pass #TODO implement method with Count Vectorizer
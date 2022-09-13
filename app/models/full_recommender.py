import numpy

import pandas
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import os
from .preparation import *


class FullRecommender:
    # model based on cosine similarity calculation


    def __init__(self, df):
        self.df = df
        self.original_df = df.copy()
        self.cosine_matrix = None


    def get_data_frame(self, df, **kwargs): # private method for internal use
        if 'drop' in kwargs:
            for a in kwargs['drop']:
                df = df.drop(a, axis=1)
        if 'parameters' in kwargs:
            df = df[kwargs['parameters']]

        return df

    def set_features(self, features, drop=False):
        if drop:
            self.df = self.get_data_frame(self.df,drop=features)
        else:
            self.df = self.get_data_frame(self.df,parameters=features)

    def clean_data(self, cleaning_method):
        self.df = cleaning_method(self.df)



    def run(self):
        matrix = self.df.to_numpy()
        self.cosine_matrix = cosine_similarity(matrix)


    def get_similar_items(self, val, by=None, top=10):
        '''
        type: public
        get similar items to the df[by==val]
        if by is None then use row index as the key

        :param val: value to be compared
        :param by: column to be compared
        :param top: number of top similar items to be returned

        :return: dataframe of similar items
        '''


        if by:
            if by in self.original_dfdf.columns:
                id = self.original_df[self.original_df[by] == val].index[0]
            else:
                raise Exception("Column {} not found".format(by))
        else:
            id = val

        similarity_list = list(enumerate(self.cosine_matrix[id]))
        similarity_list.sort(key=lambda x: x[1], reverse=True)
        return self.original_df.iloc[[v for i,v in similarity_list[1:top+1]]]




    def combine_dimensions(self, features):
        '''
        type: private
        use PCA to reduce the features to less dimensions
        
        :param features: list of features to be reduced
        '''
        pass

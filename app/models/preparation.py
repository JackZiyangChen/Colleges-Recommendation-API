import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA




def us_news_data_cleaner(df):
    df['region'].replace(np.nan, 'national', inplace=True)
    df['rank'].replace(-2, 999, inplace=True)
    df['rank'].replace(-1, 999, inplace=True)
    df['computerScienceRepScore'].replace([np.nan,'< 2.0'], 0, inplace=True)
    df['engineeringRepScore'].replace([np.nan,'< 2.0'], 0, inplace=True)
    df['businessRepScore'].replace([np.nan,'< 2.0'], 0, inplace=True)
    df['nursingRepScore'].replace([np.nan,'< 2.0'], 0, inplace=True)


    df['computerScienceRepScore'] = pd.to_numeric(df['computerScienceRepScore'])
    df['engineeringRepScore'] = pd.to_numeric(df['engineeringRepScore'])
    df['businessRepScore'] = pd.to_numeric(df['businessRepScore'])
    df['nursingRepScore'] = pd.to_numeric(df['nursingRepScore'])

    df['computerScienceRepScore'] = df['computerScienceRepScore'] - 4.0
    df['engineeringRepScore'] = df['engineeringRepScore'] - 4.0
    df['businessRepScore'] = df['businessRepScore'] - 4.0
    df['nursingRepScore'] = df['nursingRepScore'] - 4.0


    return df

def normalize_test_score(df):
    DataPointTransformation.scale_to_range_zero_one(df, 'sat25', 400, 1600)
    DataPointTransformation.scale_to_range_zero_one(df, 'sat75', 400, 1600)
    DataPointTransformation.scale_to_range_zero_one(df, 'act25', 18, 36)
    DataPointTransformation.scale_to_range_zero_one(df, 'act75', 18, 36)

def college_data_cleaner_basic(df):

    transform_feature(df, 'overall admission rate', DataPointTransformation.invert_percentage())
    transform_feature(df, 'overall admission rate.men', DataPointTransformation.invert_percentage())
    transform_feature(df, 'overall admission rate.women', DataPointTransformation.invert_percentage())
    transform_feature(df, 'average gpa', DataPointTransformation.scale_to_range_zero_one(0.0, 4.0))

    transform_feature(df, 'received financial aid', DataPointTransformation.invert_percentage())
    transform_feature(df, 'need fully met', DataPointTransformation.invert_percentage())
    transform_feature(df, 'average percent of need met', DataPointTransformation.invert_percentage())
    transform_feature(df, 'city size', DataPointTransformation.scale_to_range_zero_one(1000, 1000000)) # TODO: turn into log scaling
    transform_feature(df, 'campus size', DataPointTransformation.scale_to_range_zero_one(df['campus size'].min(), df['campus size'].max()))


    transform_feature(df, 'sororities', DataPointTransformation.invert_percentage())
    transform_feature(df, 'fraternities', DataPointTransformation.invert_percentage())


    



def vectorize_data(df, features, column_name="combined_features"):
        '''
        use CountVectorizer to vectorize the string data from features

        :param features: list of features to be vectorized
        :return: dataframe column with vectorized data
        '''

        data_list = [] # each element is a list of features for each row
        for i in range(0, df.shape[0]):
            tokens = ""
            for feature in features:
                tokens += str(df[feature][i]) + " "
            data_list.append(tokens)

        vectorizer = CountVectorizer()
        matrix = vectorizer.fit_transform(data_list)
        df_out = pd.DataFrame(matrix.toarray(), columns=[f'{column_name}_{i}' for i in range(0, matrix.shape[1])])
        return df_out

def transform_feature(df, feature_name, method):
    if feature_name in df.columns:
        df[feature_name] = df[feature_name].apply(method)
    else:
        raise Exception("Column {} not found".format(feature_name))


class DataPointTransformation:
    def scale_to_range_zero_one(self, min, max):
        return lambda val: (val - min) / (max - min)

    def invert_percentage(self):
        return lambda x: (100 - x) / 100



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
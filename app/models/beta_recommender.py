import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import os





# def us_news_data_cleaner(df):
#     df['region'].replace(np.nan, 'national', inplace=True)
#     df['rank'].replace(-2, 999, inplace=True)
#     df['rank'].replace(-1, 999, inplace=True)
#     df['computerScienceRepScore'].replace([np.nan,'< 2.0'], 0, inplace=True)
#     df['engineeringRepScore'].replace([np.nan,'< 2.0'], 0, inplace=True)
#     df['businessRepScore'].replace([np.nan,'< 2.0'], 0, inplace=True)
#     df['nursingRepScore'].replace([np.nan,'< 2.0'], 0, inplace=True)


#     df['computerScienceRepScore'] = pd.to_numeric(df['computerScienceRepScore'])
#     df['engineeringRepScore'] = pd.to_numeric(df['engineeringRepScore'])
#     df['businessRepScore'] = pd.to_numeric(df['businessRepScore'])
#     df['nursingRepScore'] = pd.to_numeric(df['nursingRepScore'])

#     df['computerScienceRepScore'] = df['computerScienceRepScore'] - 4.0
#     df['engineeringRepScore'] = df['engineeringRepScore'] - 4.0
#     df['businessRepScore'] = df['businessRepScore'] - 4.0
#     df['nursingRepScore'] = df['nursingRepScore'] - 4.0

#     return df

# note: all column in us news 2022 are written in camelCase
# if __name__ == '__main__':
#     original_df = pandas.read_csv(os.path.join('../../data', 'us_news_2022.csv'))
#
#     df = get_data_frame(os.path.join('../../data', 'us_news_2022.csv'), id_column='id', drop=['name', 'rankingType', 'urlName', 'fundingType', 'location', 'percentReceivingAid', 'hsGpa'])
#     df = us_news_data_cleaner(df)
#
#
#
#     # df.query('rank < 100', inplace=True)
#     items = get_similar_items(['3691'], df)
#     for i in items:
#         print(original_df['name'][i])
    



class BetaRecommender:
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
        self.df = cleaning_method(self.df)

    def run(self, id):
        id_list = [id]
        features_list = []
        for i in range(0, self.df.shape[0]):
            features = ""
            for elem in np.array(self.df)[i]:
                features += str(elem) + " "
            features_list.append(features)

        vectorizer = CountVectorizer()
        matrix = vectorizer.fit_transform(features_list)

        cosine_similarities = cosine_similarity(matrix)

        self.df.reset_index(inplace=True)  # find a more optimal solution for this
        all_recs = []
        for item_id in id_list:
            id = self.df[self.df['id'] == item_id].index[0]
            similarity_scores = list(enumerate(cosine_similarities[int(id)]))
            sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
            all_recs += [sorted_scores[i][0] for i in range(1, 21)]

        frequency_count = {}
        for item in all_recs:
            if item in frequency_count:
                frequency_count[item] += 1
            else:
                frequency_count[item] = 0

        out = [i[0] for i in sorted(frequency_count.items(), key=lambda x: x[1])]

        rec_indices = out[:10]
        print(rec_indices)
        df_out = self.original_df.copy()
        df_out = df_out.iloc[rec_indices]

        return df_out





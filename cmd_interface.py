from app.models.beta_recommender import us_news_recommender
import pandas as pd
import os

def get_id_from_school_name(input_name):
    df = pd.read_csv(os.path.join('data','id_table.csv'))
    id = df[df['name'] == input_name]['id']
    if len(id.values) > 0:
        return id.values[0]
    else:
        id = df[df['alias'].str.contains(input_name)==True]['id']
        return id.values[0] if len(id.values) > 0 else None


if __name__ == '__main__':
    df = pd.read_csv(os.path.join('data','id_table.csv'))
    name = str(input('Enter a school name:'))
    id = get_id_from_school_name(name)
    if id is None:
        print('School not found')
    else:
        items = us_news_recommender(id)
        for i in items:
            print(df['name'][i])
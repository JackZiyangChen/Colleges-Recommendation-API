import pandas as pd
import numpy as np
import os


class DataLoader:
    def load_from_csv(self, name):
        csv = pd.read_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)), name))
        return csv

    def get_rows_from_csv(self, csv_name, parameters):
        df = self.load_from_csv(csv_name)
        query = ''
        i=0
        for k,v in parameters.items():
            query += f'{k}==\'{v}\''
            if i < len(parameters.items())-1:
                query += ' and '
            i+=1
        df.query(query, inplace=True)
        return df.reset_index()

    def get_col_names_from_csv(self, csv_name):
        return [self.load_from_csv(csv_name).columns]

    def serialize_row(self, row, column_names):
        data = {}
        for col in column_names:
            data[col] = row[col]

        return data

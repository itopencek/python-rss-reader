import pandas as pd


class Database:
    PATH = "./database"

    def __init__(self, path_ext):
        self.PATH += path_ext
        self.df = pd.read_csv(self.PATH, index_col=0)

    def __del__(self):
        self.df.to_csv(self.PATH)

    def get_by_column(self, column, name):
        return self.df.loc[self.df[column] == name].to_dict(orient="list")

    def insert(self, row):
        self.df = self.df.append(row, ignore_index=True)

    def write_to_file(self):
        self.df.to_csv(self.PATH)

    def exists(self, column, key):
        return not self.df.loc[self.df[column] == key].empty

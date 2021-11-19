import pandas as pd


class Database:
    PATH = "./database"

    def __init__(self, path_ext):
        self.PATH += path_ext
        self.df = pd.read_csv(self.PATH, index_col=0)

    def __del__(self):
        self.df.to_csv(self.PATH)

    def get_by_name(self, name):
        return self.df.get(name)

    def insert(self, row):
        self.df = self.df.append(row, ignore_index=True)

    def write_to_file(self):
        self.df.to_csv(self.PATH)

    def exists(self, key):
        if self.df.get(key, False):
            return True
        return False

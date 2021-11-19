from src.database.database import Database


class SitesDao(Database):
    rel_path = "/files/sites.csv"

    def __init__(self):
        super().__init__(self.rel_path)

    def insert(self, row):
        if not super().exists('url', str(row['url'])):
            self.df = self.df.append(row, ignore_index=True)
            return True

        return False

    @staticmethod
    def get_object():
        """
        Returns empty object, used in db.
        """
        return {'url': None, 'name': None, 'desc': ""}

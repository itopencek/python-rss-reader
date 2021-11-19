from src.database.database import Database


class SitesDao(Database):
    rel_path = "/files/sites.csv"

    def __init__(self):
        super().__init__(self.rel_path)

    @staticmethod
    def get_object():
        """
        Returns empty object, used in db.
        """
        return {'url': None, 'name': None, 'desc': ""}

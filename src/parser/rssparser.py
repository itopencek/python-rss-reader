import pandas
from src.parser.parser import Parser


class RssParser(Parser):
    id = 0

    def __init__(self):
        pass

    def __get_data_frame(self):
        """
        Creates pandas data frame.
        :return: Pandas data frame
        """
        return pandas.DataFrame(columns=['id', 'title', 'published', 'description', 'url'])

    def parse(self, input):
        """
        Parses RSS input into Pandas data_frame.

        :param input: RSS input
        :return: Pandas data_frame
        """
        data_frame = self.__get_data_frame()
        items = input.html.find("item", first=False)

        for item in items:

            title = item.find('title', first=True).text
            pubDate = item.find('pubDate', first=True).text
            guid = item.find('guid', first=True).text
            description = item.find('description', first=True).text

            row = {'title': title, 'pubDate': pubDate, 'guid': guid, 'description': description}
            data_frame = data_frame.append(row, ignore_index=True)

        return data_frame
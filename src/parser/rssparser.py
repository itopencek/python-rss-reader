import pandas
import xml.etree.ElementTree as ET
from src.parser.parser import Parser


class RssParser(Parser):
    next_id = 0

    def __init__(self):
        pass

    @staticmethod
    def __get_data_frame():
        """
        Creates pandas data frame.

        :return: Pandas data frame
        """
        return pandas.DataFrame(columns=['id', 'title', 'published', 'description', 'url', 'source'])

    def parse(self, data):
        """
        Parses RSS input into Pandas data_frame.

        :param data: RSS input - xml in string
        :return: Pandas data_frame
        """
        data_frame = self.__get_data_frame()
        root = ET.fromstring(data)
        channel = root.find("channel")
        source = channel.find("link").text
        for item in channel.findall("item"):
            title = item.find('title').text
            published = item.find('pubDate').text
            description = item.find('description').text
            url = item.find('link').text
            row = {'id': self.__next_id(), 'title': title, 'description': description, 'published': published,
                   'url': url, 'source': source}
            data_frame = data_frame.append(row, ignore_index=True)

        return data_frame.to_dict(orient="records")

    def __next_id(self):
        """
        :return: next free id
        """
        to_return = self.next_id
        self.next_id += 1
        return to_return


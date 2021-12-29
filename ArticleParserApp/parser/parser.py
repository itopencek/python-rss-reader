from datetime import datetime

import pandas
import xml.etree.ElementTree as ElementTree

from jinja2 import Markup


class Parser:
    def parse(self, data):
        """
        Abstract method, which parses data.

        :param data: data, which needs to be parsed
        :return: parsed data
        """
        pass


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
        return pandas.DataFrame(columns=['id', 'title', 'published', 'description', 'url', 'source', 'image_url'])

    def parse(self, data):
        """
        Parses RSS input into Pandas data_frame.

        :param data: RSS input - xml in string
        :return: Pandas data_frame
        """
        data_frame = self.__get_data_frame()
        root = ElementTree.fromstring(data)
        channel = root.find("channel")
        source = channel.find("link").text
        for item in channel.findall("item"):
            title = item.find('title').text
            # date to epoch
            date_time_str = item.find('pubDate').text
            try:
                published_epoch = datetime.strptime(date_time_str, '%a, %d %b %Y %H:%M:%S %z').strftime('%s')
            except ValueError:
                published_epoch = datetime.now().strptime(date_time_str, '%a, %d %b %Y %H:%M:%S %Z').strftime('%s')
            # remove all html tags because there are images sometimes
            description = Markup(item.find('description').text).striptags()
            url = item.find('link').text
            try:
                image_url = str(item.find('enclosure').attrib['url'])
            except AttributeError:
                image_url = ""
            row = {'id': self.__next_id(), 'title': title, 'description': description, 'published': published_epoch,
                   'url': url, 'source': source, 'image_url': image_url}
            data_frame = data_frame.append(row, ignore_index=True)

        return data_frame.to_dict(orient="records")

    def __next_id(self):
        """
        :return: next free id
        """
        to_return = self.next_id
        self.next_id += 1
        return to_return

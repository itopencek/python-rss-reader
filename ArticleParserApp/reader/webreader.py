from http.client import HTTPException
from urllib.error import HTTPError, URLError

from urllib.request import urlopen


class Reader:
    """
    Abstract class to read data from specific source and then returning it.
    """
    def read(self, src):
        """
        Reads data from source, which it then returns.

        :param src: source to read data from
        :return: read data
        """
        pass


class WebReader(Reader):
    """
    Reads and returns web pages.
    """

    def read(self, src):
        """
        Reads and returns specific website.
        :param src: source website
        :return: HttpResponse with website
        """
        try:
            page = urlopen(src)
            html_bytes = page.read()
            html = html_bytes.decode("utf-8")
            return html

        except HTTPError as e:
            print("HttpError while reading website: " + str(src))
            print(e)
        except URLError as e:
            print("UrlError while reading website: " + str(src))
            print(e)
        except HTTPException as e:
            print("HttpException while reading website: " + str(src))
            print(e)
        except Exception as e:
            print("Unspecified exception while reading website: " + str(src))
            print(e)

from src.parser.rssparser import RssParser
from src.reader.webreader import WebReader


def main():
    parser = RssParser()
    reader = WebReader()
    website = reader.read("https://www.sme.sk/rss-title")
    print(parser.parse(website).values)


if __name__ == "__main__":
    main()

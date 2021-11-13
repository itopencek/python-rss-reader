from src.parser.rssparser import RssParser
from src.reader.webreader import WebReader
from flask import Flask
app = Flask(__name__)


@app.route('/')
def main():
    parser = RssParser()
    reader = WebReader()
    website = reader.read("https://www.sme.sk/rss-title")
    data = parser.parse(website).values
    return str(data)


if __name__ == "__main__":
    app.run()

from ArticleParserApp.parser.parser import RssParser
from ArticleParserApp.parser.reader import WebReader

expected_rss = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<rss version=\"2.0\" " \
               "xmlns:atom=\"http://www.w3.org/2005/Atom\" " \
               "xmlns:media=\"http://search.yahoo.com/mrss/\"><channel><title>SME.sk | Najčítanejšie správy na " \
               "Slovensku - titulka</title><link>https://www.sme.sk/rss-title</link><description>Rýchle a " \
               "dôveryhodné správy zo Slovenska, sveta i Vášho regiónu. Prihlásenie do " \
               "Post.sk.</description><webMaster>info@smeonline.sk</webMaster><language>sk</language><ttl>2</ttl" \
               "><item><title>Aj jednoduchý úkon môže trvať týždne. Prečo nie sú elektronické služby štátu ako " \
               "Netflix?</title><description>Elektronicky s úradmi komunikuje len zlomok " \
               "ľudí.</description><pubDate>Sat, 25 Dec 2021 03:07:52 +0100</pubDate><guid " \
               "isPermaLink=\"false\">art-22809178</guid><enclosure " \
               "url=\"https://m.smedata.sk/api-media/media/image/sme/8/75/7535778/7535778_600x400.jpg?rev=5\" " \
               "length=\"0\" type=\"image/jpeg\"/><link>https://www.sme.sk/c/22809178/preco-elektronicke-sluzby-statu" \
               "-vyuziva-len-zlomok-ludi.html</link></item></channel></rss>"


class MockUrlopen:
    @staticmethod
    def read():
        with open('resources/sme.xml', 'rb') as f:
            lines = f.read()
            return lines


def mock_urlopen(src):
    if src == 'https://www.sme.sk/rss-title':
        return MockUrlopen
    else:
        assert False


def test_reader():
    reader = WebReader()
    rv = reader.read(mock_urlopen, 'https://www.sme.sk/rss-title')
    assert rv == expected_rss


def test_parser():
    parser = RssParser()
    rv = parser.parse(expected_rss)
    expected_parsed = "[{'id': 0, 'title': 'Aj jednoduchý úkon môže trvať týždne. Prečo nie sú elektronické služby " \
                      "štátu ako Netflix?', 'published': '1640398072', 'description': 'Elektronicky s úradmi " \
                      "komunikuje len zlomok ľudí.', 'url': " \
                      "'https://www.sme.sk/c/22809178/preco-elektronicke-sluzby-statu-vyuziva-len-zlomok-ludi.html', " \
                      "'source': 'https://www.sme.sk/rss-title', 'image_url': " \
                      "'https://m.smedata.sk/api-media/media/image/sme/8/75/7535778/7535778_600x400.jpg?rev=5'}]"
    assert str(rv) == expected_parsed

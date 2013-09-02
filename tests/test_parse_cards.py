from bs4 import BeautifulSoup
from nose.tools import assert_equals
import datetime
import mythicrss


def test_parse_cards():
    soup = BeautifulSoup(open("tests/cards.html"))
    cards = mythicrss.parse_spoiler(soup)

    assert_equals(75, len(cards))

    cyclops = cards[0]

    assert_equals("Polis Crusher", cyclops.name)
    assert_equals("http://mythicspoiler.com/ths/cards/poliscrusher.html",
                  cyclops.spoiler_url)
    assert_equals("http://mythicspoiler.com/ths/cards/poliscrusher.jpg",
                  cyclops.img_url)
    assert_equals(datetime.date.today().year,
                  cyclops.spoiled.year)


def test_rss_feed():
    soup = BeautifulSoup(open("tests/cards.html"))
    print(mythicrss.spoiler_feed(soup))

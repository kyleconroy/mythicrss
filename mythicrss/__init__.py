import datetime
import requests
import logging
from flask import Flask, Response
from bs4 import BeautifulSoup
import PyRSS2Gen


class Card(object):

    def __init__(self, alt, img_url, source_url, spoiler_url, date):
        self.name = alt.replace("theros", "").strip().title()
        self.img_url = "http://mythicspoiler.com/" + img_url
        self.source_url = source_url
        self.spoiler_url = "http://mythicspoiler.com/" + spoiler_url
        self.spoiled = date

    def description(self):
        return "<img src=\"{}\">".format(self.img_url)


def parse_date(td):
    card_date = td.find('font').string

    if card_date is None:
        return None

    try:
        date = datetime.datetime.strptime(card_date.strip(), "%b %d")
        return date.replace(year=datetime.date.today().year)
    except ValueError:
        pass

    try:
        date = datetime.datetime.strptime(card_date.strip(), "%B %d")
        return date.replace(year=datetime.date.today().year)
    except ValueError:
        pass

    return None


def parse_card(td, date):
    try:
        spoiler_link, source_link = td.find_all('a')
    except ValueError:
        logging.error("Could not find spoiler link or source link")
        return None

    art = spoiler_link.find('img')

    if art is None:
        logging.error("Could not find card art")
        return None

    try:
        return Card(art.get('alt', "Unknown"), art['src'],
                    source_link['href'], spoiler_link['href'], date)
    except KeyError as e:
        logging.error("Couldn't find a needed attribute %s" % e)
        return None


def parse_cards(tds, date):
    cards = []
    for td in tds:
        card = parse_card(td, date)

        if card is not None:
            cards.append(card)

    return cards


def parse_spoiler(soup):
    fbroot = soup.find(id="fb-root")
    spoiler_table = fbroot.find_next_siblings('table').pop()

    card_date = datetime.date.today()
    spoiler = []

    for row in spoiler_table.find_all('tr'):
        cells = row.find_all('td')

        if len(cells) == 1:
            card_date = parse_date(cells[0]) or card_date
        elif len(cells) >= 1:
            spoiler.extend(parse_cards(cells, card_date))

    return spoiler


def spoiler_feed(soup):
    items = []

    for card in parse_spoiler(soup):
        item = PyRSS2Gen.RSSItem(
            title=card.name,
            link=card.spoiler_url,
            description=card.description(),
            guid=PyRSS2Gen.Guid(card.spoiler_url),
            pubDate=card.spoiled
        )

        items.append(item)

    rss = PyRSS2Gen.RSS2(
        title="Mythic Spoiler Latest Cards",
        link="https://mythicrss.herokuapp.com",
        description="Latest cards from new magic sets",
        lastBuildDate=datetime.datetime.now(),
        items=items
    )

    return rss.to_xml()

app = Flask(__name__)


@app.route('/')
def spoiler_rss():
    resp = requests.get('http://mythicspoiler.com/newspoilers.html')
    resp.raise_for_status()
    return Response(spoiler_feed(BeautifulSoup(resp.content)),
                    mimetype="application/rss+xml")


if __name__ == '__main__':
    app.run(debug=True)

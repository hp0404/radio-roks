"""
Python API for scraping Radioroks Playlists
"""
import datetime
import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.radioroks.ua/playlist"
DATE_FORMAT = "%d-%m-%Y"
DATETIME_FORMAT = f"{DATE_FORMAT} %H:%M"


def date_range(start, end):
    current = start
    while current <= end:
        yield current
        current += datetime.timedelta(days=1)


def fetch(date):
    r = requests.get(f"{BASE_URL}/{date}.html")
    r.raise_for_status()
    return r.content


def process_item(item, date):
    if (meta := item.find("div", class_="play-youtube")):
        time = item.find("div", class_="position-absolute time").get_text(strip=True)
        dtime = datetime.datetime.strptime(f"{date} {time}", DATETIME_FORMAT).strftime(DATETIME_FORMAT)
        yield {"datetime": dtime, "artist": meta["singer"], "song": meta["song"]}


def scrape(date):
    if date > datetime.date.today():
        raise ValueError(f"{date} is in the future")
    datestring = date.strftime(DATE_FORMAT)

    content = fetch(datestring)
    soup = BeautifulSoup(content, "html.parser")
    page = soup.find_all("div", class_="row no-gutters")
    for item in page:
        yield from process_item(item, datestring)
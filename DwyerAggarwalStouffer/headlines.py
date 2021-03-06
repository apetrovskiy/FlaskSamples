import feedparser
import json
from urllib.request import urlopen
from urllib.parse import quote
from flask import Flask, render_template, request


app = Flask(__name__)
RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

DEFAULTS = {'publication': 'bbc',
            'city': 'London,UK',
            'currency_from': 'GBP',
            'currency_to': 'USD'}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/" \
              "weather?q={}&units=metric&appid=" \
              "07147b0d16f3958f4584aff355c4ad82"
CURRENCY_URL = "https://openexchangerates.org/api/latest.json?" \
    "app_id=61a10f2443de4ccea6fabcedfd9fadc3"


@app.route("/", methods=['GET', 'POST'])
def home():
    # headlines
    publication = request.form.get("publication")
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    # weather
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    # currency
    currency_from = request.args.get('currency_from')
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.args.get('currency_to')
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate, currencies = get_rate(currency_from, currency_to)
    return render_template("home.html",
                           articles=articles, weather=weather,
                           currency_from=currency_from,
                           currency_to=currency_to,
                           rate=rate,
                           currencies=sorted(currencies))


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_weather(query):
    query = quote(query)
    url = WEATHER_URL.format(query)
    data = urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description":
                   parsed["weather"][0]["description"],
                   "temperature": parsed["main"]["temp"],
                   "city": parsed["name"],
                   'country': parsed['sys']['country']}
    return weather


def get_rate(frm, to):
    all_currency = urlopen(CURRENCY_URL).read()
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate/frm_rate, parsed.keys())

if __name__ == "__main__":
    app.run(port=5000, debug=True)

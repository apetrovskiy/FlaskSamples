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
            'city': 'London,UK'}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/" \
              "weather?q={}&units=metric&appid=" \
              "07147b0d16f3958f4584aff355c4ad82"


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
    return render_template("home.html",
                           articles=articles, weather=weather)


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
                   "city": parsed["name"]}
    return weather

if __name__ == "__main__":
    app.run(port=5000, debug=True)

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


@app.route("/", methods=['GET', 'POST'])
def get_news():
    query = request.form.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    weather = get_weather("London,UK")
    return render_template("home.html",
                           articles=feed['entries'], weather=weather)


def get_weather(query):
    api_url = "http://api.openweathermap.org/data/2.5/" \
              "weather?q={}&units=metric&appid=07147b0d16f3958f4584aff355c4ad82"
    query = quote(query)
    url = api_url.format(query)
    data = urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description":
                   parsed["weather"][0]["description"],
                   "temparature": parsed["main"]["temp"],
                   "city": parsed["name"]}
    return weather

if __name__ == "__main__":
    app.run(port=5000, debug=True)
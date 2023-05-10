from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import ssl
import urllib.parse
import sentiment


def get_headlines(self, company_name, num_headlines):
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    root = "https://www.google.com/"
    query = f"{company_name} news"
    params = {
        "client": "firefox-b-1-d",
        "hl": "en",
        "q": query,
        "tbm": "nws",
        "biw": 1512,
        "bih": 865,
        "dpr": 2,
        "tbs": "qdr:d",
    }

    url = root + "search?" + urllib.parse.urlencode(params)

    headlines = []

    while len(headlines) < num_headlines:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        webpage = urlopen(req).read()

        with requests.Session() as c:
            soup = BeautifulSoup(webpage, "html5lib")
            for item in soup.find_all("div", attrs={"class": "DnJfK"}):
                headline = (
                    item.find("div", attrs={"class": "BNeawe vvjwJb AP7Wnd"})
                    .get_text()
                    .replace(",", "")
                )
                headlines.append(headline)
                if len(headlines) >= num_headlines:
                    break

            next_page_link = soup.find("a", attrs={"aria-label": "Next page"})
            if not next_page_link:
                break

            url = root + next_page_link["href"]

    return headlines


company_name = "google"
num_headlines = 5
headlines = scraper.get_headlines(company_name, num_headlines)

sentiment_analysis = sentiment.SentimentAnalysis()
sentiment_metric = sentiment_analysis.getSentiment(headlines)
print(f"The sentiment of {company_name}'s stock performance is {sentiment_metric}.")

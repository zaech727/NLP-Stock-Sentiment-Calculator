from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import ssl
import urllib.parse


def get_headlines(company_name, num_headlines=20):
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
        "sa": "X",
    }

    url = root + "search?" + urllib.parse.urlencode(params)

    headlines = []
    i = 0
    while i < num_headlines:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        webpage = urlopen(req).read()

        with requests.Session() as c:
            soup = BeautifulSoup(webpage, "html5lib")
            for item in soup.find_all(
                "div", attrs={"class": "Gx5Zad fP1Qef xpd EtOod pkphOe"}
            ):
                # Combine description and headline to give model more context for sentiment analysis
                description = (
                    item.find("div", attrs={"class": "BNeawe s3v9rd AP7Wnd"})
                    .get_text()
                    .replace(",", "")
                )

                headline = (
                    item.find("div", attrs={"class": "BNeawe vvjwJb AP7Wnd"})
                    .get_text()
                    .replace(",", "")
                )

                text = headline + ". " + description
                headlines.append(text)
                i += 1

            next_page_link = soup.find("a", attrs={"aria-label": "Next page"})
            if not next_page_link:
                break

            url = root + next_page_link["href"]

    return headlines

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import ssl
import urllib.parse

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


root = 'https://www.google.com/'
query = 'apple news'
params = {'client': 'firefox-b-1-d',
          'hl': 'en',
          'q': query,
          'tbm': 'nws',
          'biw': 1512,
          'bih': 865,
          'dpr': 2}

url = root + 'search?' + urllib.parse.urlencode(params)

while True:
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()

    with requests.Session() as c:
        soup = BeautifulSoup(webpage, 'html5lib')

        for item in soup.find_all('div', attrs={'class': 'Gx5Zad fP1Qef xpd EtOod pkphOe'}):
            raw_link = item.find('a', href=True)['href']
            link = urllib.parse.unquote((raw_link.split("/url?q=")[1]).split('&sa=U&')[0])
            title = item.find('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'}).get_text().replace(',', '')

            print(title)
            print(link)

            # write to a CSV file
            with open('data.csv', 'a') as f:
                f.write(f'{title}, {link}\n')

        next_page_link = soup.find('a', attrs={'aria-label': 'Next page'})
        if not next_page_link:
            break

        url = root + next_page_link['href']

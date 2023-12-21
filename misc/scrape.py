import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup


urls = []
quarts = [1, 2, 3, 4]
fys = list(range(13, 24))
for fy in fys:
    for quart in quarts:
        url = f"https://thewaltdisneycompany.com/disneys-q{quart}-fy{fy}-earnings-results-webcast/"
        urls.append(url)


folder_location = 'data/'

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    for link in soup.select("a[href$='.pdf']"):
        # Name the pdf files using the last portion of each link which are unique in this case
        filename = os.path.join(folder_location, link['href'].split('/')[-1])
        with open(filename, 'wb') as f:
            f.write(requests.get(urljoin(url, link['href'])).content)


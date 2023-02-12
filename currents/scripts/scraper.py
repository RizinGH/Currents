
import requests
from bs4 import BeautifulSoup
import csv

def timesofindia():
    url = "https://timesofindia.indiatimes.com/home/headlines"
    page_request = requests.get(url)
    data = page_request.content
    soup = BeautifulSoup(data,"html.parser")

    counter = 0
    headlines = [["slno", "url"]]

    for divtag in soup.find_all('div', {'class': 'headlines-list'}):
        for ultag in divtag.find_all('ul', {'class': 'clearfix'}):
            if (counter <= 10):
                for litag in ultag.find_all('li'):
                    counter = counter + 1
                    # print(str(counter) + " - https://timesofindia.indiatimes.com" + litag.find('a')['href'])
                    headlines.append([str(counter), "https://timesofindia.indiatimes.com" + litag.find('a')['href']])

    with open("toi.csv", 'w') as csvfile:
        
        writer = csv.writer(csvfile)
        writer.writerows(headlines)

if __name__ == "__main__":
    timesofindia()
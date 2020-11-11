import requests
from bs4 import BeautifulSoup
import lxml
from datetime import datetime
from datetime import timedelta
import time

def GetURLS(date):
    url = 'https://www.racingzone.com.au/results/{}/'.format(date)
    page = requests.get(url)
    page.content
    soup = BeautifulSoup(page.content, 'lxml')
    #unwanted = soup.find_all('table', {'class':'results-table--international'})
    #for match in unwanted:
    #    match.decompose()
    racelinks = soup.find_all('td', {'class':'popup-race'})
    #print(tables)
    for link in racelinks:
        try:
            links = link.find('a')
            href = links['href']
            fullurl = 'https://www.racingzone.com.au{}'.format(href)
            print(fullurl)
            with open('C:/scratch/racingzone.txt', 'a') as myfile:
                myfile.write('{}\n'.format(fullurl))
        except:
            continue


startdatewhole = datetime(2017, 1, 1)
end_date = datetime(2020, 9, 16)
delta = timedelta(days=1)
while startdatewhole <= end_date:
    startdate = startdatewhole.strftime('%Y-%m-%d')
    print(startdate)
    GetURLS(startdate)
    startdatewhole += delta
    time.sleep(1)
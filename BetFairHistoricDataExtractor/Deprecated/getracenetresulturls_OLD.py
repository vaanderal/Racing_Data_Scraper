import requests
from bs4 import BeautifulSoup
import lxml
import pandas
from datetime import datetime
from datetime import timedelta
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache'
}

def GetRacenetResultURLS(date):
    url = 'https://www.racenet.com.au/api/results/date/{}'.format(date)
    test = requests.get(url, headers=headers)
    soup = BeautifulSoup(test.content, 'lxml')
    urls = soup.find_all('div', {'class':'table-race-meeting-detail table-race-meeting-detail-ended js-quick-results-popover'})
    for url in urls:
        print('https://www.racenet.com.au{}'.format(url.a['href']))
        with open('C:/scratch/racenetresults.txt', 'a') as myfile:
            myfile.write('https://www.racenet.com.au{}'.format(url.a['href']))

startdatewhole = datetime(1, 1, 2017)
end_date = datetime(30, 9, 2020)
delta = timedelta(days=1)
while startdatewhole <= end_date:
    startdate = startdatewhole.strftime('%d-%m-%Y')
    print(startdate)
    GetRacenetResultURLS(startdate)
    startdatewhole += delta
    time.sleep(5)

import requests
from bs4 import BeautifulSoup
import lxml
from datetime import datetime
from datetime import timedelta
import time

def GetURLS(date):
    url = 'https://www.punters.com.au/racing-results/{}/'.format(date)
    page = requests.get(url)
    page.content
    soup = BeautifulSoup(page.content, 'lxml')
    unwanted = soup.find_all('table', {'class':'results-table--international'})
    for match in unwanted:
        match.decompose()
    tables = soup.find_all('table', {'class':'results-table'})
    print(tables)
    for table in tables:
        spans = table.find_all('span', {'class':'results-table__capital results-table__form-guide'})
        print(spans)
        for span in spans:
            links = span.find('a')
            href = links['href']
            fullurl = 'https://www.punters.com.au{}#FullForm'.format(href)
            print(fullurl)
            with open('C:/scratch/test4.txt', 'a') as myfile:
                myfile.write('{}\n'.format(fullurl))

startdatewhole = datetime(2019, 2, 12)
end_date = datetime(2020, 9, 16)
delta = timedelta(days=1)
while startdatewhole <= end_date:
    startdate = startdatewhole.strftime('%Y-%m-%d')
    print(startdate)
    GetURLS(startdate)
    startdatewhole += delta
    time.sleep(1)

#url = 'https://www.punters.com.au/racing-results/2018-12-27/'
#page = requests.get(url)
#page.content
#soup = BeautifulSoup(page.content, 'lxml')
#tables = soup.find_all('table', {'class':'results-table'})
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


def GetPuntersResultTimes(date):
    url = 'https://www.punters.com.au/racing-results/{}/'.format(date)
    test = requests.get(url, headers=headers)
    soup = BeautifulSoup(test.content, 'lxml')
    resultdf = pandas.DataFrame()
    resultstable = soup.find('div', {'class':'results-tables'})
    indres = resultstable.find_all('div', {'class':'results-meeting'})
    for x in indres:
        resultdict = {}
        try:
            trackname = x.find('a', {'class':'results-meeting__full-results-link'}).text
        except:
            trackname = 'error'
            continue
        allrestab = x.find_all('table', {'class':'results-table'})
        for table in allrestab:
            try:
                raceno = table.find('b', {'class':'results-table__capital'}).text
                distance = table.find('abbr', {'class':'conversion'}).text
                firstplace = table.find('tr', {'class':'isFirst results-table__isPlaced'})
            except:
                continue
            try:
                cells = firstplace.find_all('td')
                if cells[4]:
                    try:
                        winningtime = cells[4].text
                    except:
                        winningtime = '0:00.00'
                        continue
                    resultdict['Date'] = date
                    resultdict['TrackName'] = trackname
                    resultdict['RaceNo'] = raceno
                    resultdict['Distance'] = distance
                    resultdict['Time'] = winningtime
                    resultdf = resultdf.append(resultdict, ignore_index=True)
                else:
                    continue

            except:
                continue
    resultdf.to_csv('C:/Scratch/puntersresults/{}.csv'.format(date), index = False)



startdatewhole = datetime(2020, 10, 1)
end_date = datetime(2020, 11, 11)
delta = timedelta(days=1)
while startdatewhole <= end_date:
    startdate = startdatewhole.strftime('%Y-%m-%d')
    print(startdate)
    GetPuntersResultTimes(startdate)
    startdatewhole += delta
    time.sleep(2)
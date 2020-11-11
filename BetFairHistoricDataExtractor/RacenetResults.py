import requests
from bs4 import BeautifulSoup
import lxml
import pandas
from datetime import datetime
from datetime import timedelta
import time
import re

reqheaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache'
}

#url = 'https://www.racenet.com.au/horse-racing-results/belmont-20200603/all-flags-signs-banners-handicap-race-1'

def GetResultsRacenet(url, headers):
    test = requests.get(url, headers=headers)
    soup = BeautifulSoup(test.content, 'lxml')
    if soup.find('div', {'class':'rn-sequence-order'}):
        numberfinder = soup.find('div', {'class':'rn-sequence-order'})
        racenumber = numberfinder.find('span', {'class':'rn-sequence-order-heading'}).text
        print(racenumber)
        distance = soup.find('p', {'class':'rn-race-info-bar-meta'}).text
        raceclass = soup.find('p', {'class':'rn-race-info-bar-meta hidden-xs'}).text
        trackcond = soup.find('span', {'class':'rn-track-condition-bg'}).text
        #Get details from left side of race info
        leftdetails = soup.find('div', {'class':'rn-sxn-form-detail-track-information-left'})
        leftpara = leftdetails.find_all('p')
        try:
            railpos = leftpara[2].text
        except:
            railpos = 'unknown'
            pass
            #continue
        rightdetails = soup.find('div', {'class':'rn-sxn-form-detail-track-information-right'})
        rightpara = rightdetails.find_all('p')
        try:
            trackname = rightpara[0].find('a').text
        except:
            trackname = soup.find('h2', {'class':'rn-expandable-title-heading'}).text
            pass
        print(trackname)
        try:
            timedetails = rightpara[1].find_all('span')
            racetime = timedetails[0].text
        except:
            racetime = '0'
            pass
        try:
            sectional600 = timedetails[1].text
        except:
            sectional600 = '0'
            pass
        #racedatetimefind = soup.find('time')
        #racedatetime = racedatetimefind['datetime']
        racedate = re.search('(\d\d\d\d\d\d\d\d)', url).group(0)

        resultstable = soup.find('div', {'class':'rn-sxn-race-results-table'})
        runners = resultstable.find_all('div', {'class':'rn-table-race-results'})
        resultdf = pandas.DataFrame()

        for runner in runners:
            resultdict = {}
            resultdict['trackname'] = trackname
            resultdict['racenumber'] = racenumber
            resultdict['distance'] = distance
            resultdict['raceclass'] = raceclass
            resultdict['trackcond'] = trackcond
            resultdict['railpos'] = railpos
            resultdict['racetime'] = racetime
            resultdict['sectional600'] = sectional600
            resultdict['racedate'] = racedate
            resultdict['resultspos'] = runner.find('span', {'class':'rn-sequence-order-heading'}).text
            runnerdetails = runner.find('p', {'class':'rn-sxn-horse-name'})
            resultdict['horsename'] = runnerdetails.a.text
            runnerdetails.a.decompose()
            resultdict['barrier'] = runnerdetails.span.text
            runnerdetails.span.decompose()
            resultdict['orderno'] = runnerdetails.strong.get_text(strip=True)
            resultdict['jockey'] = runner.find('span', {'class':'rn-sxn-horse-jockey'}).a.text
            resultdict['trainer'] = runner.find('span', {'class':'rn-sxn-horse-trainer'}).a.text
            resultdict['weight'] = runner.find('div', {'class':'rn-sxn-horse-weight'}).p.get_text(strip=True)
            resultdict['agesex'] = runner.find('div', {'class':'rn-sxn-horse-age hidden-sm hidden-xs'}).get_text(strip=True)
            resultdict['margin'] = runner.find('td', {'class':'rn-table-race-results-data-cell-margin hidden-xs hidden-sm rn-table-race-results-gray-bg'}).text
            resultdict['pos800'] = runner.find('td', {'class':'rn-table-race-results-data-cell-800 hidden-xs hidden-sm rn-table-race-results-gray-text'}).text
            resultdict['pos400'] = runner.find('td', {'class':'rn-table-race-results-data-cell-400 hidden-xs hidden-sm rn-table-race-results-gray-text'}).text
            resultdf = resultdf.append(resultdict, ignore_index=True)
        resultdf.to_csv('C:/Scratch/Racenetresults/{0} {1} {2}.csv'.format(trackname, racenumber, racedate), index=False)
        time.sleep(2)
    return

with open('C:/scratch/racenetresults1.csv', 'r') as txtfile:
    urllist = txtfile.read().splitlines()
    for line in urllist:
        print('Getting results {}'.format(line))
        GetResultsRacenet(line, reqheaders)
        time.sleep(1)

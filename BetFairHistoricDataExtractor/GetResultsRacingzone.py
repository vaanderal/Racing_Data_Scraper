import requests
from bs4 import BeautifulSoup
import lxml
from datetime import datetime
from datetime import timedelta
import time
import pandas
import re

def GetRacingZoneResults(url):
    print(url)
    page = requests.get(url)
    page.content
    soup = BeautifulSoup(page.content, 'lxml')
    heading = soup.find('h1')
    trackcond = heading.find('span', {'class':'white'}).text
    heading.find('span', {'class':'white'}).decompose()
    prizemoney = heading.find('span', {'class':'popup'}).text
    heading.find('span', {'class':'popup'}).decompose()
    distance = heading.find('span').text
    track = soup.find('a', {'class':'sel'}).text
    dateurl = soup.find('a', {'class':'sel'}).attrs['href']
    raceno = soup.find('h3', {'class':'title'}).text
    formtable = soup.find('table', {'class':'formguide'})
    runners = formtable.find_all('tr')
    formdata = {}
    formdata['raceno'] = re.search(r"(\d+)", raceno).group()
    formdata['dateurl'] = dateurl
    formdata['date'] = re.search(r"(\d\d\d\d-\d\d-\d\d)", formdata['dateurl']).group()
    formdata['trackcond'] = trackcond
    formdata['prizemoney'] = prizemoney
    formdata['distance'] = distance
    formdata['track'] = track
    df = pandas.DataFrame()

    for runner in runners:
        try:
            horsename = runner.find('td', {'class':'horse'})
            formdata['horsename'] = horsename.find('a').text
            cells = runner.find_all('td')
            formdata['Position'] = cells[0].text
            formdata['margin'] = cells[1].text
            #cells[2] is silks, skip
            cellspan = cells[3].find_all('span')
            if cells[3].find('span', {'class':'info'}):
                formdata['age_sex'] = cellspan[0].text
                formdata['trainer_jockey'] = cellspan[2].text
                formdata['gear'] = cellspan[1].text
            else:
                formdata['age_sex'] = cellspan[0].text
                formdata['trainer_jockey'] = cellspan[1].text
                formdata['gear'] = 'na'
            formdata['odds'] = cells[4].text
            formdata['barrier'] = cells[5].text
            formdata['weight'] = cells[6].text
            formdata['settled'] = cells[7].text
            formdata['pos1200'] = cells[8].text
            formdata['pos800'] = cells[9].text
            formdata['pos400'] = cells[10].text
            formdata['steward'] = cells[11].text 
            df = df.append(formdata, ignore_index=True)
        except:
            continue
    #Change this output to match the directory you'd like to save the files to
    df.to_csv('C:/Scratch/racingzoneresults/{0} {1} Race {2}.csv'.format(track, formdata['date'], formdata['raceno']), index = False)
    time.sleep(1)
    return(df)

#Here there is a call to open the text file that contains the URLs of all the results pages. Rename as required
with open('C:/scratch/racingzone_nonz1.txt', 'r') as txtfile:
    urllist = txtfile.read().splitlines()
    for line in urllist:
        GetRacingZoneResults(line)
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

def tocsv():
    outname = 'data.csv'

    outdir = './dir'
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    fullname = os.path.join(outdir, outname)    

    df.to_csv(fullname)


def parseclassrows(url, classname):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    [s.extract() for s in soup('sup')]
    table = soup.find('table', {'class': classname}).tbody
    return table.find_all('tr')

#scrape initial data from wikipedia page
URL = 'https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population'
rows = parseclassrows(URL, 'wikitable sortable')
columns = [v.text.replace('\n', '') for v in rows[0].find_all('th')]

del columns[-1] #delete location column
columns[6] = columns[6] + " sqmi"
columns[7] = columns[7] + " /sqmi"

#add new columns:
columns.append('Number of Outgoing Links')
columns.append('Mayor')
columns.append('Political Party of Mayor')
columns.append('County')


#create dataframe
df = pd.DataFrame(columns=columns)

def parsehtml(tds, classname, params):
    link = tds.find('a').get('href')
    url = 'https://en.wikipedia.org' + link
    rows = parseclassrows(url, classname)
    for row in rows:
        if row.find('a') != None:
            for param in params:
                if row.find('a').text == param:
                    txt = row.find('td').find('a').text
                    return txt
    return ''

def parsehtmlmayor(tds, classname):
    link = tds.find('a').get('href')
    url = 'https://en.wikipedia.org' + link
    rows = parseclassrows(url, classname)
    for row in rows:
        if row.find('a') != None:
            if row.find('a').text == 'Mayor':
                txt = row.find('td').text
                return txt
    return ''

#for each city
for i in range(1, 80):
    tds = rows[i].find_all('td')
    
    #Initial table data minus location
    values = [td.text.replace('\n', '').replace('\xa0', '').replace('\ufeff', '') for td in tds]
    del values[-2]
    del values[-3]
    del values[-1]

    values[6] = values[6].replace('sqmi', '')
    values[7] = values[7].replace('/sqmi', '')

    #number of links on page
    link = tds[1].find('a').get('href')
    url = 'https://en.wikipedia.org' + link
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    [s.extract() for s in soup('sup')]
    numlinks = len(soup.find_all('a'))
    values.append(numlinks)

    #Mayor data
    mayor = parsehtmlmayor(tds[1], 'infobox geography vcard')
    values.append(mayor)
    
    if mayor.find('(') >=0:
        if mayor[mayor.find('(') + 1] == 'D':
            values.append('Democrat')
        elif mayor[mayor.find('(') + 1] == 'R':
            values.append('Republican')
        else:
            values.append('Third Party/Independent')
    else:
        values.append('NA')

    if values[-2].find('(') >-1:
        values[-2] = values[-2][:values[-2].find('(')-1]

    #County data
    values.append(parsehtml(tds[1], 'infobox geography vcard', ['County', 'Counties', 'Constituent counties']))
    if values[-1] == '':
        values[-1] = values[1]

    

    df = df.append(pd.Series(values, index=columns), ignore_index=True)

    tocsv()

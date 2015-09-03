'''
Created on Sep 2, 2015

@author: Ashis
'''

#include the 2 below exports for .exe creation with pyinstaller
import Tkinter
import FileDialog

from lxml import html
import requests
import time
import re
import calendar
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools
from matplotlib.pyplot import flag


#class Month(OrderedEnum):
        
#months = ['January', 'February', 'March', 'Apriil','May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
#list(enumerate(months, start=1))


searchterms = raw_input('Enter your WSJ search:')

page = requests.get('http://www.wsj.com/search/term.html?KEYWORDS=+' +  searchterms +'&isAdvanced=true&min-date=1911/09/03&max-date=' + time.strftime("%Y/%m/%d") + '&daysback=4y&andor=AND&sort=date-desc&source=wsjarticle,wsjblogs,wsjvideo,sitesearch')

#page = requests.get('http://www.wsj.com/search/term.html?KEYWORDS=+' + searchterms + '&isAdvanced=true&min-date=1911/09/03&max-date=2015/09/03&daysback=4y&andor=AND&sort=date-desc&source=wsjarticle,wsjblogs,wsjvideo,sitesearch')

tree = html.fromstring(page.text)

totalpages = str(tree.xpath('//div[@class="results-menu-wrapper bottom"]//menu[@class="results"]//li[@class="results-count"]/text()'))

totalpages = re.sub(r"[\D]", "", totalpages)

print('There are a total of', totalpages, 'pages enter the number of pages you\'d like to search (max 50):')

pagetotal=raw_input()   

print('Searching', searchterms, 'for', pagetotal, 'pages.')


pagetotal = int(pagetotal)

dates_raw = []



for i in range(1,pagetotal+1): 
    page = requests.get('http://www.wsj.com/search/term.html?KEYWORDS=+' + searchterms +'&isAdvanced=true&min-date=1911/09/03&max-date=' + time.strftime("%Y/%m/%d") + '&andor=AND&sort=date-desc&source=wsjarticle,wsjblogs,wsjvideo,sitesearch&page=' + str(i))
    tree = html.fromstring(page.text)
    dates_raw.append(tree.xpath('//div[@class="headline-container"]//time/text()'))

dates_raw = list(itertools.chain(*dates_raw))

dates = [re.sub(r"[.,]|\W\d*:(.*)","", dates_raw[x]) for x in range(len(dates_raw))]


for y in range(len(dates)):
    try:
        try:
            dates[y] = time.strptime(dates[y], "%b %d %Y")
        except:
            dates[y] = time.strptime(dates[y], "%B %d %Y")
        dates[y] = time.strftime("%B %Y", dates[y])    
    except:
        dates[y] = time.strftime("%B %d %Y")
        dates[y] = time.strptime(dates[y], "%B %d %Y")
        dates[y] = time.strftime("%B %Y", dates[y])    
    
ps = pd.Series(dates)

df = ps.str.split(" ").apply(pd.Series)


df.columns = ['Month', 'Year']

size = df.groupby(['Month', 'Year'], sort=False).size()



df =pd.Series(size.values, index = ps.unique())

print(df)

df.plot(kind = 'bar')
plt.gca().invert_xaxis()

plt.show()

#df = pd.DataFrame({'Count':ps.value_counts(sort=False)})

#print(ps.value_counts(sort=False).index)

#df.reindex([""])
#print(df.axes)

#df.plot(kind = "bar")
#plt.show()

#df = pd.DataFrame({'Date':dates})
#print(list(df.columns.values))
#print(df.values)
#date_sum = df.groupby('Date').size()


#date_groups = df.groupby('Date').groups

#print(date_sum)
#print(df.groupby('Date').)

#date_sum.plot(kind = "bar")

#plt.show()




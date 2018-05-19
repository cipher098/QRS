from urllib.request import urlopen
from bs4 import BeautifulSoup
import bs4
from datetime import date
import calendar
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

cdate = date.today()
day = str(cdate.day) + '-' + (calendar.month_name[cdate.month])[:3] + '-' + str(cdate.year)

url = 'http://www.moneycontrol.com/stocks/marketinfo/meetings.php?opttopic=brdmeeting'
html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')
tags = soup('tr')

scrip = []
pattern = '/stockpricequote/'

for tag in tags:
    # itr = 0
    for each in tag:
        if (type(each) == bs4.element.Tag):
            if(type(each.contents[0]) == bs4.element.Tag):
                url = each.contents[0].get('href', None)
                if (url is not None):
                    if (pattern in url):
                        temp = (re.findall('/stockpricequote/[a-z 0-9]*/[a-z 0-9]*/([^/]+)', str(url)))
                        if len(temp) > 0:
                            temp_scrip = temp[0]
                        else:
                            break
                    else:
                        break
                else:
                    break

            if(type(each.contents[0] == bs4.element.NavigableString)):
                if (each.contents[0] == day):
                    scrip.append(temp_scrip)

print (scrip)
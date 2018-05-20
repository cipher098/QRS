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
# day = '21-May-2018'

def scripList():
    url = 'http://www.moneycontrol.com/stocks/marketinfo/meetings.php?opttopic=brdmeeting'
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup('tr')

    scrip = []
    pattern = '/stockpricequote/'

    for tag in tags:
        for each in tag:
            if (type(each) == bs4.element.Tag):
                if(type(each.contents[0]) == bs4.element.Tag):
                    url = each.contents[0].get('href', None)
                    if (url is not None):
                        if (pattern in url):
                            temp = (re.findall('/stockpricequote/[a-z 0-9]*/[a-z 0-9]*/([^/]+)', str(url)))
                            if len(temp) > 0:
                                temp_scrip = []
                                temp_scrip.append(each.contents[0].contents[0].contents[0])
                                temp_scrip.append(temp[0])
                            else:
                                break
                        else:
                            break
                    else:
                        break

                if(type(each.contents[0] == bs4.element.NavigableString)):
                    if (each.contents[0] == day):
                        scrip.append(temp_scrip)
    return scrip

def getNameInSmall(name):
    f_name = name.lower()
    f_name = f_name.replace(' ', '')
    return f_name

def checkResult(netSales, eps):
    crfo = float(netSales[0])
    prfo = float(netSales[1])
    lrfo = float(netSales[2])
    cqe = float(eps[0])
    pqe = float(eps[1])
    lqe = float(eps[2])
    if(cqe > lqe and crfo > prfo):
        if(cqe <= 1 and (cqe >= pqe + 0.25)):
            return True
        elif(cqe <= 2 and (cqe >= pqe+0.5)):
            return True
        elif(cqe <= 10 and cqe > 2 and (cqe >= pqe+1)):
            return True
        elif(cqe > 10 and (cqe >= pqe + 1.5)):
            return True
    return False

def findMonth():
    if(cdate.month >= 1 and cdate.month <= 3):
        month = (calendar.month_name[12])[:3] + ' \'' + str(cdate.year - 2001)
    elif(cdate.month >= 4 and cdate.month <= 6):
        month = (calendar.month_name[3])[:3] + ' \'' + str(cdate.year - 2000)
    elif(cdate.month >= 7 and cdate.month <= 9):
        month = (calendar.month_name[6])[:3] + ' \'' + str(cdate.year - 2000)
    elif(cdate.month >= 10 and cdate.month <= 12):
        month = (calendar.month_name[9])[:3] + ' \'' + str(cdate.year - 2000)
    return month

def findingResult(scrip):
    fix_url_start = 'http://www.moneycontrol.com/financials/'
    fix_url_end = '/results/quarterly-results/'
    for val in scrip:
        # small_name = 'sagarsoft'
        # code = 'S24'
        print('Finding result for : ', val[0])
        month = findMonth()
        # month = 'May \'18'
        small_name = getNameInSmall(val[0])
        code = val[1]
        url = fix_url_start + small_name + fix_url_end + code + '#' + code
        html = urlopen(url, context=ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup('tr')
        netSales = []
        st1 = False
        st2 = False
        st3 = False
        st4 = False
        eps = []
        for tag in tags:
            for each in tag:
                if(type(each) == bs4.element.Tag):
                    try:
                        if(len(each.contents) > 0):
                            if(each.contents[0] == month):
                                st4 = True
                            if(st4):
                                if(each.contents[0] == 'Net Sales/Income from operations'):
                                    st1 = True
                                    i = 0
                                elif(st1 and i < 3):
                                    netSales.append(each.contents[0])
                                    i = i+1
                                    if(i == 3):
                                        st1 = False
                                if(each.contents[0] == 'EPS After Extra Ordinary'):
                                    st2 = True

                                elif(st2 and each.contents[0] == 'Basic EPS'):
                                    i = 0

                                elif(st2 and i < 3):
                                    eps.append(each.contents[0])
                                    i = i + 1
                                    if(i == 3):
                                        st2 = False
                                        st3 = True
                                        break
                    except:
                        pass
            if(st3):
                print(netSales)
                print(eps)
                result = checkResult(netSales, eps)
                val.append(result)
                print (result)
                break


def main():
    scrip = scripList()
    length = len(scrip)
    if(length > 0):
        print('Total ' , length, ' scrips found.')
        print('Finding Results')
        result = findingResult(scrip)


if __name__ == "__main__":
    main()
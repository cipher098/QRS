from urllib.request import urlopen
from bs4 import BeautifulSoup
import bs4
import datetime
from datetime import date
import calendar
import ssl
import re
import openpyxl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

cdate = date.today()
day = str(cdate.day) + '-' + (calendar.month_name[cdate.month])[:3] + '-' + str(cdate.year)
# day = '21-May-2018'

def scripList():
    url = 'http://www.moneycontrol.com/stocks/marketinfo/meetings.php?opttopic=brdmeeting'
    tstart = datetime.datetime.now().timestamp()
    html = urlopen(url, context=ctx).read()
    tend = datetime.datetime.now().timestamp()
    # internetTime = internetTime + (tend - - tstart)
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

def findingResult(scrip, fCount, internetTime):
    fix_url_start = 'http://www.moneycontrol.com/financials/'
    fix_url_end = '/results/quarterly-results/'
    ind = 0
    for val in scrip:
        ind = ind + 1
        # small_name = 'sagarsoft'
        # code = 'S24'
        print(str(ind) + '. Finding result for : ', val[0])
        month = findMonth()
        # month = 'May \'18'
        small_name = getNameInSmall(val[0])
        code = val[1]
        url = fix_url_start + small_name + fix_url_end + code + '#' + code
        tstart = datetime.datetime.now().timestamp()
        html = urlopen(url, context=ctx).read()
        tend = datetime.datetime.now().timestamp()
        internetTime = internetTime + (tend - tstart)
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup('tr')
        # print(len(tags))
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
                                elif(each.contents[0] == 'EPS After Extra Ordinary'):
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
                # print(netSales)
                # print(eps)
                result = checkResult(netSales, eps)
                val.append(result)
                fCount = fCount + 1
                # print (result)
                break
    return scrip, fCount, internetTime


def main():
    # global internetTime
    internetTime = 0.0
    fCount = 0
    startTime = datetime.datetime.now().timestamp()
    print('Hey!')
    print('Finding list of scrips announced today.')
    scrip = scripList()
    length = len(scrip)
    if(length > 0):
        print('Total ', length, ' companies announced results today.')
        print('Finding Results')
        result, fCount, internetTime = findingResult(scrip, fCount, internetTime)
        print('Results found.')
        print('Exporting results to excel fiile.....')
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = 'Result ' + day
        i = 1
        for val in result:
            sheet['A' + str(i)] = val[0]
            if(len(val) > 2):
                if(val[2]):
                    sheet['B' + str(i)] = 'Yes'
                else:
                    sheet['B' + str(i)] = 'No'
            i = i + 1
        wb.save('Result ' + day + '.xlsx')
        print('Result exported. File saved as Result ' + day + '.xlsx .')
        endTime = datetime.datetime.now().timestamp()
        totalTime = ((endTime - startTime)/60)
        internetTime = internetTime / 60
        print('Total time taken by program to find result of ', fCount, 'is : ', totalTime, ' minutes.')
        print('Total time taken for getting data from internet : ', internetTime, ' minutes.')
        print('Shutting Down.....!!')


if __name__ == "__main__":
    main()
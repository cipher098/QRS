import sys
import time
import calendar
import lxml
from lxml import etree
from StringIO import StringIO

#Have to update check table to get proper table.
def checkTable(strng):
	#regular expression
	if(type(strng) == str):
		strng1 = strng.lower()
		if('financial' in strng1 and ('result' in strng1 or 'results' in strng1) and 'consolidated' not in strng1):
			return True
	return False

def checkTable1(strng):
	#regular expression
	# print(strng)
	if(type(strng) == str):
		strng1 = strng.lower()
		if('particulars' in strng1):
			return True
	return False

def convertBbox(bbox):
	return bbox[1:-1].split()

monthName = {1:'jan', 2:'feb', 3:'mar',4:'apr', 5:'may', 6:'jun', 7:'jul', 8:'aug', 9:'sep', 10:'oct', 11:'nov', 12:'dec'}

def getMonths():
	#use date time module
	tme = time.localtime(time.time())
	year = tme[0]
	cur = tme[1]
	cur = cur - (cur % 3)
	if(cur == 3):
		prev = 12
	else:
		prev = cur - 3

	if(cur == 3 or cur == 12):
		dateCur = 31
	else:
		dateCur = 30

	if(prev == 3 or prev == 12):
		datePrev = 31
	else:
		datePrev = 30

	cur = monthName[cur]
	prev = monthName[prev]

	return cur, prev, dateCur, datePrev, year


def findFig(root):
	# for page in root:
	# 	for img in page:
	# 		for fig in img:
	# 			for txtline in fig:
	# 				for txtbox in txtline:
	# 					if(checkTable(txtbox.text)):
	# 						print 'check true'
	# 						return fig

	#Iterating over pages
	for page in root:
		if type(page) is lxml.etree._Element:
			st1 = False
			st2 = False
			for txtbox in page.iter():
				if(checkTable(txtbox.text)):
					st1 = True

				if(checkTable1(txtbox.text)):
					st2 = True
				if st1 and st2:
					return page
	return False

def sortRevVal(dix):
	lst = []
	for key in dix:
		try:
			float(key)
		except:
			try:
				import unicodedata
				unicodedata.numeric(key)
			except:
				lst.append(key)
	for key in lst:
		del dix[key]
	return dix

def check(value, value1, y0, y1):
	if(value >= y0 and value <= y1):
		return True
	if(value1 >= y0 and value1 <= y1):
		return True
	return False


fname = sys.argv[1]
f = open(fname)
xml = f.read()
f.close()

tree = etree.parse(StringIO(xml))

#Gets root of document
root = tree.getroot()
fig = findFig(root)

# cur, prev, dateCur, datePrev, year = getMonths()
#For testing
cur, prev, dateCur, datePrev, year = monthName[12], monthName[9], 31, 30, 2017
bboxCur = []

#Getting bbox of required months and basic
i = 1
# for txtline in fig:
# 	if(txtline is not None):
# 		for txtbox in txtline:
# 			if(len(txtbox) == 0):
# 				if(txtbox is not None):
# 					# print txtbox.text
# 					if(cur in txtbox.text and str(dateCur) in txtbox.text):
# 						bboxCur.append = convertBbox(txtbox.get('bbox'))
# 					elif(prev in txtbox.text and str(datePrev) in txtbox.text):
# 						bboxPrev = convertBbox(txtbox.get('bbox'))
# 					elif('Basic' in txtbox.text):
# 						bboxBasic = convertBbox(txtbox.get('bbox'))
# 					elif('Revenue' in txtbox.text or 'Income' in txtbox.text and 'operations' in txtbox.text):
# 						bboxRevenue = convertBbox(txtbox.get('bbox'))
if type(fig) is lxml.etree._Element:
	for txtbox in fig.iter():
		if txtbox.text is not None:
			if(cur in txtbox.text.lower() and str(dateCur) in txtbox.text):
				bboxCur.append(convertBbox(txtbox.get('bbox')))
			elif(prev in txtbox.text.lower() and str(datePrev) in txtbox.text):
				bboxPrev = convertBbox(txtbox.get('bbox'))
			elif('Basic' in txtbox.text):
				bboxBasic = convertBbox(txtbox.get('bbox'))
			elif('Revenue' in txtbox.text or 'Income' in txtbox.text and 'operations' in txtbox.text):
				bboxRevenue = convertBbox(txtbox.get('bbox'))


	# print bboxRevenue
	if(bboxCur[0][0] > bboxCur[1][0]):
		bboxCurc = bboxCur[1]
		bboxCurl = bboxCur[0]

	bboxVal = {}
	bboxRevVal = {}
	y0 = bboxBasic[1]
	y1 = bboxBasic[3]
	ry0 = bboxRevenue[1]
	ry1 = bboxRevenue[3]

	# for txtline in fig:
	# 	if (txtline is not None):
	# 		for txtbox in txtline:
	# 			if(txtbox is not None):
	# 				if(check(txtbox.get('y0'), txtbox.get('y1'), y0, y1)):
	# 					pr = []
	# 					pr.append(convertBbox(txtbox.get('bbox')))
	# 					pr.append(txtbox.text)
	# 					bboxVal.append(pr)
	# 				if(check(txtbox.get('y0'), txtbox.get('y1'), ry0, ry1)):
	# 					pr = []
	# 					pr.append(convertBbox(txtbox.get('bbox')))
	# 					pr.append(txtbox.text)
	# 					bboxRevVal.append(pr)


	for txtbox in fig.iter():
		if(txtbox is not None):
			if(check(txtbox.get('y0'), txtbox.get('y1'), y0, y1)):
				bboxVal[txtbox.text] = convertBbox(txtbox.get('bbox'))
			if(check(txtbox.get('y0'), txtbox.get('y1'), ry0, ry1)):
				bboxRevVal[txtbox.text] = convertBbox(txtbox.get('bbox'))

	bboxRevVal = sortRevVal(bboxRevVal)

	for ele, val in bboxRevVal.iteritems():
		print(ele, val)
else:
	print("Table not found")
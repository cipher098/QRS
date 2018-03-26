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
		if('financial' in strng1 and 'result' in strng1 and 'consolidated' not in strng1):
			return True
	return False


def convertBbox(bbox):
	return bbox[1:-1].split()


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

	cur = calendar.month_name[cur]
	prev = calendar.month_name[prev]

	return cur, prev, dateCur, datePrev, year


def findFig(root):
	#Iterating over pages
	for page in root:
		for img in page:
			for fig in img:
				for txtline in fig:
					for txtbox in txtline:
						if(checkTable(txtbox.text)):
							print 'check true'
							return fig
	return False


def check(value, value1, y0, y1):
	if(value >= y0 and value <= y1):
		return True
	if(value1 >= y0 and value1 <= y1):
		return True
	return False


# fname = sys.argv[1]
f = open(fname)
xml = f.read()
f.close()

tree = etree.parse(StringIO(xml))

#Gets root of document
root = tree.getroot()
fig = findFig(root)

# cur, prev, dateCur, datePrev, year = getMonths()
#For testing
cur, prev, dateCur, datePrev, year = calendar.month_name[12], calendar.month_name[9], 31, 30, 2017
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

for txtbox in fig.iter():
	if txtbox.text is not None:
		if(cur in txtbox.text and str(dateCur) in txtbox.text):
			bboxCur.append(convertBbox(txtbox.get('bbox')))
		elif(prev in txtbox.text and str(datePrev) in txtbox.text):
			bboxPrev = convertBbox(txtbox.get('bbox'))
		elif('Basic' in txtbox.text):
			bboxBasic = convertBbox(txtbox.get('bbox'))
		elif('Revenue' in txtbox.text or 'Income' in txtbox.text and 'operations' in txtbox.text):
			bboxRevenue = convertBbox(txtbox.get('bbox'))


print bboxRevenue
if(bboxCur[0][0] > bboxCur[1][0]):
	bboxCurc = bboxCur[1]
	bboxCurl = bboxCur[0]

bboxVal = []
bboxRevVal = []
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
			pr = []
			pr.append(convertBbox(txtbox.get('bbox')))
			pr.append(txtbox.text)
			bboxVal.append(pr)
		if(check(txtbox.get('y0'), txtbox.get('y1'), ry0, ry1)):
			pr = []
			pr.append(convertBbox(txtbox.get('bbox')))
			pr.append(txtbox.text)
			bboxRevVal.append(pr)	
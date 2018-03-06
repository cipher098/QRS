import sys
import time
import calendar
import lxml
from lxml import etree
from StringIO import StringIO


def checkTable(strng):
	#regular expression
	strng1 = strng.lower()
	if('financial' in strng1 and 'result' in strng1 and 'consolidated' not in strng1):
		return True
	return false


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

	cur = calendar.month_name(cur)
	prev = calendar.month_name(prev)

	return cur, prev, dateCur, datePrev, year


def finfFig(root):
	#Iterating over pages
	for page in root:
		for img in page:
			for fig in img:
				for txtline in fig:
					for txtbox in txtline:
						if(checkTable(txtbox.text)):
							return fig


def check(value, value1 y0, y1):
	if(value >= y0 and value <= y1):
		return True
	if(value1 >= y0 and value1 <= y1):
		return True
	return False


fname = sys.argv[1]
f = open(fname)
xml = f.read()
f.close()

tree = etree.parse(StringIO(xml), remove_blank_text=True)

#Gets root of document
root = tree.getroot()
fig = finfFig(root)

cur, year = getDate()
cur, prev, dateCur, datePrev, year = getMonths(cur, )
bboxCur = []

#Getting bbox of required months and basic
for txtline in fig:
	for txtbox in txtline:
		if(cur in txtbox.text and dateCur in txtbox.text):
			bboxCur.append = convertBbox(txtbox.get('bbox'))
		elif(prev in txtbox.text and datePrev in txtbox.text):
			bboxPrev = convertBbox(txtbox.get('bbox'))
		elif('Basic' in txtbox.text):
			bboxBasic = convertBbox(txtbox.get('bbox'))


if(bboxCur[0][0] > bboxCur[1][0]):
	bboxCurc = bboxCur[1]
	bboxCurl = bboxCur[0]

bboxVal = []
y0 = bboxBasic[1]
y1 = bboxBasic[3]

for txtline in fig:
	for txtbox in txtline:
		if(check(txtbox.get('y0'), txtbox.get('y1'), y0, y1)):
			bboxVal.append(convertBbox(txtbox.get('bbox')))


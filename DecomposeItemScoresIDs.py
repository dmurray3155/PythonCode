# ------------------------------------------------------------------------------
# FileName: DecomposeItemScoresIDs.py
# Purpose: Split the NV item score and ID vectors into item records in MySQL.
#          This job was progressing slowly using a MySQL stored procedure.
#          This approach aims to speed up the process using a bulk insert.
# Author: Donald Murray
# Date: 2017-12-18 (and ongoing through the end of 2017)
# Notes:
#   This reference provides the sytax for this approach:
#   https://dev.mysql.com/doc/connector-python/en/
#                             connector-python-example-cursor-select.html
# ------------------------------------------------------------------------------

import mysql.connector
from mysql.connector import errorcode

#
# import my toolbox
#
from sys import path
path.append("F:/Python/tools")
from toolbox import prntSec2HMS

#
# This sets the tests.row_num range to process
#
testsRowNumRange = "405001 AND 453975"

#
# Initialize start time for process
#
import time
import datetime
started = time.time()
startTimeVal = datetime.datetime.fromtimestamp(started)
print("Started: " + startTimeVal.strftime('%Y-%m-%d %H:%M:%S'))
print("Range of rows in tests.row_num to process: " + testsRowNumRange)

config = {
'user': 'root',
'password': '@sbac3155',
'host': 'localhost',
'database': 'nv1617',
'raise_on_warnings': True,
}

# Get tests table rows upon which to work
try:
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	# Read some rows from the tests table
	readTestRow = "SELECT row_num, cat_score_string, item_id_string FROM nv1617.tests WHERE row_num BETWEEN " + testsRowNumRange + " AND LENGTH(cat_score_string) > 0"
	cursor.execute(readTestRow)
	tests = []
	#specify the attributes that you want to display
	for (row_num, cat_score_string, item_id_string ) in cursor:
		testsList = [row_num,cat_score_string,item_id_string]
		tests.append(list(testsList))
	cnx.commit()
except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("Something is wrong with your user name or password")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("Database does not exist")
	else:
		print(err)
else:
	cursor.close()
	cnx.close()

# Now process and insert these data into the items table
numOfTestRows = len(tests)
testRow = 0
while testRow < numOfTestRows:
	# Prepare each row to decompose item vector to distinct item records
	insertDataList = []
	tstRowNum = tests[testRow][0]
	catScoreString = tests[testRow][1]
	catScrLen = len(catScoreString)
	catIDString = tests[testRow][2]
	catIDStrLen = len(catIDString)
	testSeq = 1
	while testSeq <= catScrLen:
		insertData = ()
		pyStrSeq = testSeq - 1
		catScr = catScoreString[pyStrSeq:testSeq]
		IDstart = pyStrSeq * 6
		IDend = testSeq * 6
		if catIDStrLen > 0:
			catID = catIDString[IDstart:IDend]
		else:
			catID = 0
		insertData = (tstRowNum, 'CAT', testSeq, int(catID), str(catScr))
		insertDataList.append(tuple(insertData))
		testSeq += 1
	#	print(insertDataList)
	try:
		cnx = mysql.connector.connect(**config)
		cursor = cnx.cursor()
		stmt = "INSERT INTO items (test_row_num, subTest, subTestItemOrder, nvItemId, itemScore) VALUES (%s, %s, %s, %s, %s)"
		cursor.executemany(stmt, insertDataList)
		cnx.commit()
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	else:
		cursor.close()
		cnx.close()
	#	print("Done!")
	testRow += 1

print("Done!")
#
# wrap up time reporting
ended = time.time()
endTimeVal = datetime.datetime.fromtimestamp(ended)
print("Ended: " + endTimeVal.strftime('%Y-%m-%d %H:%M:%S'))
elapsedSeconds = ended - started
prntSec2HMS(elapsedSeconds)		# This is from my toolbox.py
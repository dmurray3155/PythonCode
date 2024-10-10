# ------------------------------------------------------------------------------
# FileName: HowManyLines.py
# Purpose:	Report how many lines are in a data file (text or csv)
# Author: 	Donald Murray
# Date: 		2018-03-13
# Notes:		This is to give me a quick way to determine file length without
#						the need to open the file in UE.
# ------------------------------------------------------------------------------

#
# import my toolbox
#
from sys import path
path.append("F:/Python/tools")
from toolbox import prntSec2HMS

#
# Initialize start time for process
#
import time
import datetime
started = time.time()
startTimeVal = datetime.datetime.fromtimestamp(started)
print("Started: " + startTimeVal.strftime('%Y-%m-%d %H:%M:%S'))

#
# Set Target values
#
locFldr = "F:/SBAC/16-17/SBAC/"

#
# Set up to read the CSV file of MI student data
# 
ThisFyl = locFldr + "ca_student.csv"

import csv
csv2db = csv.reader(open(ThisFyl), delimiter=',')
numCSVlines = len(open(ThisFyl).readlines())
print("State: CA - School Year: 16-17 - Load: Student Data - Number of Lines: " + str(format(numCSVlines - 1, ',d')))

ended = time.time()
endVal = datetime.datetime.fromtimestamp(ended)
print("Ended: " + endVal.strftime('%Y-%m-%d %H:%M:%S'))
elapsedSeconds = ended - started
prntSec2HMS(elapsedSeconds)		# This is from my toolbox.py
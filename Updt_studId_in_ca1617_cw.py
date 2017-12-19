# ------------------------------------------------------------------------------
# FileName: Updt_studId_in_ca1617_cw.py
# Purpose: There were a small number of cases in the XML files where the 
#						student ID was at the fourth row of the ExamineeAttribute block
#						rather than the fifth.  Those records have grade as student ID.
#						I queried the affected records and exported the filename.  For
#						those filenames I re-read the XML files, get the student ID and
#						build the file of update statements.
# Author: Donald Murray
# Date: 2017-12-16 (yeah, Saturday ... sigh)
# Notes:
#   This process improves upon the goal of speeding up the acquisition of 
#				other information that is not included in the CSVs and must be harvested
#				from the XML data.
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
locFldr = "F:/SBAC/16-17/ETS_CA/XML"
Subj = "MATH"
Grd = "11"
SbjGd = "M11"
print("Subject: " + Subj + " - Grade: " + Grd)

#
# Read list of filenames that show this anomaly (queried ahead of time)
#
fileRef = locFldr + "/FixStIDs/" + Subj + "_" + Grd + "_stId_" + Grd + "_filename.txt"
dfile = open(fileRef, 'r')
fnames = dfile.readlines()

#
# These lines set up to export the results to a SQL file
#
sqlExport = locFldr + "/FixStIDs/updt_" + Subj + "_" + Grd + ".sql" # This is the target file to write the data to
sql = open(sqlExport, "w") # "w" indicates that it is opened for writing

#
# Set up access to the zipped folder that contains the XML files
#
import zipfile
from os import listdir
from os.path import isfile, join
mypath = locFldr + "/"
targetFile = SbjGd + '.zip'
trgtPathFile = mypath + targetFile
z = zipfile.ZipFile(trgtPathFile, "r")
#
# Now set up to parse the studentId from the XML files in mypath
from xml.dom import minidom

fnum = 1		# the first element is the header: "filename"
while fnum < len(fnames):
	xfnamewFldr = SbjGd + '/' + fnames[fnum][:-1]
	xfname = fnames[fnum][:-1]
	ThisKidTest = minidom.parse(z.open(xfnamewFldr))
	TDSR = ThisKidTest.getElementsByTagName("TDSReport")[0]
	Stud = TDSR.getElementsByTagName("Examinee")[0]
	ExAttr = Stud.getElementsByTagName("ExamineeAttribute")[3]
	StudId = ExAttr.getAttribute('value')
	sqlrow = "UPDATE ca1617_xml_fn_studid_cw SET studentid = '" + StudId + "' WHERE subject = '" + Subj + "' AND grade = '" + Grd + "' AND filename = '" + xfname + "' AND studentid = '" + Grd + "';\n"
	sql.write(sqlrow)
	fnum +=1

#
# wrap up time reporting
ended = time.time()
endTimeVal = datetime.datetime.fromtimestamp(ended)
print("Ended: " + endTimeVal.strftime('%Y-%m-%d %H:%M:%S'))
elapsedSeconds = ended - started
prntSec2HMS(elapsedSeconds)		# This is from my toolbox.py
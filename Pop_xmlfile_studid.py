# ------------------------------------------------------------------------------
# FileName: Pop_xmlfile_studid.py
# Purpose: Read the filenames in this folder: F:\SBAC\16-17\ETS_CA\XML\EL3\
#          (those are the ELA grade 3 XML files from CA 16-17) and then
#          read the studentId from each file.  Assemble this information
#          into the table ca1617.xml_fn_studid_cw (CA 1617 xml filename and 
#          studentId crosswalk) along with subject and grade.
# Author: Donald Murray
# Date: 2017-12-12 (and ongoing through the end of 2017)
# Notes:
#   This becomes necessary to speed up the acquisition of other information
#      that is not included in the CSVs and must be harvested from the XML 
#      data.  Using UltraFinder, a single studentId search in that folder
#      takes a little more than an hour.
# ------------------------------------------------------------------------------
#
# Initialize start time and structural variables
import time
import datetime
started = time.time()
startVal = datetime.datetime.fromtimestamp(started)
print("Started: " + startVal.strftime('%Y-%m-%d %H:%M:%S'))
#
# Set Target values
#
Subj="MATH"
Grd="11"
SbjGd="M11"
print("Subject: " + Subj + " - Grade: " + Grd)
#
# These lines set up to export the results to a SQL file
#
sqlExport = "F:/SBAC/16-17/ETS_CA/XML/bulkInsert_"+Subj+Grd+".sql" # This is the target file to write the data to
sql = open(sqlExport, "w") # "w" indicates that it is opened for writing
sqlHeader = "INSERT INTO ca1617_xml_fn_studid_cw (Subject, Grade, studentId, fileName) VALUES\n"
sql.write(sqlHeader)
#
# Now retrieve all of the filenames into a list.  logic source: 
# https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
#
#
# Next, implement this technique to avoid having to unzip the compressed folder:
# https://stackoverflow.com/questions/22646623/how-to-read-text-files-in-a-zipped-folder-in-python
#
#
import zipfile
from os import listdir
from os.path import isfile, join
mypath = "F:/SBAC/16-17/ETS_CA/XML/"
targetFile = SbjGd + '.zip'
trgtPathFile = mypath + targetFile
z = zipfile.ZipFile(trgtPathFile, "r")
#
# Now set up to parse the studentId from the XML files in mypath
from xml.dom import minidom
filerownum = 1
# with z.open(filename) as f:
for filename in z.namelist():
	ThisKidTest = minidom.parse(z.open(filename))
	TDSR = ThisKidTest.getElementsByTagName("TDSReport")[0]
	Stud = TDSR.getElementsByTagName("Examinee")[0]
	ExAttr = Stud.getElementsByTagName("ExamineeAttribute")[4]
	StudId = ExAttr.getAttribute('value')
	# Need to strip off the folder reference from the filename
	fnOnly = filename.split('/')[1]
	# print('AlternateSSID: '+StudId)
	if filerownum == len(z.namelist()):
		sqlrow = "('"+Subj+"','"+Grd+"','"+StudId+"','"+fnOnly+"');"
		sql.write(sqlrow)
	else:
		if filerownum%5000 == 0:
			sqlrow = "('"+Subj+"','"+Grd+"','"+StudId+"','"+fnOnly+"');\n"
			sql.write(sqlrow)
			sql.write(sqlHeader)
			# helps me keep track of progress and predict end time
			thisNow = time.time()
			midVal = datetime.datetime.fromtimestamp(thisNow)
			print("File row number: " + str(format(filerownum, ',d')) + " at: " + midVal.strftime('%Y-%m-%d %H:%M:%S'))
		else:
			sqlrow = "('"+Subj+"','"+Grd+"','"+StudId+"','"+fnOnly+"'),\n"
			sql.write(sqlrow)
	filerownum += 1
ended = time.time()
endVal = datetime.datetime.fromtimestamp(ended)
print("Ended: " + endVal.strftime('%Y-%m-%d %H:%M:%S'))
elapsedSeconds = ended - started
elapsedHours = int(elapsedSeconds / 3600)
elapsedMinutes = int((elapsedSeconds - (elapsedHours * 3600)) / 60)
remainingSeconds = (elapsedSeconds - (elapsedHours * 3600)) - (elapsedMinutes *60)
print("Elapsed Seconds: " + str(elapsedSeconds))
print("Elapsed Time: " + str(elapsedHours) + ":" + str(elapsedMinutes) + ":" + str(remainingSeconds))
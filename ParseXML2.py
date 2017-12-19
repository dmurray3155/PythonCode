# ------------------------------------------------------------------------------
# FileName: ParseXML2.py
# Purpose: Parse the XML files that contain assessment data from California
#          and write out CSV and / or perform summary analytics.  Future
#          development may include building insert statements for RDBMS
# Author: Donald Murray
# Date: 2017-12-12
# Notes:
#   See this youtube: https://www.youtube.com/watch?v=c2qlCZhkwtE
#   This one uses minidom in xml.com
# ------------------------------------------------------------------------------

from xml.dom import minidom
ThisKidTest = minidom.parse("F:/SBAC/16-17/ETS_CA/XML/EL3/0002434908002014.xml")
TDSR = ThisKidTest.getElementsByTagName("TDSReport")[0]
Stud = TDSR.getElementsByTagName("Examinee")[0]
ExAttr = Stud.getElementsByTagName("ExamineeAttribute")[4]
StudId = ExAttr.getAttribute('value')
# print('AlternateSSID: '+StudId)
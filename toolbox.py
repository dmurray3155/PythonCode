# ------------------------------------------------------------------------------
# FileName: toolbox.py
# Purpose: This python code contains user defined functions that are used
#						often enough to devote them to a toolbox that is included with
#						each python work session. Date of each addition is recorded in 
#						the function comment header.
# Author: Donald Murray
# Date: 2017-12-16 (Date of initiation of this python toolbox - yeah Saturday)
# Notes:
#   The structure and usage of this toolbox is much like my long practiced
#				toolbox method in SAS with Pacific Metrics.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Function name: prntSec2HMS(seconds)
# Purpose: display seconds value in HH:MM:SS.ss 
# Author: Donald Murray
# Date Added: 2017-12-16 (yeah, Saturday)
# ------------------------------------------------------------------------------
def prntSec2HMS(seconds):
		elapsedHours = int(seconds / 3600)
		elapsedMinutes = int((seconds - (elapsedHours * 3600)) / 60)
		remainingSeconds = seconds - (elapsedHours * 3600) - (elapsedMinutes *60)
		# print("Elapsed Seconds: " + str(elapsedSeconds))
		print('Elapsed Time (HH:MM:SS.ss): {:02d}:{:02d}:{:00.2f}'.format(elapsedHours, elapsedMinutes, remainingSeconds))

# ------------------------------------------------------------------------------
# Function name: YN2Bool(YNFlag)
# Purpose: Convert "Yes" / "No" to 1 / 0
# Author: Donald Murray
# Date Added: 2018-01-29
# Note: YNFlag values not in ("Yes", "No") will return a dot
# ------------------------------------------------------------------------------
def YN2Bool(YNFlag):
		if YNFlag == "Yes":
			return "1"
		elif YNFlag == "No":
			return "0"
		else:
			return "."

# ------------------------------------------------------------------------------
# Function name: Bool2YN(Bool)
# Purpose: Convert 1 / 0 to "Yes" / "No"
# Author: Donald Murray
# Date Added: 2018-03-01
#	Note: Bool values not in (1, 0) will return a zero length string
# ------------------------------------------------------------------------------
def Bool2YN(Bool):
		if Bool == 1:
			return "Yes"
		elif Bool == 0:
			return "No"
		else:
			return ""

# ------------------------------------------------------------------------------
# Function name: quadratic(a, b, c)
# Purpose: Compute and print any real roots of a quadratic equation
# Author: Donald Murray
# Date Added: 2017-12-16 (yeah, Saturday)
# Note: Include related conditions associated with the discriminant
# ------------------------------------------------------------------------------
def quadratic(a, b, c):
		print("a =",a,",  b =",b,",  c =",c)
		print("Equation: ",a,"* x**2","+",b,"* x", "+",c,"= 0")
		import math
		d = b**2 - 4*a*c		# compute the discriminant
		if d < 0:
			print("This equation has no real roots")
		elif d == 0:
			x = (-b + d)/(2*a)
			print("This equation has one real root: ", x)
		else:
			x1 = (-b + math.sqrt(d))/(2*a)
			x2 = (-b - math.sqrt(d))/(2*a)
			print("This equation has two real roots: ", x1, " and ", x2)

# ------------------------------------------------------------------------------
# Function name: SetYYYYMMDD()
# Purpose: Set the current date to the field named YYYYMMDD
# Author: Donald Murray
# Date Added: 2018-04-20
#	Note: This is needed as part of my AuditDBContent process
#				The conditional, dlm, is a boolean (0, 1) that controls whether
#					delimiters are included in the returned value (in this case hyphens)
# ------------------------------------------------------------------------------
def SetYYYYMMDD(dlm):
	import datetime
	now = datetime.datetime.now()
	if dlm == 1:
		YYYYMMDD = now.strftime("%Y-%m-%d")
	else:
		YYYYMMDD = now.strftime("%Y%m%d")
	return YYYYMMDD

# ------------------------------------------------------------------------------
# Function name: SetHHMMSS()
# Purpose: Set the current time to the field named HHMMSS
# Author: Donald Murray
# Date Added: 2018-04-20
#	Note: This is needed for downstream machine-created feedback file 
#					version control
#				The conditional, dlm, is a boolean (0, 1) that controls whether
#					delimiters are included in the returned value (in this case colons)
# ------------------------------------------------------------------------------
def SetHHMMSS(dlm):
	import datetime
	now = datetime.datetime.now()
	if dlm == 1:
		HHMMSS = now.strftime("%H:%M:%S")
	else:
		HHMMSS = now.strftime("%H%M%S")
	return HHMMSS

# ------------------------------------------------------------------------------
# Function name: ParseFromItemJson()
# Purpose: Retrieve metadata values from item_json that are not presented by
#					 IMRT. This is interpreted from my SAS macro of the same name.
# Author: Donald Murray
# Date Added: 2018-08-03
#	Note:
# ------------------------------------------------------------------------------
def ParseFromItemJson(textMatch, contentLength, item_json):
	# textMatchEnc = "'" + textMatch + "':"
	print("textMatch: " + textMatch)
	print("contentLength: " + str(contentLength))
	fieldLoc = item_json.find(textMatch) - 1
	print("fieldLoc: " + str(fieldLoc))
	handleLen = len(textMatch)
	print("handleLen: " + str(handleLen))
	jsonChopLen = handleLen + contentLength + 8
	print("jsonChopLen: " + str(jsonChopLen))
	jsonChopEnd = fieldLoc + jsonChopLen
	print("jsonChopEnd: " + str(jsonChopEnd))
	jsonChopOut = item_json[fieldLoc:jsonChopEnd]
	trgtCnt = jsonChopOut.split(':')[1]
	cntHDlm = trgtCnt[1:2]
	cntTDlm = cntHDlm + ','
	cntStartPos = handleLen + 4
	cntEndPos = jsonChopOut.find(cntTDlm) + 1
	resultVal = jsonChopOut[cntStartPos:cntEndPos]
	return resultVal

# ------------------------------------------------------------------------------
# Function name: CartesianTools(x1, y1, x2, y2)
# Purpose: Compute and print various values related to two points from a 
#					 cartesian coordinate plane.
# Author: Donald Murray
# Date Added: 2018-07-06
# Note: 
# ------------------------------------------------------------------------------
def CartesianTools(x1, y1, x2, y2):
	#	Confirm values of coordinates of points entered
	print("Point coordinates submitted ( x1 , y1 ); ( x2 , y2 ): (",x1,",",y1,"); (",x2,",",y2,")")
	# Compute slope and intercept of line passing through the two points
	m = ((y2 - y1) / (x2 - x1))
	b = y1 - m * x1
	print("Slope and intercept through those points: m =",m," b =",b)
#	print("Equation of line (y = m * x + b): y =",m,"* x +",b)
	#	Compute the cartesian distance
	import math
	cd = math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
	print("Distance between the points: ",cd)

# ------------------------------------------------------------------------------
# Function name: Cartesian(x1, y1, x2, y2)
# Purpose: Compute and print various values related to two points from a 
#					 cartesian coordinate plane.
# Author: Donald Murray
# Date Added: 2018-07-06
# Note: This is a class-based version of what I wrote above.
#				Source: https://nessy.info/?p=16
# ------------------------------------------------------------------------------
class Cartesian(object):

	def __init__(self, points):
		self.first, self.second = points

	def slope(self):
		'''Get the slope of a line segment'''
		(x1, y1), (x2, y2) = self.first, self.second
		try:
			return (float(y2)-y1)/(float(x2)-x1)
		except ZeroDivisionError:
			# line is vertical
			return None

	def distance(self):
		'''Compute the distance between the points'''
		(x1, y1), (x2, y2) = self.first, self.second
		import math
		return math.sqrt((y2 - y1)**2 + (x2 - x1)**2)

	def yintercept(self, slope):
		'''Get the y intercept of a line segment'''
		if slope != None:
			x, y = self.first
			return y - slope * x
		else:
			return None

	def solve_for_y(self, x, slope, yintercept):
		'''Solve for Y cord using line equation'''
		if slope != None and yintercept != None:
			return float(slope) * x + float(yintercept)
		else:
			raise Exception('Can not solve on a vertical line')

	def solve_for_x(self, y, slope, yintercept):
		'''Solve for X cord using line equatio'''
		if slope != 0 and slope:
			return float((y - float(yintercept))) / float(slope)
		else:
			raise Exception('Can not solve on a horizontal line')

#	Function to upload to AWS S3
#	Source: https://medium.com/bilesanmiahmad/how-to-upload-a-file-to-amazon-s3-in-python-68757a1867c6
def upload_to_aws(local_file, bucket, s3_file):
	import boto3
	from botocore.exceptions import NoCredentialsError

	session = boto3.Session(profile_name='default')
	s3 = session.client('s3')

	try:
		s3.upload_file(local_file, bucket, s3_file)
		print("Upload Successful")
		return True
	except FileNotFoundError:
		print("The file was not found")
		return False
	except NoCredentialsError:
		print("Credentials not available")
		return False
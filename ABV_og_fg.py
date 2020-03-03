#!/usr/bin/python
# --------------------------------------------------------------------------------------------------
# FileName:	ABV_og_fg.py
# Purpose:	Given measures of original gravity and final gravity, compute alcohol by volume.
#						original gravity (og) and final gravity (fg) are command-line parameters at execution.
# Author:		Donald Murray
# Date:			2020-03-02
# Notes:		Dependent data is a CSV of the same file name (ABV_og_fg.csv) that should be stored
#						into the same folder as this python script.  The CSV is of hydrometer readings and
#						potential resultant ABV as an python dictionary that is used as a hash lookup.
#	Usage:		This command on the command-line: "python ABV_og_fg.py 1.070 1.017" computes the ABV
#						for a beer for which its original	gravity measures 1.070 and its final gravity measures
#						0.017.
# --------------------------------------------------------------------------------------------------

locFldr = 'C:/Users/Donald Murray/Documents/GitHub/PythonCode'

from sys import path
path.append("C:/Users/Donald Murray/Documents/GitHub/PythonCode")
from toolbox import alcByVol

#	Set up for arguments of og and fg on command-line
import sys

#	print('Number of arguments: ', len(sys.argv), 'arguments.')
#	print('Argument List:', sys.argv)

#	Compute final alcohol by volume (abv) from og and fg (from my toolbox)
abv = alcByVol(sys.argv[1], sys.argv[2])
print("ABV: {0:4.1f} percent".format(abv))
print('og: ', sys.argv[1])
print('fg: ', sys.argv[2])